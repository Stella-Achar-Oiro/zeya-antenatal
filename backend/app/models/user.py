"""UserProfile model.

Represents a registered user's profile, stored in the in-memory store
keyed by Clerk user ID. Gestational age is recorded at registration and
projected forward dynamically.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from app.enums import Language


class UserProfile(BaseModel):
    """A registered user's antenatal profile.

    Args:
        id: Internal UUID. Never set by callers.
        clerk_user_id: Clerk-issued user ID from the JWT.
        name: Display name provided at registration.
        gestational_age_weeks: Weeks pregnant at time of registration.
        enrolled_at: UTC datetime when the profile was created.
        language: Preferred response language — English or Swahili.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clerk_user_id: str
    name: Optional[str] = None
    gestational_age_weeks: Optional[int] = None
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    language: Language = Language.EN

    def current_gestational_age(self) -> Optional[int]:
        """Calculate current gestational age by adding weeks elapsed since enrollment.

        Returns:
            Current gestational age in weeks, or None if not recorded at registration.
        """
        if self.gestational_age_weeks is None:
            return None
        weeks_elapsed = (datetime.now(timezone.utc) - self.enrolled_at).days // 7
        return self.gestational_age_weeks + weeks_elapsed


class RegisterRequest(BaseModel):
    """Request body for user registration.

    Args:
        clerk_user_id: Clerk-issued user ID from the JWT.
        name: User's preferred name.
        gestational_age_weeks: Weeks pregnant at time of registration. 1-42.
        language: Preferred response language. Defaults to English.
    """

    clerk_user_id: str
    name: Optional[str] = None
    gestational_age_weeks: Optional[int] = Field(None, ge=1, le=42)
    language: Language = Language.EN
