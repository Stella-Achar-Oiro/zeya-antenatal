"""Chat message models.

Represents a single turn in a conversation and the incoming
request payload for the chat endpoint.
"""

from pydantic import BaseModel, Field

from app.enums import Language


class ChatMessage(BaseModel):
    """A single conversation turn.

    Args:
        role: Speaker — 'user' or 'assistant'.
        content: Text content of the turn.
    """

    role: str
    content: str


class ChatRequest(BaseModel):
    """Request body for the streaming chat endpoint.

    Args:
        message: The user's incoming message. Max 2 000 characters.
        clerk_user_id: Clerk-issued user ID used to look up profile and history.
        language: Override language for this message. Falls back to profile preference.
    """

    message: str = Field(..., min_length=1, max_length=2000)
    clerk_user_id: str
    language: Language = Language.EN
