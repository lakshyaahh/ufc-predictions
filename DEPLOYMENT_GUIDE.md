# UFC Predictions Web App - Complete Deployment & Feature Guide

## Features Added

### 1. Charts & Visualizations (Recharts) ✅
- **Probability Bar Charts**: Compare Red vs Blue win probabilities for each fight
- **Win Distribution Pie Chart**: Shows predicted win counts by fighter color
- **Confidence Interval Line Charts**: Track prediction confidence over time with 95% CI bounds
- Interactive tooltips and legends for all charts

**Frontend Pages Updated:**
- `pages/index.js`: Home page with upload, bar chart, and pie chart
- `pages/history.js`: History page with line chart showing confidence intervals

### 2. Calibration & Confidence Intervals ✅
- **Platt Scaling**: Applied to normalize predicted probabilities
- **Wilson Score Interval**: 95% confidence intervals computed for all predictions
- **Confidence Levels**: Visual indicators (🟢 High >65%, 🟡 Med 55-65%, 🔴 Low <55%)
- **Database**: Stores `ci_low_RedFighter`, `ci_high_RedFighter`, etc. for historical tracking

**Backend Implementation:**
- `app/utils.py`: `calibrate_probabilities()` and `compute_confidence_interval()`
- `app/models.py`: Extended DB schema with confidence interval columns

### 3. Authentication (JWT) ✅
- **User Accounts**: Register and login with username/password
- **Token-based Auth**: JWT tokens for API requests
- **User-scoped Predictions**: Each user sees only their predictions
- **Protected Endpoints**: All `/predict`, `/upload`, `/results` require valid token

**Backend Implementation:**
- `app/auth.py`: JWT token creation and verification
- `app/main.py`: Updated endpoints with `verify_token()` dependency
- `app/crud.py`: User filtering in prediction queries

**Frontend Implementation:**
- `pages/auth.js`: Login/Register page
- `pages/index.js` & `pages/history.js`: Token management via localStorage

### 4. Live UFC API Integration ✅
- **Placeholder Endpoint**: `GET /upcoming` returns UFC API integration ready
- **ESPN/UFC Stats Ready**: Structure in place for ESPN API or UFC Stats integration
- **Backend Ready**: `app/utils.py` has `fetch_upcoming_fights_espn()` and `fetch_upcoming_fights_ufcstats()`

**Notes on Integration:**
- ESPN API: Requires parsing XML/JSON for upcoming events
- UFC Stats: May require webscraping or API key
- Recommendation: Use ESPN for reliable historical data + upcoming events

### 5. Backend Deployment (Render/Heroku) ✅

#### Option A: Deploy to Render
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
6. Set environment variables:
   - `SECRET_KEY`: Your JWT secret
   - `DATABASE_URL`: PostgreSQL connection string
   - `MODEL_PATH`: Path to model file (or use Docker image with embedded model)

#### Option B: Deploy to Heroku
1. Install Heroku CLI: `brew install heroku`
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:standard-0`
5. Set env vars: `heroku config:set SECRET_KEY=xxx DATABASE_URL=xxx`
6. Deploy: `git push heroku main`

#### Files Provided:
- `Procfile`: Web server command for Heroku/Render
- `Dockerfile`: Container image for production
- `.env.example`: Environment variable template
- `download_model.py`: Script to download model at startup
- `k8s-deployment.yaml`: Kubernetes manifest (advanced)

### 6. Frontend Deployment (Vercel) ✅

#### Deploy to Vercel
1. Push code to GitHub
2. Go to https://vercel.com and click "Import Project"
3. Select your repo
4. Framework preset: Next.js
5. Environment variables:
   - `NEXT_PUBLIC_API_URL`: Backend URL (e.g., `https://your-api.render.com`)
6. Click "Deploy"
7. Vercel auto-deploys on every push to `main`

#### Files Provided:
- `vercel.json`: Vercel configuration
- `next.config.js`: Next.js configuration with API URL env var
- `.env.example`: Environment variable template

---

## Quick Start (Local Development)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:3000
```

### Login
1. Go to http://localhost:3000/auth
2. Register a test account (e.g., `testuser` / `password123`)
3. Token saved to localStorage automatically
4. Upload CSV or manage predictions

---

## API Endpoints

### Public
- `GET /health` — Health check

### Auth
- `POST /auth/login` — `{username, password}` → `{access_token, token_type}`
- `POST /auth/register` — `{username, password}` → `{access_token, ...}`

### Protected (Requires Bearer Token)
- `POST /predict` — Send `{fights: [...]}` → predictions with confidence intervals
- `POST /upload` — Upload CSV → predictions with confidence intervals
- `GET /results` — Fetch user's predictions
- `GET /upcoming` — Placeholder for live UFC fights (ESPN/UFC Stats API)

---

## Production Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Use PostgreSQL instead of SQLite for database
- [ ] Enable HTTPS on backend and frontend
- [ ] Set up rate limiting (e.g., Redis)
- [ ] Configure CORS properly (allow only your frontend domain)
- [ ] Add password hashing (use `bcrypt` or `passlib`)
- [ ] Implement email verification for registration
- [ ] Set up database backups
- [ ] Monitor API health and logs
- [ ] Cache model in memory on server startup
- [ ] Implement caching for predictions (Redis)

---

## Next Steps & Improvements

1. **User Dashboard**: Stats, accuracy tracking, personalized insights
2. **Fight Notifications**: Email/SMS when fights involving favorites are scheduled
3. **Advanced Features**:
   - Model versioning and A/B testing
   - Hyperparameter tuning via AutoML
   - Feature importance visualization
4. **Mobile App**: React Native for iOS/Android
5. **Social**: Share predictions, compare accuracy with friends
6. **Monetization**: Premium features, API access for third parties

---

## Troubleshooting

### Model Version Mismatch
If you see `InconsistentVersionWarning`, retrain with matching scikit-learn version.

### JWT Errors
- Check `SECRET_KEY` is set in `.env`
- Token expires after `TOKEN_EXPIRE_DAYS` (default 30)
- Refresh token by re-logging in

### CORS Issues
- Frontend must match `NEXT_PUBLIC_API_URL`
- Backend must allow frontend origin in `CORSMiddleware`

### Database Errors
- Use absolute paths for SQLite or set `DATABASE_URL` for PostgreSQL
- Run migrations if needed (SQLAlchemy handles auto-creation)

---

## Support & Questions
See `backend/README.md` and `frontend/README.md` for more details.
