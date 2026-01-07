FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install FastAPI backend dependencies
COPY fastapi_backend/requirements.txt /app/fastapi_backend/requirements.txt
RUN pip install --no-cache-dir -r /app/fastapi_backend/requirements.txt

# Copy and install Flask frontend dependencies
COPY flask_frontend/requirements.txt /app/flask_frontend/requirements.txt
RUN pip install --no-cache-dir -r /app/flask_frontend/requirements.txt

# Copy FastAPI backend application
COPY fastapi_backend/ /app/fastapi_backend/

# Copy Flask frontend application
COPY flask_frontend/ /app/flask_frontend/

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose only the frontend port
EXPOSE 5000

# Run startup script
CMD ["/app/start.sh"]

