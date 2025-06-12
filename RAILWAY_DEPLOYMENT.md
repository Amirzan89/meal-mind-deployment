# Railway Deployment Guide for Meal-Mind

This guide explains how to deploy your Meal-Mind application on Railway.

## 🚨 SQLite Issue on Railway

**The Problem**: Railway has an **ephemeral filesystem** - files get reset on each deployment. SQLite creates `.db` files that need to persist, which causes deployment failures.

## ✅ Solutions

### Option 1: Use PostgreSQL (Recommended for Production)

1. **Add PostgreSQL to your Railway project:**
   ```bash
   # In your Railway dashboard
   Add Service > Database > PostgreSQL
   ```

2. **Railway automatically sets `DATABASE_URL`** environment variable

3. **Your app will automatically use PostgreSQL** when `DATABASE_URL` is available

### Option 2: Use SQLite with Temp Directory (Development/Testing)

Your app is now configured to fallback to SQLite in `/tmp` directory when no PostgreSQL is available.

## 🚀 Deployment Steps

### 1. Prepare Your Repository

```bash
# Make sure you're in the project root
cd Meal-Mind-main

# Your Docker files are ready:
# ✅ backend/Dockerfile (updated for Railway)
# ✅ backend/railway_start.py (Railway startup script)
# ✅ backend/config.py (Railway configuration)
```

### 2. Deploy to Railway

**Method A: Connect GitHub Repository**
1. Go to [Railway](https://railway.app)
2. Click "New Project"  
3. Choose "Deploy from GitHub repo"
4. Select your Meal-Mind repository
5. Railway will auto-detect Docker and deploy

**Method B: Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Configure Environment Variables

In Railway Dashboard, set these variables:

**Required:**
```
FLASK_ENV=railway
PORT=5000 (automatically set by Railway)
```

**Optional (for PostgreSQL):**
```
DATABASE_URL=postgresql://... (automatically set when you add PostgreSQL)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### 4. Add PostgreSQL Database (Recommended)

1. In Railway Dashboard: "Add Service" → "Database" → "PostgreSQL"
2. Railway automatically sets `DATABASE_URL`
3. Your app will use PostgreSQL instead of SQLite

## 🔧 Configuration Details

### Docker Configuration
- **Base Image**: Python 3.11-slim
- **Working Directory**: `/app`
- **Exposed Port**: 5000
- **Startup Script**: `railway_start.py`

### Environment Configurations
| Environment | Database | Use Case |
|------------|----------|----------|
| `development` | SQLite (local file) | Local development |
| `testing` | SQLite (in-memory) | Unit tests |
| `production` | PostgreSQL/SQLite fallback | General production |
| `railway` | PostgreSQL/SQLite temp | Railway deployment |

## 📊 Health Checks

Your app includes these endpoints for monitoring:
- `GET /health` - Health check
- `GET /api/test` - API test
- `GET /api/cors-test` - CORS test

## 🐛 Troubleshooting

### "Database is locked" or "No such file or directory"
- **Cause**: SQLite trying to write to read-only filesystem
- **Solution**: Add PostgreSQL service to your Railway project

### "Port already in use"  
- **Cause**: Railway automatically sets the PORT environment variable
- **Solution**: Use `railway_start.py` which reads Railway's PORT

### "Module not found"
- **Cause**: Missing dependencies
- **Solution**: Check `requirements.txt` includes all dependencies

### Logs
View logs in Railway dashboard or using CLI:
```bash
railway logs
```

## 🔒 Security Notes

- **Non-root user**: Container runs as `appuser` (UID 1000)
- **Environment variables**: Use Railway's environment variables for secrets
- **HTTPS**: Railway provides HTTPS by default

## 📈 Production Recommendations

1. **Use PostgreSQL**: Add PostgreSQL service for data persistence
2. **Environment Variables**: Set proper SECRET_KEY and JWT_SECRET_KEY
3. **Monitoring**: Monitor your Railway dashboard for performance
4. **Backups**: Set up database backups if using PostgreSQL

## 🆔 Your Current Setup

- ✅ **Docker**: Ready with `backend/Dockerfile`
- ✅ **Startup Script**: `railway_start.py` handles initialization
- ✅ **Config**: Multiple environment configurations
- ✅ **Health Checks**: Built-in endpoints for monitoring
- ✅ **Database**: Auto-fallback from PostgreSQL to SQLite

Just connect your repository to Railway and it should deploy automatically! 🚀 