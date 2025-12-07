# Deploy Guard My Bills - Step by Step

## Problem Summary
Your deployment was working intermittently because of:
1. Render free tier memory constraints during model training
2. Missing/loose dependency versions causing build failures
3. Lack of proper startup logging and health checks
4. No request timeout handling

## Changes Made

### Backend Fixes
- ✅ `requirements-prod.txt` - Pinned versions for stability
- ✅ `runtime.txt` - Specified Python 3.11.11
- ✅ `start.sh` - Startup script with logging
- ✅ `render.yaml` - Updated to use production requirements
- ✅ `main.py` - Added request timeout tracking and startup events
- ✅ `routers/health.py` - Added `/health` endpoint

### Frontend Fixes
- ✅ `.env.local` - Development API URL
- ✅ `.env.production` - Production API URL
- ✅ `services/api.ts` - Backend health check before upload

## Deployment Steps

### Step 1: Commit Changes
```bash
git add -A
git commit -m "fix: Improve deployment stability and add health checks"
git push origin master
```

### Step 2: Deploy Backend (Render)

1. Go to https://dashboard.render.com
2. Click "New Service" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `guard-my-bills-backend`
   - **Environment**: `Python`
   - **Build Command**: `cd backend && pip install -r requirements-prod.txt`
   - **Start Command**: `cd backend && bash start.sh`
   - **Plan**: Free (or Starter for production)
   
5. Add Environment Variables:
   ```
   PORT=10000
   PYTHONUNBUFFERED=true
   ```

6. Click "Create Web Service"

### Step 3: Deploy Frontend (Vercel)

1. Go to https://vercel.com/new
2. Import your repository
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com
   ```

5. Click "Deploy"

### Step 4: Verify Deployment

Test backend:
```bash
curl https://your-service.onrender.com/health
# Should return: {"status":"ok","message":"Backend is running"}
```

Test frontend:
```bash
# Visit your Vercel deployment URL
# Check browser console for any API errors
# Try uploading a CSV file
```

## Monitoring & Maintenance

### Keep Backend Awake (Free Tier)
Free Render instances spin down after 15 minutes of inactivity. Use UptimeRobot (free):

1. Go to https://uptimerobot.com (free account)
2. Create new monitor:
   - URL: `https://your-service.onrender.com/health`
   - Interval: 5 minutes
   - Type: HTTP(s)

### Check Logs
- **Render**: Dashboard → Service → Logs
- **Vercel**: Dashboard → Deployments → Logs
- **Browser**: DevTools → Console

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "502 Bad Gateway" | Check Render logs for startup errors |
| "Backend unreachable" | Verify `NEXT_PUBLIC_API_URL` environment variable |
| "Timeout during upload" | Cold start - wait 30s and retry, or upgrade tier |
| "Model file not found" | Pre-train model locally and commit, or wait for auto-training |

## Performance Tips

1. **Pre-train the model** (optional but recommended):
   ```bash
   cd backend
   python -c "from core.ml_model import fraud_model; print('Model ready')"
   # Commit the model file to git
   ```

2. **Upgrade from free tier**:
   - Render Starter: $7/month (better stability)
   - Vercel Pro: $20/month (optional, free should work)

3. **Set up alerts**:
   - Render: Enable notifications in dashboard
   - Vercel: Enable deployment notifications

## Next Steps

After deployment is confirmed working:

1. Run end-to-end tests on production
2. Share deployment link and gather user feedback
3. Set up monitoring for errors
4. Consider paid tier if handling significant traffic
