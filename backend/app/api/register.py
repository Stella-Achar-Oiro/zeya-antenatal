"""User registration router.

POST /api/register — saves or updates a user's antenatal profile in the
in-memory store. Called from the frontend after Clerk sign-in when the user
completes the registration form (name, gestational age, language).
"""

import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.models.user import RegisterRequest, UserProfile
from app.services import memory as mem

logger = logging.getLogger(__name__)

router = APIRouter(tags=["register"])


class RegisterResponse(BaseModel):
    """Response body confirming successful registration.

    Args:
        clerk_user_id: The registered user's Clerk ID.
        registered: Always True on success.
    """

    clerk_user_id: str
    registered: bool


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(body: RegisterRequest) -> RegisterResponse:
    """Create or update a user profile.

    Idempotent — calling again with the same clerk_user_id overwrites the
    existing profile. Returns 201 on both create and update.

    Args:
        body: Validated registration payload.

    Returns:
        RegisterResponse confirming the user ID and success flag.
    """
    profile = UserProfile(
        clerk_user_id=body.clerk_user_id,
        name=body.name,
        gestational_age_weeks=body.gestational_age_weeks,
        language=body.language,
    )
    mem.save_profile(profile)
    logger.info(
        "Registered user %s language=%s gestational_age=%s",
        body.clerk_user_id,
        body.language,
        body.gestational_age_weeks,
    )
    return RegisterResponse(clerk_user_id=body.clerk_user_id, registered=True)
