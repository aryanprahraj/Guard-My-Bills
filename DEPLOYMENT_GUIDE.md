# Deployment Troubleshooting Guide

## Issue: "Can't reach backend" - Intermittent Failures

### Common Causes and Solutions

#### 1. **Free Tier Dyno/Instance Spinning Down**
- **Problem**: Render free tier spins down after 15 minutes of inactivity
- **Solution**: Upgrade to Starter tier ($7/month) or use a ping service to keep it alive
- **Quick Fix**: 
  ```bash
  # Use a service like UptimeRobot to ping your backend every 5 minutes
  # URL: https://guard-my-bills.onrender.com/health
  ```

#### 2. **Memory Issues During Startup**
- **Problem**: Free tier has only 512MB RAM; model training can exceed this
- **Solution**: 
  - Check Render logs: `render logs <service-id>`
  - Pre-train model locally and commit `model/isolation_forest.pkl` to repo
  - Or use `requirements-prod.txt` with pinned versions for stability

#### 3. **Cold Start Timeout**
- **Problem**: First request after spin-up times out (model loading + training)
- **Solution**: 
  - Increase health check timeout in Render dashboard
  - Pre-warm the model before deployment
  - Add logging to monitor startup time

#### 4. **CORS or Environment Variable Issues**
- **Problem**: Frontend uses wrong API URL in production
- **Solution**: 
  - Verify `NEXT_PUBLIC_API_URL=https://guard-my-bills.onrender.com` in Vercel
  - Check browser DevTools → Application → Environment Variables
  - Test endpoint: `curl https://guard-my-bills.onrender.com/health`

#### 5. **Dependency Conflicts**
- **Problem**: Requirements without versions cause conflicts in build
- **Solution**:
  ```bash
  # Use production requirements with pinned versions
  pip install -r requirements-prod.txt
  ```

### How to Deploy

#### Backend (Render)
1. Go to https://dashboard.render.com
2. Create new service from Git repo
3. Set build command: `cd backend && pip install -r requirements-prod.txt`
4. Set start command: `cd backend && bash start.sh`
5. Add environment variables:
   - `PYTHONUNBUFFERED=true`
   - `PORT=10000`

#### Frontend (Vercel)
1. Go to https://vercel.com
2. Import repository
3. Set root directory: `frontend`
4. Add environment variable: `NEXT_PUBLIC_API_URL=https://guard-my-bills.onrender.com`
5. Deploy

### Debugging Steps

1. **Check backend health**
   ```bash
   curl https://guard-my-bills.onrender.com/health
   ```
   Expected: `{"status":"ok","message":"Backend is running"}`

2. **Check Render logs**
   - Render Dashboard → Your Service → Logs
   - Look for startup errors or memory warnings

3. **Check frontend logs**
   - Browser DevTools → Console
   - Look for network errors and API URL being used

4. **Test API directly**
   ```bash
   # Get API docs
   https://guard-my-bills.onrender.com/docs
   
   # Test health
   curl https://guard-my-bills.onrender.com/health/ping
   ```

5. **Check database/file permissions**
   ```bash
   # Verify model can be written
   ls -la backend/model/
   ```

### Performance Tips

- **Enable caching**: Add cache headers in FastAPI responses
- **Use CDN**: Vercel CDN is free for frontend
- **Monitor uptime**: Use UptimeRobot (free tier)
- **Set up alerts**: Configure Render notifications for crashes

### Quick Checklist

- [ ] Backend build command uses `requirements-prod.txt`
- [ ] Environment variables set correctly
- [ ] Health check endpoint is `/health/ping`
- [ ] Frontend `NEXT_PUBLIC_API_URL` is correct
- [ ] Model directory exists and is writable
- [ ] Logs show clean startup without errors
- [ ] CORS is enabled in FastAPI
- [ ] Tests pass locally before deploying
