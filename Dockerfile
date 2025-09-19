# Use a small Python base
FROM python:3.11-slim

# Workdir inside the container
WORKDIR /app

# System deps needed by psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps first (leverages Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose API port
EXPOSE 8000

# Container will be started by docker-compose with a command, so no CMD here
