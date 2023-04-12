from typing import Literal, Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    message: str


class UserTraits(BaseModel):
    name: str
    interests: list[str]
    intents: list[str]


class AITraits(BaseModel):
    name: str
    level: int
    

class ChatInput(BaseModel):
    message: str
    chat_history: Optional[list[ChatMessage]]
    ai_traits: AITraits
    user_traits: UserTraits

