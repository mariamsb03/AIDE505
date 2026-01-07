#!/bin/bash
set -e

# Function to handle shutdown
cleanup() {
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null || true
    exit 0
}

# Set trap for cleanup
trap cleanup SIGTERM SIGINT

# Start FastAPI backend in background
cd /app/fastapi_backend
echo "Starting FastAPI backend on port 8000..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for FastAPI backend to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "FastAPI backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Warning: FastAPI backend did not start properly"
    fi
    sleep 1
done

# Start Flask frontend in foreground
cd /app/flask_frontend
echo "Starting Flask frontend on port 5000..."
export FASTAPI_URL=http://localhost:8000
exec python app.py

