FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements/base.txt requirements/base.txt
RUN pip install --no-cache-dir -r requirements/base.txt

# Copy application code
COPY . .

# Create media directory for temp files
RUN mkdir -p media/tts_temp media/mock_tts

# Expose port
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "lughabridge.asgi:application"]
