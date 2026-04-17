"""Shared pytest fixtures.

Provides an AsyncClient wired to the full app for integration tests,
and resets the in-memory store between tests.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.factory import create_app
from app.services import memory as mem


@pytest.fixture
def app():
    """Return a fresh FastAPI app instance per test."""
    return create_app()


@pytest.fixture
async def client(app):
    """Return an AsyncClient wired to the app with ASGI transport."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
def reset_memory():
    """Clear all in-memory state before each test."""
    mem._profiles.clear()
    mem._history.clear()
    mem._last_active.clear()
    yield
