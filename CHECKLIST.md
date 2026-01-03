# ✅ DEPLOYMENT CHECKLIST

## **PHASE 1: BEFORE YOU START**
- [ ] Create GitHub account (https://github.com/signup)
- [ ] Create Render account (https://render.com)
- [ ] Create Vercel account (https://vercel.com)
- [ ] Read START_HERE.md
- [ ] Read VIDEO_GUIDE.md

**Estimated Time**: 10 minutes

---

## **PHASE 2: GITHUB SETUP**
- [ ] Open PowerShell in project directory
- [ ] Run: `.\setup_github.bat`
- [ ] Create repo at https://github.com/new
- [ ] Name repo: `ufc-predictions`
- [ ] Make it **Public**
- [ ] Run git remote command: `git remote add origin https://...`
- [ ] Run: `git branch -M main`
- [ ] Run: `git push -u origin main`
- [ ] Wait 30 seconds for push to complete
- [ ] Verify code is on GitHub (visit your repo)

**Estimated Time**: 5 minutes

---

## **PHASE 3: BACKEND DEPLOYMENT (RENDER)**

### **Part A: Web Service**
- [ ] Go to https://render.com
- [ ] Click "New +" → "Web Service"
- [ ] Select your `ufc-predictions` repo
- [ ] Fill in:
  - [ ] Name: `ufc-predictions-api`
  - [ ] Environment: `Python 3`
  - [ ] Root Directory: `backend`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- [ ] Click "Create Web Service"
- [ ] Wait 2-3 minutes for deployment
- [ ] Verify it says "Your service is running"

### **Part B: Database**
- [ ] Click "New +" → "PostgreSQL"
- [ ] Fill in:
  - [ ] Name: `ufc-predictions-db`
  - [ ] Database: `ufc_predictions`
  - [ ] User: `postgres`
  - [ ] Region: Same as backend
  - [ ] Plan: Free
- [ ] Click "Create Database"
- [ ] Wait 2-3 minutes for database creation
- [ ] Copy the Internal Database URL (not external)

### **Part C: Environment Variables**
- [ ] Go back to `ufc-predictions-api` service
- [ ] Click "Environment" in left sidebar
- [ ] Add these variables:

| Key | Value |
|-----|-------|
| DATABASE_URL | (paste Internal Database URL) |
| SECRET_KEY | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| ALGORITHM | HS256 |
| TOKEN_EXPIRE_DAYS | 30 |
| MODEL_PATH | ./models/ufc_prediction_model.pkl |

- [ ] Click "Save"
- [ ] Wait 3-5 minutes for redeploy

### **Part D: Verification**
- [ ] Copy your backend URL from Render (e.g., https://ufc-predictions-api.onrender.com)
- [ ] Open in browser: `https://your-backend-url/docs`
- [ ] Should see API documentation page
- [ ] ✅ Backend is working!

**Estimated Time**: 10 minutes
**Backend URL**: `_______________________________`

---

## **PHASE 4: FRONTEND DEPLOYMENT (VERCEL)**

### **Part A: Project Setup**
- [ ] Go to https://vercel.com
- [ ] Click "Add New" → "Project"
- [ ] Select your `ufc-predictions` repo
- [ ] Click "Import"
- [ ] Fill in:
  - [ ] Framework: Next.js
  - [ ] Root Directory: **`frontend`** (important!)
- [ ] Click "Deploy"
- [ ] Wait 2-3 minutes for deployment

### **Part B: Environment Variable**
- [ ] Go to "Settings" → "Environment Variables"
- [ ] Add:
  - [ ] Name: `NEXT_PUBLIC_API_URL`
  - [ ] Value: `https://your-backend-url.onrender.com` (from Phase 3)
  - [ ] Environments: Select all (Production, Preview, Development)
- [ ] Click "Add"

### **Part C: Redeploy**
- [ ] Go to "Deployments" tab
- [ ] Click three dots (...) on latest deployment
- [ ] Click "Redeploy"
- [ ] Click "Redeploy" in popup
- [ ] Wait 2-3 minutes for redeploy

### **Part D: Get Your Link**
- [ ] Go to "Deployments" tab
- [ ] Look for successful (green) deployment
- [ ] Find the URL: `https://your-app-name.vercel.app`
- [ ] ✅ Frontend is live!

**Estimated Time**: 10 minutes
**Frontend URL**: `_______________________________`

---

## **PHASE 5: TESTING YOUR APP**

### **Test 1: App Loads**
- [ ] Go to your frontend URL
- [ ] Homepage should load
- [ ] No error messages

### **Test 2: Register Account**
- [ ] Click "Login" in top right
- [ ] Click "Sign Up"
- [ ] Enter:
  - Username: `testuser123`
  - Email: `test@example.com`
  - Password: `Test123!Pass`
- [ ] Click "Sign Up"
- [ ] Should be logged in

### **Test 3: Make Prediction**
- [ ] Should see "Free Predictions Left: 3/3"
- [ ] Try uploading a fight data file (if you have one)
- [ ] Should see prediction results

### **Test 4: View History**
- [ ] Click "History" in navigation
- [ ] Should see your past predictions
- [ ] Charts should display

### **All Tests Pass?**
- [ ] ✅ **CONGRATULATIONS! YOUR APP IS LIVE!**

**Estimated Time**: 5 minutes

---

## **SUMMARY**

### **Your Live Links:**
```
🎯 Main App: 
   https://your-app-name.vercel.app

🔧 Backend API: 
   https://ufc-predictions-api.onrender.com

📚 API Docs: 
   https://ufc-predictions-api.onrender.com/docs
```

### **What Works:**
- ✅ User registration
- ✅ User login
- ✅ Make predictions
- ✅ View history
- ✅ Charts & visualizations
- ✅ All features!

### **Total Time**: ~40 minutes

### **Cost**: FREE

---

## **TROUBLESHOOTING**

### **Problem: "Cannot reach backend"**
- [ ] Check `NEXT_PUBLIC_API_URL` in Vercel Settings
- [ ] Make sure it's exactly: `https://your-backend-url.onrender.com`
- [ ] Verify backend is running in Render dashboard
- [ ] Redeploy frontend in Vercel

### **Problem: "Application Error" in Render**
- [ ] Go to Render → your service → Logs
- [ ] Look for error messages
- [ ] Usually: `DATABASE_URL` is wrong or missing
- [ ] Fix environment variables
- [ ] Redeploy

### **Problem: Can't register account**
- [ ] Open browser console: F12 → Console
- [ ] Look for error messages
- [ ] If database error: check `DATABASE_URL` in Render
- [ ] If JWT error: check `SECRET_KEY` in Render

### **Problem: Predictions not showing**
- [ ] Check if CSV upload succeeded
- [ ] Verify ML model is loaded (check Render logs)
- [ ] Make sure you're logged in

### **Still stuck?**
- [ ] Check Render logs (Service → Logs tab)
- [ ] Check Vercel logs (Deployments → click build)
- [ ] Check browser console (F12 → Console)
- [ ] Read troubleshooting in VIDEO_GUIDE.md

---

## **AFTER DEPLOYMENT**

- [ ] Test everything works
- [ ] Share your app link with friends!
- [ ] Monitor dashboards occasionally
- [ ] When you update code: `git push origin main` auto-deploys
- [ ] (Optional) Add custom domain to Vercel

---

## **✅ DEPLOYMENT COMPLETE!**

Your UFC Predictions app is now:
- ✅ Live on the internet
- ✅ Accessible 24/7
- ✅ Using real databases
- ✅ Ready for users

**Share your link: `_______________________________`**

---

**Print this checklist and check off as you go!**

**Questions?** Check the relevant guide.

**You've got this! 🚀**
