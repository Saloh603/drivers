FROM python:3.11-slim

# Work directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY ../requirements.txt .

# Install deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY ../bot ./bot

# Run bot
CMD ["python", "-m", "bot.main"]
