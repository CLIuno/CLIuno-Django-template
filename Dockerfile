FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

# Remove .env if it exists and use production env
RUN rm -f .env && cp .env.production .env

# Run migrations and collect static
RUN uv run python manage.py collectstatic --noinput 2>/dev/null || true

# Expose port
EXPOSE 8000

# Start the server
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
