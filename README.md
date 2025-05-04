# Text2ImageGenerator

A powerful text-to-image generation service built with Stable Diffusion, gRPC, and Gradio.

## Features

- Text-to-image generation using Stable Diffusion v1.4
- gRPC service for efficient communication
- User-friendly Gradio web interface
- Docker support for easy deployment
- Comprehensive test suite

## Architecture

The application consists of three main components:

1. *gRPC Server*: Handles image generation requests using Protocol Buffers
2. *AI Model*: Stable Diffusion v1.4 for image generation
3. *Frontend*: Gradio web interface for user interaction

## Setup

### Prerequisites

- Python 3.10 or higher
- Docker (optional)
- CUDA-compatible GPU (recommended)

### Installation

1. Clone the repository:
bash
git clone <repository-url>
cd Text2ImageGenerator


2. Install dependencies:
bash
pip install -r requirements.txt
pip install -r frontend/requirements.txt


### Docker Setup

Build and run using Docker:

bash
docker build -t text2image-generator .
docker run -p 7860:7860 -p 50051:50051 text2image-generator


## Usage

### Starting the Services

1. Start the gRPC server:
bash
python -m app.server


2. Start the Gradio interface:
bash
python -m frontend.gradio_app


Access the web interface at http://localhost:7860

### API Usage

The service exposes a gRPC endpoint at port 50051. Example request:

python
import grpc
import app.text2img_pb2 as pb2
import app.text2img_pb2_grpc as pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = pb2_grpc.Text2ImageStub(channel)
response = stub.GenerateImage(pb2.TextRequest(
    text="A magical forest",
    context="fantasy style"
))


## Model Information

- *Model*: Stable Diffusion v1.4
- *Source*: CompVis/stable-diffusion-v1-4
- *License*: CreativeML Open RAIL-M
- *Capabilities*: Generates 512x512 images from text descriptions

## Testing

Run the test suite:

bash
pytest test/test_app.py


For gRPC endpoint testing:
bash
./test_grpc.sh


## Limitations

1. *Hardware Requirements*
   - GPU recommended for optimal performance
   - CPU generation is significantly slower

2. *Generation Constraints*
   - Fixed output size (512x512)
   - Generation time varies based on hardware
   - Limited to English language prompts

3. *Resource Usage*
   - High memory usage during initialization
   - Significant GPU VRAM required (>6GB recommended)

4. *Network Dependencies*
   - Requires initial model download
   - Stable internet connection needed for first setup
