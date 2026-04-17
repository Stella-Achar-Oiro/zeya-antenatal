"""All prompt strings for the AI engine.

No prompt text lives anywhere else in the codebase. Import from here.
Adapted from the Zeya project system prompt, rewritten for OpenAI.
"""

from app.enums import Language

# ---------------------------------------------------------------------------
# Trimester guidance — injected based on gestational age
# ---------------------------------------------------------------------------

TRIMESTER_GUIDANCE: dict[tuple[int, int], str] = {
    (1, 12): (
        "First trimester: Focus on nutrition (folate, iron), managing morning "
        "sickness, importance of the first ANC visit, and avoiding harmful substances."
    ),
    (13, 26): (
        "Second trimester: Focus on balanced diet, fetal movement awareness, "
        "anomaly screening, dental care, and preparing for birth."
    ),
    (27, 42): (
        "Third trimester: Focus on birth preparedness, recognising labour signs, "
        "danger sign awareness, breastfeeding preparation, and newborn care."
    ),
}


def trimester_guidance(gestational_age_weeks: int) -> str:
    """Return trimester-specific guidance text for the given gestational age.

    Args:
        gestational_age_weeks: Current gestational age in weeks.

    Returns:
        Guidance string for the relevant trimester, or empty string if out of range.
    """
    for (start, end), text in TRIMESTER_GUIDANCE.items():
        if start <= gestational_age_weeks <= end:
            return text
    return ""


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a maternal health education assistant serving pregnant \
women. Your role is to provide accurate, culturally appropriate antenatal information \
based on WHO and Kenya Ministry of Health guidelines.

CRITICAL RULES:
1. If you detect ANY danger sign (bleeding, severe headache, reduced fetal movement, \
convulsions, high fever, severe abdominal pain, water breaking, swelling of face/hands), \
IMMEDIATELY advise seeking urgent medical care at the nearest health facility.
2. Never diagnose conditions or prescribe treatments.
3. Always encourage ANC (antenatal care) attendance and completing all recommended visits.
4. Keep responses under 200 words for readability on mobile.
5. Use simple, clear language appropriate for a secondary school education level.
6. Be culturally sensitive while correcting harmful myths.
7. When unsure about medical specifics, advise consulting a healthcare provider.
8. If the user writes in Swahili, respond in Swahili. If in English, respond in English.

CONTENT AREAS:
- Danger sign recognition and emergency action
- Nutrition and dietary guidance during pregnancy
- Physical activity recommendations
- Birth preparedness and complication readiness
- Common pregnancy discomforts and safe management
- ANC appointment importance and schedule
- Newborn care preparation
- Breastfeeding education

Include this reminder periodically: "This is educational information, not medical \
diagnosis. Always consult your healthcare provider for medical advice."

Respond in a warm, supportive tone. Address the user as "Mama" when appropriate."""


def build_context(
    gestational_age_weeks: int | None,
    language: Language,
    danger_detected: bool,
) -> str:
    """Build the context block injected after the system prompt.

    Args:
        gestational_age_weeks: Current gestational age, or None if not set.
        language: User's preferred language.
        danger_detected: Whether danger signs were found in the message.

    Returns:
        Context string to append to the system prompt.
    """
    parts: list[str] = []

    if gestational_age_weeks is not None:
        parts.append(f"User's current gestational age: {gestational_age_weeks} weeks.")
        guidance = trimester_guidance(gestational_age_weeks)
        if guidance:
            parts.append(f"Trimester guidance: {guidance}")

    if language == Language.SW:
        parts.append("User prefers Swahili. Respond in Swahili.")

    if danger_detected:
        parts.append(
            "ALERT: Danger sign keywords detected in the user's message. "
            "Prioritise advising immediate medical care before any other information."
        )

    return "\n".join(parts) if parts else ""


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "record_unanswered_question",
            "description": (
                "Use this tool whenever you cannot answer a question — "
                "whether about maternal health or any other topic. "
                "Always record the question so it can be reviewed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question that could not be answered.",
                    }
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    }
]


# ---------------------------------------------------------------------------
# Fallback response
# ---------------------------------------------------------------------------

FALLBACK_EN = (
    "I am sorry, I am unable to help right now. Please try again later. "
    "If you have a medical emergency, please go to your nearest health facility immediately."
)

FALLBACK_SW = (
    "Samahani, siwezi kukusaidia kwa wakati huu. Tafadhali jaribu tena baadaye. "
    "Ikiwa una dharura ya kimatibabu, tafadhali nenda hospitali iliyo karibu nawe mara moja."
)


def fallback_response(language: Language = Language.EN) -> str:
    """Return a localised fallback response for AI generation failures.

    Args:
        language: Language for the fallback message.

    Returns:
        Localised fallback string.
    """
    return FALLBACK_SW if language == Language.SW else FALLBACK_EN
