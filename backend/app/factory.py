"""FastAPI application factory.

create_app() is the single entry point for constructing the application.
Called once at module load for the uvicorn entrypoint, and once per test
run to get an isolated app instance.

Pattern adapted from the agentic course goldenberri project.
"""

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, health, register

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage startup and shutdown tasks.

    Currently a no-op placeholder — the in-memory store needs no
    initialisation. Extend here when adding a database in Phase 2.

    Args:
        app: The FastAPI application instance.

    Yields:
        None while the application is running.
    """
    logger.info("Zeya Antenatal API starting up")
    yield
    logger.info("Zeya Antenatal API shut down")


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application.

    Registers CORS middleware, mounts all routers under /api, and wires
    the lifespan context manager.

    Returns:
        A fully configured FastAPI instance.
    """
    app = FastAPI(
        title="Zeya Antenatal API",
        version="0.1.0",
        lifespan=lifespan,
    )

    cors_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    cors_origins = [o.strip() for o in cors_origins_raw.split(",")]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(register.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")

    return app
