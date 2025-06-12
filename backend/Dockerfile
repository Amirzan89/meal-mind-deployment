# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directories for SQLite database and logs
RUN mkdir -p /app/instance /app/logs /tmp

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Create a non-root user for security and ensure /tmp is writable
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod 777 /tmp
USER appuser

# Use Railway startup script
CMD ["python", "railway_start.py"] 