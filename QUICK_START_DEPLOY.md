# ⚡ QUICK REFERENCE CARD

## 📋 What You Have

✅ **Full-stack UFC prediction web app**  
✅ **Machine learning model** (Random Forest, 57% accuracy)  
✅ **User authentication** (JWT)  
✅ **Database ready** (PostgreSQL)  
✅ **Charts & visualizations** (Recharts)  
✅ **Production configs** (Docker, Procfile)  
✅ **Deployment scripts** (Automated setup)  

---

## 🚀 DEPLOYMENT IN 3 STEPS

### 1️⃣ Initialize Git
```bash
cd "c:\Users\Lakshya\Desktop\UFC PREDICTIONS"
.\setup_github.bat
```
Then push to GitHub (follow script instructions)

### 2️⃣ Deploy Backend
- Go to https://render.com
- Connect GitHub repo
- Deploy as Web Service (use Procfile)
- Add PostgreSQL database
- Copy backend URL (e.g., `https://api.onrender.com`)

### 3️⃣ Deploy Frontend
- Go to https://vercel.com
- Import `ufc-predictions` repo
- Root directory: `frontend`
- Set env var: `NEXT_PUBLIC_API_URL=<your-backend-url>`
- Deploy!

---

## 📞 Important Links

| Service | URL |
|---------|-----|
| GitHub | https://github.com/new |
| Render | https://render.com |
| Vercel | https://vercel.com |
| Your Frontend | Will be given by Vercel |
| Your Backend | Will be given by Render |
| API Docs | `{backend-url}/docs` |

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app + all endpoints |
| `frontend/pages/index.js` | Home page + predictions |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node.js dependencies |
| `Procfile` | Render startup command |
| `Dockerfile` | Container image |
| `FINAL_DEPLOYMENT_GUIDE.md` | Step-by-step deployment |

---

## 🧪 Test Endpoints (After Deployment)

```bash
# Check API is live
curl https://your-backend.onrender.com/docs

# Register
curl -X POST https://your-backend.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"test@test.com","password":"pass"}'

# Get token (login)
curl -X POST https://your-backend.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# Make prediction (use token from login)
curl -X POST https://your-backend.onrender.com/predict \
  -H "Authorization: Bearer TOKEN_HERE" \
  -d '{"red_fighter":"Fighter1","blue_fighter":"Fighter2",...}'
```

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `Cannot connect to backend` | Check `NEXT_PUBLIC_API_URL` in Vercel |
| `500 error from backend` | Check Render logs, verify `DATABASE_URL` |
| `Port already in use` | Render handles ports automatically |
| `Model not found` | Model file is committed to repo |

---

## 💾 Environment Variables

### Backend (.env.production)
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
TOKEN_EXPIRE_DAYS=30
MODEL_PATH=./models/ufc_prediction_model.pkl
```

### Frontend (.env.production)
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

---

## 📊 What Users See

1. **Landing Page**: Upload fight data or browse features
2. **Auth Page**: Register/Login
3. **Predict Page**: Upload CSV, see predictions with charts
4. **History Page**: View past predictions, accuracy trends
5. **Premium Page**: Upgrade option (optional)

---

## 🎯 Your Live Links (After Deployment)

Frontend: `https://[your-vercel-project].vercel.app`  
Backend: `https://ufc-predictions-api.onrender.com`  
API Docs: `https://ufc-predictions-api.onrender.com/docs`  

---

## ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set
- [ ] Tested registration
- [ ] Tested prediction
- [ ] Charts display correctly
- [ ] Shared link with friends

---

**Status: 🟢 READY TO LAUNCH**

Follow `FINAL_DEPLOYMENT_GUIDE.md` for detailed step-by-step instructions.
