#!/bin/bash

echo "🐳 Starting Baseball Dashboard with Docker..."
echo "=========================================="

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and run the container
echo "🔨 Building Docker image..."
docker-compose up --build

echo ""
echo "🎉 Dashboard should be available at:"
echo "   👉 http://localhost:8501"
echo ""
echo "To stop the dashboard, press Ctrl+C or run:"
echo "   docker-compose down"