FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY ./backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for SQLite database
RUN mkdir -p database

# Copy backend application code
COPY ./backend/ .

# Expose port
EXPOSE 5000

# Run the application
CMD ["bash", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 --workers 1 app:app"]