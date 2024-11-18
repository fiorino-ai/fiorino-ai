FROM python:3.10.11-slim-bullseye

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create platform directory and download frontend
RUN mkdir -p /platform
RUN cd /platform && \
    curl -L https://github.com/fiorino-ai/fiorino-webapp/releases/download/fiorino-webapp-stable/release.zip -o release.zip && \
    unzip release.zip && \
    rm release.zip

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port
EXPOSE 8000

# Start command
CMD ["/bin/bash", "-c", "python run.py"]