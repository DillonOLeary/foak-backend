# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install git for private repository access
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Create a non-root user FIRST (before copying files)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create necessary directories with correct ownership
RUN mkdir -p /app/storage /app/logs /app/cache && \
    chown appuser:appuser /app/storage /app/logs /app/cache

# Copy dependency files
COPY uv.lock pyproject.toml ./

# Install the project's dependencies using the lockfile and settings
RUN uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Copy as root user (default)
COPY . /app

# Only chown the source code (not .venv)
RUN chown -R appuser:appuser /app/src /app/scripts /app/pyproject.toml || true

# Install the project
RUN uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Run the FastAPI application by default
# Uses `fastapi dev` to enable hot-reloading when the `watch` sync occurs
# Uses `--host 0.0.0.0` to allow access from outside the container
CMD ["fastapi", "dev", "--host", "0.0.0.0", "src/backend/main.py"]