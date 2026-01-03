# 🚀 Quick Deployment Guide - 30 Minutes to Live

## **Option A: Deploy Backend to Render (RECOMMENDED)**

### Step 1: Push Code to GitHub
```bash
cd c:\Users\Lakshya\Desktop\UFC PREDICTIONS
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ufc-predictions.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Fill in:
   - **Name**: `ufc-predictions-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: 
     ```
     gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
6. Click "Create Web Service"

### Step 3: Add Environment Variables to Render
In Render dashboard, go to your service → Environment:
```
DATABASE_URL=postgresql://user:password@host:5432/ufc_predictions
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
TOKEN_EXPIRE_DAYS=30
MODEL_PATH=./models/ufc_prediction_model.pkl
```

> **Note**: Render will give you a free PostgreSQL database addon. Add it first!

### Step 4: Copy Your Backend URL
Once deployed, Render shows you the URL (e.g., `https://ufc-predictions-api.onrender.com`)
Save this - you'll need it for frontend.

---

## **Deploy Frontend to Vercel**

### Step 1: Add to GitHub (if not done)
Your frontend is already in the GitHub repo

### Step 2: Deploy Frontend to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Add New..." → "Project"
4. Select your `ufc-predictions` repo
5. Framework: Select `Next.js`
6. Root Directory: `frontend`
7. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://ufc-predictions-api.onrender.com
   ```
   (Replace with YOUR backend URL from Step 4)
8. Click "Deploy"

### Step 3: Wait for Deployment
Vercel auto-deploys. In ~2-3 minutes, you'll get:
```
✅ Deployment complete!
🔗 Your app is live at: https://your-project.vercel.app
```

---

## **Test Your Live App**

### 1. Open the App
```
https://your-project.vercel.app
```

### 2. Register a Test Account
- Click "Login" or go to `/auth`
- Click "Sign Up"
- Enter any username/email/password
- You'll be auto-logged in

### 3. Make a Prediction
- Upload a CSV with fight data
- See predictions with charts
- View history

### 4. Troubleshooting
If frontend can't connect to backend:
- Check backend URL in Vercel env vars
- Verify backend is running (`https://your-api.onrender.com/docs`)
- Check browser console for errors

---

## **Get Your Live Links**

After deployment, you have:

✅ **Backend API**: `https://ufc-predictions-api.onrender.com`
✅ **Frontend App**: `https://your-project.vercel.app`
✅ **API Docs**: `https://ufc-predictions-api.onrender.com/docs`

---

## **Optional: Custom Domain**

### Add Custom Domain to Vercel
1. Go to Vercel dashboard → your project
2. Settings → Domains
3. Add your domain (e.g., `ufc-predictions.com`)
4. Follow DNS instructions

---

## **Troubleshooting**

| Problem | Solution |
|---------|----------|
| 404 on backend | Check Render URL, ensure service is running |
| Frontend can't reach backend | Update `NEXT_PUBLIC_API_URL` in Vercel |
| Model not loading | Check if `models/ufc_prediction_model.pkl` is in repo |
| Database errors | Add PostgreSQL addon in Render, set `DATABASE_URL` |
| CORS errors | Backend already has `allow_origins=["*"]` |

---

## **Next Steps (Optional)**

- [ ] Enable Stripe for premium feature
- [ ] Add custom domain
- [ ] Set up monitoring (Sentry)
- [ ] Enable auto-deployments on push
