"""Unit tests for danger sign detection.

Pure logic tests — no HTTP, no store, no OpenAI calls.
"""

import pytest

from app.services.danger_signs import detect_danger_signs
from app.enums import DangerCategory


def test_no_danger_signs_in_normal_message():
    result = detect_danger_signs("I am feeling well today, just a bit tired.")
    assert not result.detected
    assert result.categories == []
    assert result.keywords == []


def test_detects_bleeding_english():
    result = detect_danger_signs("I have been experiencing heavy bleeding since morning.")
    assert result.detected
    assert DangerCategory.BLEEDING in result.categories


def test_detects_bleeding_swahili():
    result = detect_danger_signs("Nina kutoka damu nyingi.")
    assert result.detected
    assert DangerCategory.BLEEDING in result.categories


def test_detects_severe_headache():
    result = detect_danger_signs("I have a severe headache and blurred vision.")
    assert result.detected
    assert DangerCategory.HEADACHE_VISION in result.categories


def test_detects_fetal_movement_english():
    result = detect_danger_signs("I can't feel the baby moving at all today.")
    assert result.detected
    assert DangerCategory.FETAL_MOVEMENT in result.categories


def test_detects_water_breaking():
    result = detect_danger_signs("My water broke about an hour ago.")
    assert result.detected
    assert DangerCategory.WATER_BREAKING in result.categories


def test_detects_convulsions():
    result = detect_danger_signs("She had a seizure and passed out briefly.")
    assert result.detected
    assert DangerCategory.CONVULSIONS in result.categories


def test_detects_swelling():
    result = detect_danger_signs("My face and hands are severely swollen.")
    assert result.detected
    assert DangerCategory.SWELLING in result.categories


def test_detects_multiple_categories():
    result = detect_danger_signs("I have heavy bleeding and a severe headache.")
    assert result.detected
    assert DangerCategory.BLEEDING in result.categories
    assert DangerCategory.HEADACHE_VISION in result.categories
    assert len(result.categories) == 2


def test_bool_true_when_detected():
    result = detect_danger_signs("heavy bleeding")
    assert bool(result) is True


def test_bool_false_when_not_detected():
    result = detect_danger_signs("feeling good")
    assert bool(result) is False


def test_case_insensitive():
    result = detect_danger_signs("HEAVY BLEEDING from this morning.")
    assert result.detected
    assert DangerCategory.BLEEDING in result.categories
