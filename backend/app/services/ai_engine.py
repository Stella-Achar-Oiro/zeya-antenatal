"""AI engine — OpenAI tool-calling loop with SSE streaming.

Handles prompt assembly, danger sign context injection, the tool-call loop,
and token-by-token streaming back to the caller via an async generator.

Pattern adapted from the agentic course foundations app (app.py tool loop)
and the Zeya AI engine, rewritten for the OpenAI Python SDK v2.
"""

import json
import logging
import os
from collections.abc import AsyncGenerator
from typing import Optional

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from app.enums import Language
from app.models.message import ChatMessage
from app.services import memory as mem
from app.services.danger_signs import detect_danger_signs, emergency_response
from app.services.templates import (
    SYSTEM_PROMPT,
    TOOLS,
    build_context,
    fallback_response,
)

logger = logging.getLogger(__name__)

_client: AsyncOpenAI | None = None
MODEL = "gpt-4o-mini"


def _get_client() -> AsyncOpenAI:
    """Return the shared AsyncOpenAI client, initialising on first call."""
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


# ---------------------------------------------------------------------------
# Tool execution
# ---------------------------------------------------------------------------

def _handle_tool_call(tool_name: str, arguments: str) -> str:
    """Execute a tool call and return the result as a JSON string.

    Args:
        tool_name: Name of the tool to invoke.
        arguments: JSON-encoded argument string from the model.

    Returns:
        JSON string result to pass back to the model.
    """
    args = json.loads(arguments)
    if tool_name == "record_unanswered_question":
        question = args.get("question", "")
        logger.info("Unanswered question recorded: %s", question)
        return json.dumps({"recorded": True})
    logger.warning("Unknown tool called: %s", tool_name)
    return json.dumps({"error": "unknown tool"})


# ---------------------------------------------------------------------------
# Message builder
# ---------------------------------------------------------------------------

def _build_messages(
    user_message: str,
    history: list[ChatMessage],
    gestational_age_weeks: Optional[int],
    language: Language,
    danger_detected: bool,
) -> list[ChatCompletionMessageParam]:
    """Assemble the full messages list for the OpenAI call.

    Args:
        user_message: The current user message.
        history: Previous conversation turns (oldest first).
        gestational_age_weeks: Current gestational age, or None.
        language: User's preferred language.
        danger_detected: Whether danger sign keywords were found.

    Returns:
        List of message dicts ready for the OpenAI chat completions API.
    """
    context = build_context(gestational_age_weeks, language, danger_detected)
    system_content = SYSTEM_PROMPT
    if context:
        system_content += f"\n\n{context}"

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_content}
    ]
    for turn in history:
        messages.append({"role": turn.role, "content": turn.content})  # type: ignore[misc]
    messages.append({"role": "user", "content": user_message})
    return messages


# ---------------------------------------------------------------------------
# Streaming generator
# ---------------------------------------------------------------------------

async def stream_response(
    user_message: str,
    clerk_user_id: str,
    language: Language = Language.EN,
) -> AsyncGenerator[str, None]:
    """Generate a streaming AI response for an incoming user message.

    Runs danger sign detection first. If danger signs are detected, yields
    the emergency response header immediately before the AI reply.

    Implements the tool-call loop: if the model requests a tool, executes
    it, appends the result, and continues until a final text response is
    produced. Appends the completed turn to the conversation history.

    Args:
        user_message: Raw message text from the user.
        clerk_user_id: Used to retrieve profile and conversation history.
        language: Preferred response language.

    Yields:
        SSE-formatted strings — either text tokens or a [DONE] sentinel.
    """
    profile = mem.get_profile(clerk_user_id)
    gestational_age = profile.current_gestational_age() if profile else None
    effective_language = profile.language if profile else language

    danger = detect_danger_signs(user_message)

    if danger.detected:
        logger.info(
            "Danger signs detected for user %s: %s",
            clerk_user_id,
            danger.categories,
        )
        emergency = emergency_response(effective_language)
        yield f"data: {json.dumps({'token': emergency})}\n\n"

    history = mem.get_history(clerk_user_id)
    messages = _build_messages(
        user_message, history, gestational_age, effective_language, danger.detected
    )

    full_reply = ""

    try:
        # Tool-call loop — identical pattern to agentic course foundations app
        while True:
            response = await _get_client().chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,  # type: ignore[arg-type]
                stream=False,  # resolve tool calls before streaming final reply
            )

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                # Execute each tool and append results
                messages.append(choice.message)  # type: ignore[arg-type]
                for tc in choice.message.tool_calls:
                    result = _handle_tool_call(tc.function.name, tc.function.arguments)
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tc.id,
                    })
                continue

            # Final text response — stream it token by token
            final_text = choice.message.content or fallback_response(effective_language)
            full_reply += final_text

            # Stream in ~4-word chunks to simulate token streaming
            words = final_text.split(" ")
            chunk: list[str] = []
            for word in words:
                chunk.append(word)
                if len(chunk) >= 4:
                    token = " ".join(chunk) + " "
                    yield f"data: {json.dumps({'token': token})}\n\n"
                    chunk = []
            if chunk:
                yield f"data: {json.dumps({'token': ' '.join(chunk)})}\n\n"

            break

    except Exception as exc:
        logger.error("AI generation error for user %s: %s", clerk_user_id, exc)
        fallback = fallback_response(effective_language)
        yield f"data: {json.dumps({'token': fallback})}\n\n"
        full_reply = fallback

    finally:
        if full_reply:
            mem.append_turn(clerk_user_id, user_message, full_reply)
        yield "data: [DONE]\n\n"
