FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
# Use --no-cache-dir and a cache-busting argument to force reinstallation
ARG CACHE_BUST=1
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY ./backend/ .

# Create directory for SQLite database
RUN mkdir -p database

# Expose port
EXPOSE 5000

# Run the application with gunicorn
CMD ["bash", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 --workers 4 app:app"]