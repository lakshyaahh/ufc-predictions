# 🚀 COMPLETE DEPLOYMENT GUIDE - STEP BY STEP

> **Time Required**: ~30 minutes | **Cost**: FREE (Render + Vercel both have free tiers)

---

## **📋 PRE-DEPLOYMENT CHECKLIST**

✅ All files are ready  
✅ Backend API fully configured  
✅ Frontend app configured  
✅ Database ready  
✅ Model included  

**Status**: 🟢 **READY TO DEPLOY**

---

## **PHASE 1: PREPARE GITHUB (5 minutes)**

### Step 1: Initialize Git Repository

**On Windows (PowerShell):**
```powershell
cd "c:\Users\Lakshya\Desktop\UFC PREDICTIONS"
.\setup_github.bat
```

**On macOS/Linux:**
```bash
cd ~/UFC\ PREDICTIONS
bash setup_github.sh
```

This will:
- ✓ Initialize git
- ✓ Stage all files
- ✓ Create initial commit

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named: **`ufc-predictions`**
3. Choose: **Public** (so Render/Vercel can access it)
4. Click **Create Repository**

### Step 3: Push Code to GitHub

After running the script above, you'll see instructions. In PowerShell/Terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ufc-predictions.git
git branch -M main
git push -u origin main
```

⏳ Wait 30 seconds for push to complete.

---

## **PHASE 2: DEPLOY BACKEND TO RENDER (10 minutes)**

### Step 1: Create Render Account

1. Go to https://render.com
2. Click **Sign Up**
3. Choose **Sign up with GitHub** (easier!)
4. Authorize GitHub access

### Step 2: Deploy Backend Service

1. In Render dashboard, click **New +**
2. Select **Web Service**
3. Select your `ufc-predictions` GitHub repo
4. Fill in:
   - **Name**: `ufc-predictions-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
   - **Root Directory**: Leave blank

5. Click **Create Web Service**

⏳ **Wait 2-3 minutes for build & deployment**

### Step 3: Add PostgreSQL Database

1. In Render dashboard, click **New +**
2. Select **PostgreSQL**
3. Fill in:
   - **Name**: `ufc-predictions-db`
   - **Database**: `ufc_predictions`
   - **User**: `postgres`
   - **Region**: Same as backend
   - **Plan**: **Free** tier
4. Click **Create Database**

⏳ **Wait 1-2 minutes for database creation**

### Step 4: Connect Database to Backend

1. Go back to your backend service (`ufc-predictions-api`)
2. Click **Environment** (left sidebar)
3. Add these environment variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Copy from PostgreSQL service details (Internal Database URL) |
| `SECRET_KEY` | Generate random string: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ALGORITHM` | `HS256` |
| `TOKEN_EXPIRE_DAYS` | `30` |
| `MODEL_PATH` | `./models/ufc_prediction_model.pkl` |

4. Click **Save Changes**

### Step 5: Verify Backend is Running

1. Wait 2-3 minutes for redeploy with env vars
2. Copy your backend URL (shown at top of Render page, e.g., `https://ufc-predictions-api.onrender.com`)
3. Open in browser: `https://ufc-predictions-api.onrender.com/docs`
4. ✅ If you see interactive API docs, backend is working!

**📌 Save your backend URL - you'll need it for frontend!**

---

## **PHASE 3: DEPLOY FRONTEND TO VERCEL (10 minutes)**

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click **Sign Up**
3. Choose **Continue with GitHub**
4. Authorize GitHub access

### Step 2: Deploy Frontend

1. In Vercel dashboard, click **Add New**
2. Select **Project**
3. Find your `ufc-predictions` repo
4. Click **Import**
5. Fill in:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend` ⚠️ **Important!**
   - Leave other settings as default

6. Click **Deploy**

⏳ **Wait 2-3 minutes for build & deployment**

### Step 3: Add Environment Variable

Before deployment finishes:

1. Go to **Settings** → **Environment Variables**
2. Add:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://ufc-predictions-api.onrender.com` (your backend URL from Phase 2)
   - **Environment**: Production, Preview, Development

3. Click **Save**

### Step 4: Redeploy to Apply Environment Variable

1. Click **Deployments** (left sidebar)
2. Click the three dots (...) on latest deployment
3. Select **Redeploy**
4. Click **Redeploy**

⏳ **Wait 2-3 minutes for redeploy**

---

## **✅ DEPLOYMENT COMPLETE!**

### Your Live App URLs:

🎯 **Frontend (User-facing)**: 
```
https://YOUR_PROJECT_NAME.vercel.app
```

🔧 **Backend API**: 
```
https://ufc-predictions-api.onrender.com
```

📚 **API Documentation**: 
```
https://ufc-predictions-api.onrender.com/docs
```

---

## **🧪 TEST YOUR LIVE APP**

### Test Registration:
1. Open your frontend URL
2. Click **Login** → **Sign Up**
3. Enter:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `Test123!`
4. Click **Sign Up**
5. ✅ You should be logged in!

### Test Predictions:
1. You should see: **"Free Predictions Left: 3/3"**
2. Upload a CSV file with fight data (or use sample from dataset/)
3. ✅ See predictions with charts!

### If Something Breaks:
See **Troubleshooting** section below.

---

## **🔧 TROUBLESHOOTING**

| Problem | Solution |
|---------|----------|
| **Frontend shows "Cannot reach API"** | Check `NEXT_PUBLIC_API_URL` in Vercel env vars, verify backend URL is correct |
| **Vercel deployment failed** | Go to Deployments → click failed build → see error logs |
| **Render backend won't start** | Check Render logs, verify `DATABASE_URL` is set, ensure start command is correct |
| **Database connection error** | Verify `DATABASE_URL` is internal PostgreSQL URL from Render |
| **Model file not found** | Model is in repo, should be available. Check Render build logs |
| **CORS errors in browser** | Backend already has `allow_origins=["*"]`, might be network issue |

### Get Help:
1. Check Render logs: Your service → **Logs** tab
2. Check Vercel logs: Your project → **Deployments** → click build → **Logs**
3. Check browser console: F12 → Console tab for errors

---

## **📊 OPTIONAL: Custom Domain**

### Add Domain to Vercel
1. Go to your Vercel project → **Settings** → **Domains**
2. Enter your domain (e.g., `ufc-predictions.com`)
3. Add DNS records as shown
4. Wait 5-10 minutes for DNS propagation
5. ✅ Access via your custom domain!

---

## **🎉 YOU'RE LIVE!**

Your UFC predictions app is now:
✅ Live on the internet  
✅ Accessible 24/7  
✅ Using real databases  
✅ Ready for users  

Share your app URL with friends! 🚀

---

## **📝 IMPORTANT NOTES**

- **Free tier limitations**: 
  - Render spins down after 15 mins of inactivity (takes 30 secs to wake up)
  - Vercel has unlimited free deployments
  
- **Security**:
  - Never commit `.env` files with real secrets
  - Keep `SECRET_KEY` private (already in `.env.production` - don't share)
  
- **Scaling**:
  - When ready for paid tier, upgrade Render to get:
    - Always-on server
    - Better performance
    - 24/7 uptime

---

## **NEXT STEPS**

1. ✅ Share your app with others
2. 📊 Monitor usage in Render/Vercel dashboards
3. 🔄 When you update code, just `git push origin main` - both redeploy automatically!
4. 💳 (Optional) Set up Stripe for premium features
5. 📱 (Optional) Promote your app on social media

---

**Questions? Issues?** Check the logs first (99% of issues are there)!
