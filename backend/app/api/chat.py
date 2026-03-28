import json
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse
import asyncio

from ..api.llm_client import LLMClient
from ..api.insight_recommendation import generate_insight_prompt

router = APIRouter(prefix="/api/chat", tags=["chat"])


async def generate_chat_response(message: str, csv_metadata: dict = None):
    llm = LLMClient.get_instance()

    messages = []

    if csv_metadata:
        prompt = generate_insight_prompt(
            columns=csv_metadata.get("columns", []),
            row_count=csv_metadata.get("row_count", 0),
            user_question=message,
        )
        messages.append({"role": "system", "content": prompt})

    messages.append({"role": "user", "content": message})

    response = llm.chat(messages=messages, stream=True)

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield {
                "event": "message",
                "data": json.dumps({"content": chunk.choices[0].delta.content}),
            }

    yield {"event": "done", "data": json.dumps({"done": True})}


@router.post("/stream")
async def chat_stream(request: Request):
    body = await request.json()
    message = body.get("message", "")
    csv_metadata = body.get("csv_metadata")

    return EventSourceResponse(generate_chat_response(message, csv_metadata))
