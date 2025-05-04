import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import grpc
import gradio as gr
import app.text2img_pb2 as pb2
import app.text2img_pb2_grpc as pb2_grpc
import base64
from PIL import Image
import io

def generate_image(text, context):
    # Connect to your gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.Text2ImageStub(channel)
    
    try:
        # Send request
        response = stub.GenerateImage(pb2.TextRequest(text=text, context=context))
        
        # Decode the base64 image
        if response.status != "success":
            raise Exception(response.status)
        
        img_data = base64.b64decode(response.image_url)
        img = Image.open(io.BytesIO(img_data))
        return img
    except Exception as e:
        raise gr.Error(str(e))

# Build the Gradio Interface
iface = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(label="Main Text", placeholder="e.g. A dragon flying over a city"),
        gr.Textbox(label="Style/Context", placeholder="e.g. fantasy, detailed, sunset")
    ],
    outputs=gr.Image(label="Generated Image"),
    title="Text2Image Generator",
    description="Enter a text and context to generate an AI image!",
    examples=[
        ["A serene lake at sunset", "photorealistic, peaceful"],
        ["A futuristic city", "cyberpunk, neon lights, rain"],
    ]
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)