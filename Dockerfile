FROM python:3.10-slim

WORKDIR /app

# Install system utilities and git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and source code
COPY pyproject.toml setup.py /app/
COPY nexus_agent/ /app/nexus_agent/

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Expose Web Mission Control Port
EXPOSE 8000

# Default entrypoint runs the Cyberpunk Web Dashboard
CMD ["nexus-agent", "web", "--host", "0.0.0.0", "--port", "8000"]
