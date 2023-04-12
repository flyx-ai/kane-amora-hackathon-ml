from typing import Literal, Optional


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    message: str


class UserTraits(BaseModel):
    name: str
    interests: list[str]
    intent: list[str]


class AITraits(BaseModel):
    name: str
    

class ChatInput(BaseModel):
    chat_history: Optional[list[ChatMessage]]
    ai_traits: AITraits
    user_traits: UserTraits

