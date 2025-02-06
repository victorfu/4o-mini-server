#!/bin/bash

# Check if token is provided as argument
if [ $# -eq 0 ]; then
    echo "Error: NGROK_TOKEN is required"
    echo "Usage: ./colab_setup.sh <your_ngrok_token>"
    exit 1
fi

NGROK_TOKEN=$1

# Clone the repository
git clone https://github.com/victorfu/4o-mini-server.git

# Change to project directory
cd 4o-mini-server/

# Install required packages
pip install fastapi uvicorn pyngrok python-dotenv httpx

# Create .env file with provided ngrok token
echo "NGROK_TOKEN=$NGROK_TOKEN" > .env

# Run the server
python main.py 