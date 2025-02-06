import json
import random
import httpx
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str


class OpenAIRequest(BaseModel):
    model: str = "gpt-4o-mini"
    messages: List[Message]
    stream: Optional[bool] = False


USER_AGENTS = [
    "PostmanRuntime/7.39.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]


async def chat_completions(request: OpenAIRequest):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/event-stream",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://duckduckgo.com/",
        "Content-Type": "application/json",
        "Origin": "https://duckduckgo.com",
        "Connection": "keep-alive",
        "Cookie": "dcm=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "TE": "trailers",
    }

    status_url = "https://duckduckgo.com/duckchat/v1/status"
    chat_url = "https://duckduckgo.com/duckchat/v1/chat"

    async with httpx.AsyncClient() as client:
        resp = await client.get(status_url, headers={"x-vqd-accept": "1", **headers})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        vqd4 = resp.headers.get("x-vqd-4")

    payload = {
        "model": "gpt-4o-mini",
        "messages": [message.dict() for message in request.messages],
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            chat_url, json=payload, headers={"x-vqd-4": vqd4, **headers}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

    if not request.stream:
        result_content = ""
        id = ""
        created = 0
        model = ""
        async for line in resp.aiter_lines():
            if line.startswith("data: "):
                chunk = line[6:]
                if chunk == "[DONE]":
                    break
                try:
                    data = json.loads(chunk)
                    id = data.get("id", "")
                    created = data.get("created", 0)
                    model = data.get("model", "")
                    result_content += data.get("message", "")
                except json.JSONDecodeError:
                    continue
        return {
            "id": id,
            "object": "chat.completion",
            "created": created,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": result_content},
                    "finish_reason": "stop",
                }
            ],
        }

    async def event_stream():
        async for line in resp.aiter_lines():
            if line.startswith("data: "):
                chunk = line[6:]
                if chunk == "[DONE]":
                    yield f"{chunk}"
                    break
                try:
                    data = json.loads(chunk)
                    message = data.get("message", "")
                    yield f"{message}"
                    # yield f"{json.dumps(data, ensure_ascii=False)}\n\n"
                except json.JSONDecodeError:
                    continue

    return StreamingResponse(event_stream(), media_type="text/event-stream")
