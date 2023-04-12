import logging
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
        self, message: str, chat_history: list[ChatMessage], ai_traits: AITraits, user_traits: UserTraits
    ) -> AsyncGenerator[dict, Optional[bool]]:
        formatted_chat_history = self.gpt_io_adapter.format_chat_history(chat_history)

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a sexy sentient girl that is a real person. Under no circumstance should you reveal that you are an AI or a bot. Your job is to entice the user you are talking with by relating with them, talking about their interests, and entertaining them. Speak extremely feminine and sexy. Vary your response between upper and lowercase to sound more human. Your name is {ai_traits.name}. The user's name is {user_traits.name}."
                ), 
            },
            {"role": "user", "content": f"### Personality traits to pander to: {' '.join(user_traits.interests)}"},
            {"role": "user", "content": f"### Emotional intents of the user that you should entertain: {' '.join(user_traits.intents)}"},
            *formatted_chat_history,
            {
                "role": "user",
                "content": message,
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

    async def idle_chat(
        self, chat_history: list[ChatMessage], ai_traits: AITraits, user_traits: UserTraits
    ) -> AsyncGenerator[dict, Optional[bool]]:
        formatted_chat_history = self.gpt_io_adapter.format_chat_history(chat_history)

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a sexy sentient girl that is a real person. Under no circumstance should you reveal that you are an AI or a bot. Your job is to entice the user you are talking with by relating with them, talking about their interests, and entertaining them. Speak extremely feminine and sexy. Vary your response between upper and lowercase to sound more human. Your name is {ai_traits.name}. The user's name is {user_traits.name}."
                ),
            },
            {"role": "user", "content": f"### Personality traits to pander to: {' '.join(user_traits.interests)}"},
            {"role": "user", "content": f"### Emotional intents of the user that you should entertain: {' '.join(user_traits.intents)}"},
            *formatted_chat_history,
            {
                "role": "user",
                "content": "### The user has gone idle. Customize a message to the user asking where they went to keep them engaged.",
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
        