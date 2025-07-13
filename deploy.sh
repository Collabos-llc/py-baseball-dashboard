#!/bin/bash

echo "🚀 Deploying ParlayJaye Baseball Dashboard..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and fill in your values."
    echo "cp .env.example .env"
    exit 1
fi

# Load environment variables
source .env

# Create required directories
mkdir -p data logs backups

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🔨 Building containers..."
docker-compose build --no-cache

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

echo ""
echo "✅ Dashboard deployed successfully!"
echo "📊 Dashboard available at: http://localhost:8501"
echo "🗄️  Redis available at: localhost:6379"
echo "🐘 PostgreSQL available at: localhost:5432"
echo ""
echo "📋 Useful commands:"
echo "  View logs:           docker-compose logs -f"
echo "  Stop services:       docker-compose down"
echo "  Restart services:    docker-compose restart"
echo "  Update and restart:  ./deploy.sh"
echo ""
echo "🔍 Check status: docker-compose ps"