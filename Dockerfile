# Use Python 3.13 slim image as base for smaller size
FROM python:3.13-slim

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY pyproject.toml ./

# Install Python dependencies using pip
RUN pip install --no-cache-dir -e .

# Copy source code
COPY server.py tidio_client.py ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# The MCP server uses STDIO transport, so no port exposure needed
# CMD will be overridden by docker run arguments for MCP usage
CMD ["python", "server.py"]
