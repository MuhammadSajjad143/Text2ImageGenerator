import grpc
import json
import base64
import app.text2img_pb2 as pb2
import app.text2img_pb2_grpc as pb2_grpc

def test_grpc_json():
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.Text2ImageStub(channel)
    
    # Create request
    request = pb2.TextRequest(
        text="A magical forest",
        context="fantasy style"
    )
    
    # Get response
    response = stub.GenerateImage(request)

    # Decode and save the image
    if response.image_url:
        try:
            with open("output.png", "wb") as f:
                f.write(base64.b64decode(response.image_url))
            image_saved = True
        except Exception as e:
            print("Error saving image:", e)
            image_saved = False
    else:
        image_saved = False

    # Convert to JSON
    json_response = {
        'status': response.status,
        'image_url': response.image_url[:100] + '...' if response.image_url else '',
        'image_saved': image_saved
    }

    # Print formatted JSON
    print(json.dumps(json_response, indent=2))

if __name__ == "__main__":
    test_grpc_json()
