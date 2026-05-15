#!/bin/bash
set -e

echo "=== SCAMEATER Deployment ==="

# Check .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Copy .env.example to .env and fill in values."
    exit 1
fi

# Load environment
source .env

echo "[1/5] Building Docker images..."
docker compose build

echo "[2/5] Starting infrastructure services..."
docker compose up -d db redis seaweedfs

echo "[3/5] Waiting for database to be ready..."
sleep 10

echo "[4/5] Starting all services..."
docker compose up -d

echo "[5/5] Checking status..."
docker compose ps

echo ""
echo "=== Deployment complete ==="
echo "Dashboard: http://localhost:8501"
echo "API: http://localhost:8000"
echo "Langfuse: http://localhost:3000"