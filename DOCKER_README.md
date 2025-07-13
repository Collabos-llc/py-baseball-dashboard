# 🐳 ParlayJaye Baseball Dashboard - Docker Setup

Complete containerized deployment for the advanced baseball betting analytics dashboard.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Git (for cloning the repository)

### 1. Environment Setup
```bash
# Copy and configure environment file
cp .env.example .env

# Edit .env with your API keys and passwords
nano .env
```

### 2. Development Deployment
```bash
# Make scripts executable
chmod +x deploy.sh deploy-prod.sh

# Deploy development environment
./deploy.sh
```

**Dashboard will be available at: http://localhost:8501**

### 3. Production Deployment
```bash
# Configure production environment
./deploy-prod.sh
```

## 📋 Services Overview

### 🎯 baseball-dashboard
- **Port**: 8501
- **Purpose**: Main Streamlit application
- **Features**: All 6 advanced analysis tabs with betting insights

### 🗄️ postgres
- **Port**: 5432
- **Purpose**: Data storage for players, games, and insights
- **Database**: `baseball_analytics`
- **User**: `parlayjaye`

### ⚡ redis
- **Port**: 6379
- **Purpose**: Caching PyBaseball data and analysis results
- **Features**: Persistent storage with AOF

### 🌐 nginx (Production Only)
- **Ports**: 80, 443
- **Purpose**: Reverse proxy and SSL termination
- **Features**: Load balancing and security headers

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
THE_ODDS_API_KEY=your_odds_api_key_here
DB_PASSWORD=your_secure_password_here

# Optional for production
DISCORD_WEBHOOK_URL=your_discord_webhook_url
REDIS_PASSWORD=your_redis_password
```

### Database Schema
- **players**: Player information and metadata
- **games**: Game details with weather data
- **pitches**: Detailed Statcast pitch data
- **betting_insights**: Analysis results and recommendations
- **umpire_analysis**: Strike zone bias data
- **player_profiles**: Aggregated player metrics

## 📊 Features by Tab

### 🚀 Exit Velocity Analysis
- Sweet spot detection (95+ mph, 25-35°)
- Home run probability zones
- Betting edge alerts

### 🎯 Barrel Rate Trends
- Expected vs actual home runs
- Regression analysis
- Value betting opportunities

### ⚖️ Umpire Strike Zone Analysis
- Zone-by-zone accuracy
- Bias detection for betting edges
- Strike rate tendencies

### 🌤️ Weather Impact Analysis
- Temperature effects on distance
- Wind direction impact
- Environmental betting alerts

### 😴 Pitcher Fatigue Analysis
- Times through order tracking
- Exit velocity progression
- 3rd time through alerts

### 👤 Player Profile Analysis
- Radar charts for power metrics
- Launch angle distributions
- Complete scouting reports

## 🛠️ Management Commands

### Development
```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Rebuild and restart
./deploy.sh
```

### Production
```bash
# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Monitor resource usage
docker stats

# Database backup
docker exec parlayjaye-db-prod pg_dump -U parlayjaye baseball_analytics > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Scale dashboard (multiple instances)
docker-compose -f docker-compose.prod.yml up -d --scale baseball-dashboard=3
```

## 🔒 Security Features

### Production Security
- Password-protected Redis
- PostgreSQL with secure credentials
- Nginx reverse proxy
- SSL/TLS support (configure certificates)
- Resource limits on containers

### Data Security
- Encrypted environment variables
- Isolated network (parlayjaye-network)
- Volume-based data persistence
- Regular backup capabilities

## 📈 Performance Optimization

### Caching Strategy
- Redis caching for PyBaseball API calls
- Streamlit @st.cache_data decorators
- PostgreSQL query optimization with indexes

### Resource Limits (Production)
- Dashboard: 2GB RAM, 1 CPU
- Database connection pooling
- Nginx gzip compression

## 🐛 Troubleshooting

### Common Issues

**Dashboard won't start:**
```bash
# Check logs
docker-compose logs baseball-dashboard

# Common fix: clear cache
docker-compose down -v
docker-compose up -d
```

**Database connection issues:**
```bash
# Check database status
docker-compose ps postgres

# Reset database
docker-compose down
docker volume rm py-baseball_postgres_data
docker-compose up -d
```

**Memory issues:**
```bash
# Check resource usage
docker stats

# Increase memory limits in docker-compose.yml
```

### Health Checks
```bash
# Dashboard health
curl http://localhost:8501/_stcore/health

# Database connection
docker exec parlayjaye-db psql -U parlayjaye -d baseball_analytics -c "SELECT 1;"

# Redis connection
docker exec parlayjaye-redis redis-cli ping
```

## 📦 Data Volumes

### Persistent Data
- `postgres_data`: Database storage
- `redis_data`: Cache persistence
- `./data`: PyBaseball cache files
- `./logs`: Application logs
- `./backups`: Database backups

### Development vs Production
- **Development**: Direct volume mounts for live editing
- **Production**: Named volumes for better performance and security

## 🔄 Updates & Maintenance

### Regular Updates
```bash
# Pull latest images
docker-compose pull

# Rebuild with latest code
./deploy.sh

# Database migrations (if needed)
docker exec parlayjaye-db psql -U parlayjaye -d baseball_analytics -f /app/migrations/latest.sql
```

### Monitoring
- Container health checks every 30 seconds
- Automatic restart on failure
- Log rotation for production
- Disk space monitoring recommended

## 📞 Support

### Useful Links
- **PyBaseball Documentation**: https://github.com/jldbc/pybaseball
- **Streamlit Docs**: https://docs.streamlit.io/
- **Docker Compose Reference**: https://docs.docker.com/compose/

### Log Locations
- Application logs: `./logs/`
- Container logs: `docker-compose logs [service]`
- Database logs: `docker-compose logs postgres`

## 🎯 Next Steps

1. **Configure SSL certificates** for production HTTPS
2. **Set up monitoring** with Prometheus/Grafana
3. **Implement automated backups** with cron jobs
4. **Add more data sources** (weather APIs, odds APIs)
5. **Scale horizontally** with load balancers

---

**🏆 Your advanced baseball betting analytics platform is now containerized and ready for production deployment!**