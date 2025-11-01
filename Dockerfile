# Stage 1: Builder
FROM python:3.13 AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies directly to system Python (NO .venv!)
RUN uv pip install --system -r pyproject.toml

# Copy the application code
COPY . /app

# Stage 2: Production
FROM python:3.13

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose the port
EXPOSE 8003

# Run entrypoint
ENTRYPOINT ["sh", "./entrypoint.sh"]

# Default CMD for Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8003", "core.asgi:application"]