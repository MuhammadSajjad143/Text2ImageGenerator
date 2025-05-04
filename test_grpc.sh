#!/bin/bash

# Install grpcurl if not already installed
if ! command -v grpcurl &> /dev/null; then
    echo "Installing grpcurl..."
    curl -sSL "https://github.com/fullstorydev/grpcurl/releases/download/v1.8.7/grpcurl_1.8.7_linux_x86_64.tar.gz" | tar -xz -C /usr/local/bin
fi

# Test the gRPC service
grpcurl -plaintext -d '{"text": "A magical forest", "context": "fantasy style"}' localhost:50051 Text2Image/GenerateImage