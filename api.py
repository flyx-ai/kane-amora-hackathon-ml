import itertools
import logging
import random as rand
import textwrap
import traceback
from pprint import pformat
from typing import AsyncGenerator, Optional

import openai
from utils.gpt_io_adapter import GPTIOAdapter
from utils.schemas import ChatMessage

logger = logging.getLogger("fastapi-logger")
logger.propagate = False


class GPTApi:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.gpt_io_adapter = GPTIOAdapter()

    async def aio_chat(
        self, query: str, chat_history: list[ChatMessage], character: Character
    ) -> AsyncGenerator[dict, Optional[bool]]:
        pass