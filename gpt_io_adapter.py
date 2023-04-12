from schemas import ChatMessage


class GPTIOAdapter:
    def __init__(self):
        pass

    def format_chat_history(self, chat_history: list[ChatMessage]) -> list[dict]:
        formatted_chat_history = []
        for chat_message in chat_history:
            formatted_chat_message = {
                "role": chat_message.role,
                "content": chat_message.message,
            }
            formatted_chat_history.append(formatted_chat_message)

        return formatted_chat_history