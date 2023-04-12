import itertools
import logging
import random as rand
import textwrap
import traceback
from pprint import pformat
from typing import AsyncGenerator, Optional

import openai

from gpt_io_adapter import GPTIOAdapter
from schemas import AITraits, ChatMessage, UserTraits

logger = logging.getLogger("fastapi-logger")
logger.propagate = False


class GPTApi:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.gpt_io_adapter = GPTIOAdapter()

    async def aio_chat(
        self, query: str, chat_history: list[ChatMessage], ai_traits: AITraits, user_traits: UserTraits
    ) -> AsyncGenerator[dict, Optional[bool]]:
        # examples_prefix = """"""

        formatted_chat_history = self.gpt_io_adapter.format_chat_history(chat_history)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a chat bot that interacts with the user and acts amicable towards them."
                ),
            },
            {"role": "user", "content": "### Here are your character traits:  "},
            *formatted_chat_history,
            {
                "role": "user",
                "content": f"User: {query}",
            },
        ]

        logger.info(f"{pformat(messages)}\n")

        async def generate_chat_stream() -> AsyncGenerator[dict, Optional[bool]]:
            chat_message = ""
            async for chunk in await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["#", "`"],
                stream=True,
            ):
                try:
                    chunk_content = chunk.choices[0].delta.get("content", "")
                    chat_message += chunk_content
                    yield (chat_message,)
                except Exception:
                    pass
                
        return generate_chat_stream()