# Docker Deployment Guide

This guide explains how to deploy your Meal Mind Python backend with SQLite database using Docker.

## Prerequisites

1. **Docker Desktop** (for Windows/Mac) or **Docker Engine** (for Linux)
   - Download from: https://www.docker.com/products/docker-desktop/
   - Make sure Docker Compose is included (it's bundled with Docker Desktop)

2. **Git** (if cloning the repository)

## Quick Start

### Option 1: Using the Deploy Script (Recommended)

**For Windows:**
```cmd
deploy.bat
```

**For Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Docker Commands

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build -d
```

2. **Check if the service is running:**
```bash
curl http://localhost:5000/health
```

## What's Included

### Files Created
- `backend/Dockerfile` - Docker image configuration for Python Flask backend
- `backend/.dockerignore` - Excludes unnecessary files from Docker build
- `docker-compose.yml` - Orchestrates the backend service
- `deploy.sh` / `deploy.bat` - Automated deployment scripts

### Features
- ✅ Python 3.11 slim base image
- ✅ SQLite database with persistent storage
- ✅ Health check endpoint (`/health`)
- ✅ Non-root user for security
- ✅ Volume mounting for database persistence
- ✅ Auto-restart policy
- ✅ Proper dependency caching

## Service Endpoints

Once deployed, your backend will be available at:

- **Main API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Test**: http://localhost:5000/api/test
- **CORS Test**: http://localhost:5000/api/cors-test

## Docker Commands

### View logs:
```bash
docker-compose logs -f backend
```

### Stop the service:
```bash
docker-compose down
```

### Rebuild and restart:
```bash
docker-compose up --build -d
```

### Access container shell:
```bash
docker-compose exec backend bash
```

### Check container status:
```bash
docker-compose ps
```

## Database Persistence

The SQLite database is stored in a Docker volume named `sqlite_data` which ensures data persistence across container restarts. The database files are mounted to `/app/instance` inside the container.

## Environment Variables

The following environment variables are set in the container:
- `FLASK_ENV=production`
- `FLASK_APP=run.py`
- `PYTHONPATH=/app`

## Troubleshooting

### Container won't start
1. Check logs: `docker-compose logs backend`
2. Verify Docker is running: `docker --version`
3. Check port availability: `netstat -an | findstr :5000`

### Database issues
1. SQLite database is automatically created on first run
2. Database files are in the `sqlite_data` volume
3. To reset database: `docker-compose down -v` (⚠️ This deletes all data)

### Port conflicts
If port 5000 is already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "8000:5000"  # Use port 8000 instead
```

## Production Considerations

For production deployment, consider:

1. **Use environment files** for sensitive configuration
2. **Add SSL/TLS** with a reverse proxy (nginx, Traefik)
3. **Use PostgreSQL** instead of SQLite for better performance
4. **Add monitoring** and logging aggregation
5. **Implement backup strategy** for the database
6. **Use Docker secrets** for sensitive data

## Building Custom Images

To build only the backend image:
```bash
cd backend
docker build -t meal-mind-backend .
```

To run the custom image:
```bash
docker run -p 5000:5000 -v sqlite_data:/app/instance meal-mind-backend
``` 