#!/bin/bash

echo "🚀 Deploying ParlayJaye Dashboard to Production..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and fill in your values."
    echo "cp .env.example .env"
    exit 1
fi

# Load environment variables
source .env

# Verify required environment variables
required_vars=("THE_ODDS_API_KEY" "DB_PASSWORD" "REDIS_PASSWORD")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set in .env file"
        exit 1
    fi
done

# Create required directories
mkdir -p data logs backups ssl

# Stop any existing production containers
echo "🛑 Stopping existing production containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start production containers
echo "🔨 Building production containers..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo "🚀 Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check service health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Setup log rotation
echo "📋 Setting up log rotation..."
cat > logrotate.conf << 'EOF'
/var/log/parlayjaye/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF

echo ""
echo "✅ Production dashboard deployed successfully!"
echo "🌐 Dashboard available at: http://your-domain.com"
echo "🔒 HTTPS available at: https://your-domain.com (configure SSL certificates)"
echo ""
echo "📋 Production management commands:"
echo "  View logs:           docker-compose -f docker-compose.prod.yml logs -f"
echo "  Stop services:       docker-compose -f docker-compose.prod.yml down"
echo "  Restart services:    docker-compose -f docker-compose.prod.yml restart"
echo "  Update and restart:  ./deploy-prod.sh"
echo "  Database backup:     docker exec parlayjaye-db-prod pg_dump -U parlayjaye baseball_analytics > backups/backup_$(date +%Y%m%d_%H%M%S).sql"
echo ""
echo "🔍 Monitor status: docker-compose -f docker-compose.prod.yml ps"
echo "📊 Resource usage: docker stats"
echo ""
echo "⚠️  Important: Configure SSL certificates in ./ssl/ directory for HTTPS"
echo "⚠️  Update nginx.conf with your actual domain name"