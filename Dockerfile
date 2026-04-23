FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen

# Put the uv-managed venv on PATH so `dagster` is resolvable directly.
# The code server still launches via `uv run dagster ...` below; this only
# matters for run workers where the launcher invokes `dagster` without a
# wrapper (ACA Jobs, K8s Jobs, ECS tasks).
ENV PATH="/app/.venv/bin:${PATH}"

# Set the entrypoint for Dagster
ENV DAGSTER_HOME=/app

# Expose port for Dagster gRPC server
EXPOSE 4000

# Run Dagster code server
CMD ["uv", "run", "dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "azure_demo.definitions"]
