import uvicorn
from fastapi import FastAPI
from duckduckgo import chat_completions, OpenAIRequest
from pyngrok import ngrok
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


@app.get("/")
async def root():
    return ":D"


@app.get("/api/version")
async def version():
    return {"version": "1.0.0"}


@app.post("/api/chat/completions")
async def chat_completion_endpoint(request: OpenAIRequest):
    return await chat_completions(request)


if __name__ == "__main__":
    ngrok_token = os.getenv("NGROK_TOKEN")
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
    else:
        print("Warning: NGROK_TOKEN not found in environment variables")

    ngrok_tunnel = ngrok.connect(8000)
    print(f"Public URL: {ngrok_tunnel.public_url}")

    uvicorn.run(app, host="0.0.0.0", port=8000)
