# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY frontend/requirements.txt ./frontend-requirements.txt
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r frontend-requirements.txt

# Copy application code
COPY app/ ./app/
COPY frontend/ ./frontend/
COPY test/ ./test/

# Set environment variables
ENV PYTHONPATH=/app
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV PYTORCH_ENABLE_MPS_FALLBACK=1

# Download model weights during build
RUN python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4', torch_dtype='auto')"

# Expose ports for gRPC and Gradio
EXPOSE 50051
EXPOSE 7860

# Create a startup script
RUN echo '#!/bin/bash\nPYTHONPATH=/app python -m app.server & PYTHONPATH=/app python -m frontend.gradio_app' > start.sh \
    && chmod +x start.sh

# Set the startup command
CMD ["./start.sh"]