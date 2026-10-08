FROM docker.io/debian:stable-slim AS base

# Ensure apt is in non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update the system
RUN apt-get update
RUN apt-get upgrade -y

# Install essential tooling 
RUN apt-get install -y \
    python3-minimal \
    python3-venv 

FROM base AS dev 

# Install development tools
RUN apt-get install -y \
    curl \
    ripgrep

# Install Python development tools
RUN apt-get install python3-dev -y > /dev/null
# Pip for Python package management
RUN apt-get install python3-pip -y > /dev/null
# Ensure 'python' command points to 'python3'
RUN apt-get install python-is-python3 -y > /dev/null
# Pipx for installing Python packages
RUN apt-get install pipx -y > /dev/null
# UV (Python package and project manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin/ sh > /dev/null
# MISE ( Task runner that integrates nicely with UV )
RUN curl https://mise.run | MISE_INSTALL_PATH=/usr/local/bin/mise sh

FROM dev AS builder 

WORKDIR /src 

# Copy the source code into the container
COPY pyproject.toml README.md ./
COPY src/ ./src

# Build the project using UV 
RUN uv sync --no-dev
RUN uv build -o dist

# Install the built wheel to venv  
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir dist/*.whl

FROM base AS prod 

# Add the built wheel from the builder stage to the prod stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Remove apt cache to minimize image size
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

