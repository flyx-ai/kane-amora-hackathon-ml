import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from datetime import datetime

import uvicorn
from decouple import config
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware

from api import GPTApi
from gpt_io_adapter import GPTIOAdapter
from schemas import ChatInput, IdleInput

app = FastAPI(docs_url="/")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "PATCH", "POST", "PUT"],
    allow_headers=["*"],
)

gpt_api = GPTApi(config("OPENAI_API_KEY"))
gpt_io_adapter = GPTIOAdapter()


@app.post("/chat", response_model_exclude_none=False)
async def chat(payload: ChatInput):
    async def stream_chat():
        s = datetime.now()

        chat_stream = await gpt_api.aio_chat(
            payload.message, payload.chat_history, payload.ai_traits, payload.user_traits
        )

        event_data = {
            "message": "",
            "is_error": False,
            "event_delay": f"{datetime.now() - s}",
        }

        async for message, *args in chat_stream:
            if message is not None and message != "":
                is_error = args[0] if args else False

                event_data.update(
                    {
                        "message": message,
                        "is_error": is_error,
                        "event_delay": f"{datetime.now() - s}",
                    }
                )
                yield {
                    "event": "message",
                    "data": json.dumps(event_data),
                }

        print(f"GPT resp time: {datetime.now() - s}")

    return EventSourceResponse(stream_chat())


@app.post("/idle", response_model_exclude_none=False)
async def idle(payload: IdleInput):
    async def stream_chat():
        s = datetime.now()

        chat_stream = await gpt_api.idle_chat(payload.chat_history, payload.ai_traits, payload.user_traits)

        event_data = {
            "message": "",
            "is_error": False,
            "event_delay": f"{datetime.now() - s}",
        }

        async for message, *args in chat_stream:
            if message is not None and message != "":
                is_error = args[0] if args else False

                event_data.update(
                    {
                        "message": message,
                        "is_error": is_error,
                        "event_delay": f"{datetime.now() - s}",
                    }
                )
                yield {
                    "event": "message",
                    "data": json.dumps(event_data),
                }

        print(f"GPT resp time: {datetime.now() - s}")

    return EventSourceResponse(stream_chat())


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True)
