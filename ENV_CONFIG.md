# Environment Configuration

## Frontend API URL Configuration

The frontend uses environment variables to determine the backend API URL.

### Local Development
Create `.env.local` in the `frontend/` directory:
```
NEXT_PUBLIC_API_URL=http://localhost:8002
```

### Production Deployment
The `.env.production` file uses:
```
NEXT_PUBLIC_API_URL=https://guard-my-bills.onrender.com
```

## Running Locally

### Backend
```bash
cd backend
PYTHONPATH=/path/to/backend python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

### Frontend
```bash
cd frontend
npm install  # First time only
npm run dev
```

Visit `http://localhost:3000` to access the app.

## Troubleshooting: "Can't reach backend"

If you see "Can't reach backend" error:

1. **Check backend is running:**
   ```bash
   curl http://localhost:8002/health
   ```
   Should return: `{"status":"ok","message":"Backend is running"}`

2. **Verify NEXT_PUBLIC_API_URL environment variable:**
   - Development: Should be `http://localhost:8002`
   - Production: Should be `https://guard-my-bills.onrender.com`

3. **Check frontend logs:**
   - Open browser DevTools → Console
   - Look for network errors showing the API URL being called

4. **Restart servers:**
   - Kill frontend and backend processes
   - Clear Next.js cache: `rm -rf frontend/.next`
   - Restart both servers

## API Health Check

Both environments now support a health check endpoint:
```bash
curl ${API_BASE}/health
```

The frontend automatically checks backend health before uploading statements.
