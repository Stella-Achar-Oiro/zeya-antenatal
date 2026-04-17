"""Integration tests for the registration endpoint."""

import pytest

from app.services import memory as mem


@pytest.mark.asyncio
async def test_register_creates_profile(client):
    response = await client.post("/api/register", json={
        "clerk_user_id": "user_abc123",
        "name": "Achieng",
        "gestational_age_weeks": 20,
        "language": "en",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["registered"] is True
    assert data["clerk_user_id"] == "user_abc123"


@pytest.mark.asyncio
async def test_register_saves_to_memory(client):
    await client.post("/api/register", json={
        "clerk_user_id": "user_xyz",
        "name": "Wanjiru",
        "gestational_age_weeks": 32,
        "language": "sw",
    })
    profile = mem.get_profile("user_xyz")
    assert profile is not None
    assert profile.name == "Wanjiru"
    assert profile.gestational_age_weeks == 32
    assert profile.language.value == "sw"


@pytest.mark.asyncio
async def test_register_is_idempotent(client):
    payload = {"clerk_user_id": "user_dup", "gestational_age_weeks": 10, "language": "en"}
    r1 = await client.post("/api/register", json=payload)
    r2 = await client.post("/api/register", json=payload)
    assert r1.status_code == 201
    assert r2.status_code == 201


@pytest.mark.asyncio
async def test_register_rejects_invalid_gestational_age(client):
    response = await client.post("/api/register", json={
        "clerk_user_id": "user_bad",
        "gestational_age_weeks": 99,
        "language": "en",
    })
    assert response.status_code == 422
