from concurrent import futures
import grpc
import app.text2img_pb2 as pb2
import app.text2img_pb2_grpc as pb2_grpc
from app.model import Text2ImageModel
import io
import base64
from PIL import Image

class Text2ImageServicer(pb2_grpc.Text2ImageServicer):
    def __init__(self):
        self.model = Text2ImageModel()  # Load the AI model

    def GenerateImage(self, request, context):
        # Extract text and context from request
        text = request.text
        context_text = request.context
        
        # Basic validation (error handling)
        if not text.strip():
            return pb2.ImageResponse(image_url="", status="error: text cannot be empty")
        
        if not context_text.strip():
            return pb2.ImageResponse(image_url="", status="error: context cannot be empty")

        # Combine text and context into a single prompt
        prompt = text + " " + context_text

        # Generate image using the model
        image = self.model.generate(prompt)

        # Convert image to base64 string to send easily
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Return the image in the response
        return pb2.ImageResponse(image_url=img_str, status="success")

def serve():
    # Create a gRPC server with a thread pool
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))  # 5 concurrent users
    pb2_grpc.add_Text2ImageServicer_to_server(Text2ImageServicer(), server)
    
    # Bind the server to port 50051 on all interfaces
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("Server started at port 50051 🚀")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()