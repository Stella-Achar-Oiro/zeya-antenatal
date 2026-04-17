"""Single source of truth for all domain string values.

Import from here. Never use raw string literals in model fields.
"""

from enum import Enum


class Language(str, Enum):
    EN = "en"
    SW = "sw"


class DangerCategory(str, Enum):
    BLEEDING = "bleeding"
    HEADACHE_VISION = "headache_vision"
    FEVER = "fever"
    FETAL_MOVEMENT = "fetal_movement"
    ABDOMINAL_PAIN = "abdominal_pain"
    WATER_BREAKING = "water_breaking"
    CONVULSIONS = "convulsions"
    SWELLING = "swelling"
