"""Danger sign detection for obstetric emergencies.

Scans incoming messages for keywords indicating the 8 WHO/Kenya MOH danger
sign categories in both English and Swahili. Detection runs before every AI
call so emergency guidance is never delayed by model latency.

Ported and adapted from the Zeya project.
"""

import re
from dataclasses import dataclass

from app.enums import DangerCategory, Language

# ---------------------------------------------------------------------------
# Keyword patterns — one compiled regex list per category
# ---------------------------------------------------------------------------

PATTERNS: dict[DangerCategory, list[re.Pattern[str]]] = {
    DangerCategory.BLEEDING: [
        re.compile(r"\b(heavy\s+)?bleeding\b", re.IGNORECASE),
        re.compile(r"\bexcessive\s+blood\b", re.IGNORECASE),
        re.compile(r"\bblood\s+(clots?|loss)\b", re.IGNORECASE),
        re.compile(r"\bkutoka\s+damu\b", re.IGNORECASE),
        re.compile(r"\bdamu\s+nyingi\b", re.IGNORECASE),
    ],
    DangerCategory.HEADACHE_VISION: [
        re.compile(r"\bsevere\s+headache\b", re.IGNORECASE),
        re.compile(r"\bblurred?\s+vision\b", re.IGNORECASE),
        re.compile(r"\bvision\s+(is\s+)?blurred?\b", re.IGNORECASE),
        re.compile(r"\bseeing\s+(spots?|stars?)\b", re.IGNORECASE),
        re.compile(r"\bkichwa\s+kuuma\b", re.IGNORECASE),
        re.compile(r"\bmacho\s+kuona\s+vibaya\b", re.IGNORECASE),
    ],
    DangerCategory.FEVER: [
        re.compile(r"\bhigh\s+fever\b", re.IGNORECASE),
        re.compile(r"\bsevere\s+fever\b", re.IGNORECASE),
        re.compile(r"\bchills\b", re.IGNORECASE),
        re.compile(r"\bhoma\s+kali\b", re.IGNORECASE),
        re.compile(r"\bbaridi\s+mwilini\b", re.IGNORECASE),
    ],
    DangerCategory.FETAL_MOVEMENT: [
        re.compile(r"\breduced\s+fetal\s+movement\b", re.IGNORECASE),
        re.compile(r"\bno\s+(fetal\s+)?movement\b", re.IGNORECASE),
        re.compile(r"\bbaby\s+(not\s+moving|stopped?\s+moving|isn'?t\s+moving)\b", re.IGNORECASE),
        re.compile(r"\bcan'?t\s+feel\s+(the\s+)?baby\b", re.IGNORECASE),
        re.compile(r"\bmtoto\s+ha(tembei|chezi)\b", re.IGNORECASE),
    ],
    DangerCategory.ABDOMINAL_PAIN: [
        re.compile(r"\bsevere\s+(abdominal\s+)?pain\b", re.IGNORECASE),
        re.compile(r"\bstomach\s+pain\b", re.IGNORECASE),
        re.compile(r"\bsharp\s+pain\b", re.IGNORECASE),
        re.compile(r"\btumbo\s+kuuma\s+sana\b", re.IGNORECASE),
    ],
    DangerCategory.WATER_BREAKING: [
        re.compile(r"\bwater\s+(break(ing|s)?|broke)\b", re.IGNORECASE),
        re.compile(r"\bfluid\s+(leaking|leakage|gushing)\b", re.IGNORECASE),
        re.compile(r"\bleaking\s+fluid\b", re.IGNORECASE),
        re.compile(r"\bmaji\s+ya(mekatika|kutoka)\b", re.IGNORECASE),
    ],
    DangerCategory.CONVULSIONS: [
        re.compile(r"\bconvulsion\b", re.IGNORECASE),
        re.compile(r"\bseizure\b", re.IGNORECASE),
        re.compile(r"\bloss\s+of\s+consciousness\b", re.IGNORECASE),
        re.compile(r"\bfaint(ed|ing)\b", re.IGNORECASE),
        re.compile(r"\bpassed?\s+out\b", re.IGNORECASE),
        re.compile(r"\bdegedege\b", re.IGNORECASE),
        re.compile(r"\bkupoteza\s+fahamu\b", re.IGNORECASE),
    ],
    DangerCategory.SWELLING: [
        re.compile(r"\bsevere\s+swelling\b", re.IGNORECASE),
        re.compile(r"\bswollen\b", re.IGNORECASE),
        re.compile(r"\bseverely\s+swollen\b", re.IGNORECASE),
        re.compile(r"\bkuvimba\s+sana\b", re.IGNORECASE),
    ],
}


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class DangerSignResult:
    """Result of a danger sign scan.

    Attributes:
        detected: True if any danger sign keywords were found.
        categories: List of matched DangerCategory values.
        keywords: The specific matched strings from the message.
    """

    detected: bool
    categories: list[DangerCategory]
    keywords: list[str]

    def __bool__(self) -> bool:
        return self.detected


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def detect_danger_signs(message: str) -> DangerSignResult:
    """Scan a message for obstetric danger sign keywords.

    Checks all 8 danger sign categories against both English and Swahili
    patterns. Stops at the first match per category.

    Args:
        message: Raw message text from the user.

    Returns:
        DangerSignResult with detection status, matched categories, and keywords.
    """
    categories_found: list[DangerCategory] = []
    keywords_found: list[str] = []

    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            match = pattern.search(message)
            if match:
                categories_found.append(category)
                keywords_found.append(match.group())
                break

    return DangerSignResult(
        detected=len(categories_found) > 0,
        categories=categories_found,
        keywords=keywords_found,
    )


# ---------------------------------------------------------------------------
# Emergency response text
# ---------------------------------------------------------------------------

EMERGENCY_HEADER_EN = (
    "URGENT: This sounds like it could be a danger sign requiring immediate "
    "medical attention. Please do the following right away:\n\n"
    "1. Go to your nearest health facility immediately or call emergency services.\n"
    "2. If you cannot travel, ask someone nearby to help you get to hospital.\n"
    "3. Do NOT wait to see if symptoms improve on their own.\n\n"
)

EMERGENCY_HEADER_SW = (
    "DHARURA: Hii inaonekana kama dalili ya hatari inayohitaji matibabu ya haraka. "
    "Tafadhali fanya yafuatayo mara moja:\n\n"
    "1. Nenda hospitali iliyo karibu nawe mara moja au piga simu ya dharura.\n"
    "2. Ikiwa huwezi kusafiri, mwombe mtu aliye karibu akusaidie kwenda hospitalini.\n"
    "3. USISUBIRI kuona kama dalili zitaboreshwa zenyewe.\n\n"
)

EMERGENCY_FOOTER_EN = (
    "\n\nThis is educational information, not medical diagnosis. "
    "Always consult your healthcare provider for medical advice."
)

EMERGENCY_FOOTER_SW = (
    "\n\nHii ni taarifa ya kielimu, si utambuzi wa kimatibabu. "
    "Daima wasiliana na mtoa huduma wako wa afya kwa ushauri wa kimatibabu."
)


def emergency_response(language: Language = Language.EN) -> str:
    """Return a localised emergency response message.

    Args:
        language: Language for the response — EN or SW.

    Returns:
        Formatted emergency string to prepend to the AI response.
    """
    if language == Language.SW:
        return EMERGENCY_HEADER_SW + EMERGENCY_FOOTER_SW
    return EMERGENCY_HEADER_EN + EMERGENCY_FOOTER_EN
