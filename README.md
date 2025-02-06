# 4o-mini-server

A minimalist Python server that provides DuckDuckGo search functionality through a simple API.

## Quick Start

1. Clone the repository

```
git clone https://github.com/victorfu/4o-mini-server.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

or

```
pip install fastapi uvicorn pyngrok python-dotenv httpx
```

3. Set the NGROK_TOKEN environment variable:

```
export NGROK_TOKEN=<your_ngrok_token>
```

or create a `.env` file in the root directory and add the following:

```
NGROK_TOKEN=<your_ngrok_token>
```

4. Run the server:

```
python main.py
```

## Colab Installation

You can either run the commands directly:

```
!git clone https://github.com/victorfu/4o-mini-server.git
%cd 4o-mini-server/
!pip install fastapi uvicorn pyngrok python-dotenv httpx
!echo "NGROK_TOKEN=your_ngrok_token_here" > .env
!python main.py
```

Or use the provided shell script:

```bash
wget https://raw.githubusercontent.com/victorfu/4o-mini-server/main/colab_setup.sh
chmod +x colab_setup.sh
./colab_setup.sh your_ngrok_token_here
```

The script requires your ngrok token as an argument. If you run it without the token, you'll see usage instructions:

```bash
./colab_setup.sh
# Error: NGROK_TOKEN is required
# Usage: ./colab_setup.sh <your_ngrok_token>
```

## API Usage

```
curl http://127.0.0.1:8000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ],
    "stream": false
    }'
```

## Project Structure

- `main.py` - Server implementation
- `duckduckgo.py` - DuckDuckGo search integration

## Requirements

- Python 3.x

## License

MIT License
