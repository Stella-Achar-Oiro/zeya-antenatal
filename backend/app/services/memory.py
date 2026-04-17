"""In-memory conversation and user profile store.

Keyed by Clerk user ID. Conversation history is capped at MAX_TURNS and
expires after 24 hours of inactivity. User profiles persist for the
lifetime of the process.

Phase 1 only — replace with a database-backed store in Phase 2.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.models.message import ChatMessage
from app.models.user import UserProfile

logger = logging.getLogger(__name__)

MAX_TURNS = 6
SESSION_TTL_HOURS = 24

# ---------------------------------------------------------------------------
# Internal store
# ---------------------------------------------------------------------------

_profiles: dict[str, UserProfile] = {}

_history: dict[str, list[ChatMessage]] = {}
_last_active: dict[str, datetime] = {}


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

def save_profile(profile: UserProfile) -> None:
    """Persist a user profile to the in-memory store.

    Args:
        profile: The UserProfile to save, keyed by clerk_user_id.
    """
    _profiles[profile.clerk_user_id] = profile
    logger.info("Saved profile for user %s", profile.clerk_user_id)


def get_profile(clerk_user_id: str) -> Optional[UserProfile]:
    """Retrieve a user profile by Clerk user ID.

    Args:
        clerk_user_id: The Clerk-issued user ID.

    Returns:
        The UserProfile if found, otherwise None.
    """
    return _profiles.get(clerk_user_id)


# ---------------------------------------------------------------------------
# Conversation history
# ---------------------------------------------------------------------------

def _is_expired(clerk_user_id: str) -> bool:
    """Check whether a session has exceeded the TTL.

    Args:
        clerk_user_id: The Clerk-issued user ID.

    Returns:
        True if the session has expired or never existed.
    """
    last = _last_active.get(clerk_user_id)
    if last is None:
        return True
    return datetime.now(timezone.utc) - last > timedelta(hours=SESSION_TTL_HOURS)


def get_history(clerk_user_id: str) -> list[ChatMessage]:
    """Return the recent conversation history for a user.

    Expired sessions are cleared before returning. History is capped at
    MAX_TURNS most recent messages.

    Args:
        clerk_user_id: The Clerk-issued user ID.

    Returns:
        List of ChatMessage objects, oldest first, max MAX_TURNS entries.
    """
    if _is_expired(clerk_user_id):
        clear_history(clerk_user_id)
        return []
    return _history.get(clerk_user_id, [])


def append_turn(clerk_user_id: str, user_message: str, assistant_reply: str) -> None:
    """Append a completed conversation turn and update the TTL.

    Keeps only the last MAX_TURNS messages.

    Args:
        clerk_user_id: The Clerk-issued user ID.
        user_message: The user's raw message text.
        assistant_reply: The assistant's full reply text.
    """
    if clerk_user_id not in _history:
        _history[clerk_user_id] = []

    _history[clerk_user_id].append(ChatMessage(role="user", content=user_message))
    _history[clerk_user_id].append(ChatMessage(role="assistant", content=assistant_reply))

    # Keep only the most recent MAX_TURNS messages (each turn = 2 messages)
    _history[clerk_user_id] = _history[clerk_user_id][-(MAX_TURNS * 2):]
    _last_active[clerk_user_id] = datetime.now(timezone.utc)


def clear_history(clerk_user_id: str) -> None:
    """Remove all conversation history for a user.

    Args:
        clerk_user_id: The Clerk-issued user ID.
    """
    _history.pop(clerk_user_id, None)
    _last_active.pop(clerk_user_id, None)
