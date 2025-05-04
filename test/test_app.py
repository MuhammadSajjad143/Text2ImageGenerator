import grpc
import base64
from PIL import Image
import io
import os
import pytest
import time

# Import gRPC-generated classes
import app.text2img_pb2 as pb2
import app.text2img_pb2_grpc as pb2_grpc

# gRPC channel setup (targeting the local server)
@pytest.fixture(scope="module")
def grpc_stub():
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.Text2ImageStub(channel)
    return stub

# ✅ Test 1: Check valid text + context returns an image
def test_generate_valid_image(grpc_stub):
    request = pb2.TextRequest(text="A magical forest", context="fantasy, vibrant colors")
    response = grpc_stub.GenerateImage(request)
    
    assert response.status == "success"
    assert response.image_url != ""

    try:
        img_data = base64.b64decode(response.image_url)
        img = Image.open(io.BytesIO(img_data))
        img.verify()  # Ensures it's a valid image
    except Exception as e:
        pytest.fail(f"Failed to decode or verify image: {e}")

# ✅ Test 2: Handle empty input gracefully
def test_generate_with_empty_text(grpc_stub):
    request = pb2.TextRequest(text="", context="")
    response = grpc_stub.GenerateImage(request)
    
    assert response.status != "success"
    assert "error" in response.status.lower()

# ✅ Test 3: Check response format for long prompts
def test_generate_long_prompt(grpc_stub):
    long_text = "a" * 1000
    long_context = "b" * 500
    request = pb2.TextRequest(text=long_text, context=long_context)
    response = grpc_stub.GenerateImage(request)
    
    assert response.status in ["success", "error"]
    assert isinstance(response.image_url, str)

# ✅ Test 4: Service handles special characters
def test_generate_with_special_chars(grpc_stub):
    request = pb2.TextRequest(text="@#$% A #*()@ rainbow", context="🌈 colorful")
    response = grpc_stub.GenerateImage(request)
    
    assert response.status in ["success", "error"]

# ✅ Test 5: Functionality - Test image dimensions
def test_image_dimensions(grpc_stub):
    request = pb2.TextRequest(text="A simple circle", context="minimalist")
    response = grpc_stub.GenerateImage(request)
    
    img_data = base64.b64decode(response.image_url)
    img = Image.open(io.BytesIO(img_data))
    
    # Stable Diffusion default output is 512x512
    assert img.size == (512, 512)
    assert img.mode in ['RGB', 'RGBA']

# ✅ Test 6: Error Handling - Test malformed UTF-8 input
def test_malformed_utf8_input(grpc_stub):
    request = pb2.TextRequest(text=b'\xff\xfe'.decode('utf-8', 'ignore'), context="test")
    response = grpc_stub.GenerateImage(request)
    
    assert response.status != "success"
    assert "error" in response.status.lower()

# ✅ Test 7: Performance - Test response time
def test_response_time(grpc_stub):
    request = pb2.TextRequest(text="Quick test", context="simple")
    
    start_time = time.time()
    response = grpc_stub.GenerateImage(request)
    end_time = time.time()
    
    response_time = end_time - start_time
    # Assuming reasonable response time for GPU/CPU
    assert response_time < 60, f"Response time {response_time}s exceeded 60s threshold"

# ✅ Test 8: Security - Test input sanitization
def test_input_sanitization(grpc_stub):
    malicious_input = "'; DROP TABLE users; --"
    request = pb2.TextRequest(text=malicious_input, context="test")
    response = grpc_stub.GenerateImage(request)
    
    assert response.status == "success" or "error" in response.status.lower()
    # Ensure the service continues to function after malicious input
    assert grpc_stub.GenerateImage(pb2.TextRequest(text="test", context="test")).status in ["success", "error"]