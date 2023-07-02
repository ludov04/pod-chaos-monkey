# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy and install dependencies
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-root

# Production stage
FROM python:3.11-alpine AS production

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy dependencies
COPY --from=builder /app/.venv /app/.venv
COPY pod_chaos_monkey ./pod_chaos_monkey

ENTRYPOINT ["python", "pod_chaos_monkey"]