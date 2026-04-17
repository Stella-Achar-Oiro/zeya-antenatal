"""Chat router — SSE streaming endpoint.

POST /api/chat — accepts a user message and streams the AI response
token-by-token as Server-Sent Events. The frontend reads the stream and
appends tokens to the message bubble as they arrive.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.message import ChatRequest
from app.services.ai_engine import stream_response

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


@router.post("/chat")
async def chat(body: ChatRequest) -> StreamingResponse:
    """Stream an AI response for the user's message.

    Runs danger sign detection before the AI call. If danger signs are
    detected, the emergency response header is yielded first. Conversation
    history is loaded and saved automatically inside the engine.

    Args:
        body: Validated chat request with message, clerk_user_id, and language.

    Returns:
        StreamingResponse with Content-Type text/event-stream. Each chunk
        is a JSON-encoded SSE event: data: {"token": "..."} or data: [DONE].
    """
    logger.info("Chat request from user %s", body.clerk_user_id)
    return StreamingResponse(
        stream_response(
            user_message=body.message,
            clerk_user_id=body.clerk_user_id,
            language=body.language,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
