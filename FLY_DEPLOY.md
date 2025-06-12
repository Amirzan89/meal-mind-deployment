# 🚀 Deploy to Fly.io

Super simple guide to deploy your Python backend to Fly.io cloud.

## 1. Install Fly CLI

### Windows (PowerShell):
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Mac/Linux:
```bash
curl -L https://fly.io/install.sh | sh
```

## 2. Login to Fly.io

```bash
fly auth login
```

## 3. Deploy Your App

```bash
cd backend
fly launch --no-deploy
```

When asked:
- **App name**: `meal-mind-backend` (or whatever you want)
- **Region**: Choose closest to you
- **Database**: Skip (we're using SQLite)

## 4. Create Volume for SQLite

```bash
fly volumes create sqlite_data --region sjc --size 1
```

## 5. Deploy!

```bash
fly deploy
```

That's it! 🎉

## Your App URLs

After deployment:
- **API**: `https://meal-mind-backend.fly.dev`
- **Health**: `https://meal-mind-backend.fly.dev/health`

## Useful Commands

```bash
# View logs
fly logs

# Check status
fly status

# Open app in browser
fly open

# SSH into container
fly ssh console

# Scale up/down
fly scale count 2
```

## Cost

- **Free tier**: 3 shared-cpu-1x 256mb VMs
- **Your setup**: ~$1.94/month (1 VM + 1GB storage)

## Troubleshooting

**Build fails?**
```bash
fly logs
```

**Need to update?**
```bash
fly deploy
```

**Delete app?**
```bash
fly apps destroy meal-mind-backend
``` 