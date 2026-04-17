# Multi-stage build — production image for AWS App Runner
# Build for linux/amd64 to ensure compatibility on Apple Silicon:
#   docker build --platform linux/amd64 -t zeya-antenatal-api .

# ---------------------------------------------------------------------------
# Stage 1: install dependencies
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for layer caching
COPY pyproject.toml .
COPY .python-version .

# Install dependencies into /app/.venv (no dev deps)
RUN uv sync --no-dev

# ---------------------------------------------------------------------------
# Stage 2: lean production image
# ---------------------------------------------------------------------------
FROM python:3.12-slim

WORKDIR /app

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy venv and source from builder
COPY --from=builder /app/.venv /app/.venv
COPY app/ ./app/

# Make venv binaries available
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
