# 🎬 STEP-BY-STEP DEPLOYMENT VIDEO GUIDE

> **Total Time**: 30 minutes | **Cost**: FREE | **Technical Level**: Beginner-Friendly

---

## **BEFORE YOU START**

✅ You have:
- GitHub account (free at https://github.com)
- Render account (free at https://render.com)
- Vercel account (free at https://vercel.com)

> **Note**: You can create all three accounts in 5 minutes

---

## **SECTION 1: GITHUB SETUP (5 minutes)**

### Step 1.1: Open PowerShell

**Windows**:
- Press `Win + X`
- Click "Windows PowerShell" or "Terminal"
- Paste this command:

```powershell
cd "c:\Users\Lakshya\Desktop\UFC PREDICTIONS"
```

### Step 1.2: Initialize Git

Run this command:

```powershell
.\setup_github.bat
```

**What happens**:
- ✓ Git repo initialized
- ✓ All files staged
- ✓ Commit created
- ✓ Shows next steps

### Step 1.3: Create GitHub Repository

1. Go to https://github.com/new
2. Create new repo:
   - **Name**: `ufc-predictions`
   - **Visibility**: **Public**
   - **DON'T** add README (repo already has one)
   - Click **Create repository**

### Step 1.4: Push to GitHub

After repo created, GitHub shows a page like:

```
…or push an existing repository from the command line

git remote add origin https://github.com/YOUR_USERNAME/ufc-predictions.git
git branch -M main
git push -u origin main
```

**Copy these commands** and run in PowerShell:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ufc-predictions.git
git branch -M main
git push -u origin main
```

> Replace `YOUR_USERNAME` with your actual GitHub username!

**Wait 30 seconds** for upload. You should see:

```
Enumerating objects: XXX, done.
...
✓ Push successful!
```

✅ **GitHub Setup Complete!**

---

## **SECTION 2: DEPLOY BACKEND TO RENDER (10 minutes)**

### Step 2.1: Create Render Account

1. Go to https://render.com
2. Click **Sign Up**
3. Choose **Sign up with GitHub**
4. Click **Authorize Render**

✅ You're now logged into Render

### Step 2.2: Deploy Web Service

1. In Render dashboard, click **New +** button
2. Select **Web Service**
3. You'll see your repos. Select `ufc-predictions`
4. Click **Connect**

### Step 2.3: Configure Web Service

Fill in these fields:

```
Name:                  ufc-predictions-api
Environment:           Python 3
Region:                Choose closest to you (us-east-1, etc)
Branch:                main
Root Directory:        backend
Build Command:         pip install -r requirements.txt
Start Command:         gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
Plan:                  Free
```

Click **Create Web Service**

**Wait 2-3 minutes** - you'll see:
- Build running
- Deploying
- "Your service is running"

✅ Backend deployed!

### Step 2.4: Create Database

1. In Render dashboard, click **New +**
2. Select **PostgreSQL**
3. Fill in:

```
Name:              ufc-predictions-db
Database:          ufc_predictions
User:              postgres
Password:          (auto-generated, you don't need to remember it)
Region:            Same as your backend
Plan:              Free
```

Click **Create Database**

**Wait 2-3 minutes** for database creation

✅ Database created!

### Step 2.5: Connect Database to Backend

1. Go to your PostgreSQL database service
2. You'll see the connection string:
   ```
   postgresql://user:password@host:port/database
   ```
3. Copy the **Internal Database URL** (NOT the external one)

4. Go back to `ufc-predictions-api` service
5. Click **Environment** in left sidebar
6. Add these environment variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Paste the Internal Database URL from PostgreSQL |
| `SECRET_KEY` | Generate one: Run `python -c "import secrets; print(secrets.token_urlsafe(32))"` in PowerShell, copy output |
| `ALGORITHM` | `HS256` |
| `TOKEN_EXPIRE_DAYS` | `30` |
| `MODEL_PATH` | `./models/ufc_prediction_model.pkl` |

7. Click **Save**

**Wait 3-5 minutes** for redeploy with new environment variables

### Step 2.6: Verify Backend is Running

1. Go to your `ufc-predictions-api` service page
2. At the top, you'll see a URL like:
   ```
   https://ufc-predictions-api.onrender.com
   ```

3. Copy this URL
4. Open in browser: `https://ufc-predictions-api.onrender.com/docs`

**You should see**:
- Beautiful API documentation
- List of endpoints
- Try them out section

✅ If you see this, backend is working!

**📌 SAVE THIS URL - you need it for frontend!**

---

## **SECTION 3: DEPLOY FRONTEND TO VERCEL (10 minutes)**

### Step 3.1: Create Vercel Account

1. Go to https://vercel.com
2. Click **Sign Up**
3. Choose **Continue with GitHub**
4. Click **Authorize**

✅ Logged into Vercel

### Step 3.2: Deploy Project

1. In Vercel dashboard, click **Add New**
2. Click **Project**
3. Under "Import Git Repository", find `ufc-predictions`
4. Click **Import**

### Step 3.3: Configure Project

You'll see a setup form:

```
Project Name:      ufc-predictions (or any name you like)
Framework:         Next.js
Root Directory:    frontend ⚠️ IMPORTANT!
```

**Make sure Root Directory is set to `frontend`** (click to change if needed)

Leave other settings default

Click **Deploy**

**Wait 2-3 minutes** for deployment

### Step 3.4: Add Environment Variable

Before deployment finishes:

1. Click **Settings** tab
2. Click **Environment Variables** in left sidebar
3. Add new variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://ufc-predictions-api.onrender.com` (your backend URL)
   - **Select all environments** (Production, Preview, Development)
4. Click **Add**

### Step 3.5: Redeploy with Environment Variable

1. Go to **Deployments** tab
2. Find latest deployment (should be running)
3. Click the three dots (...)
4. Click **Redeploy**
5. Click **Redeploy** in popup

**Wait 2-3 minutes** for redeploy

✅ Frontend deployed!

### Step 3.6: Get Your Live URL

1. Go to **Deployments** tab
2. Click on the successful (green) deployment
3. You'll see:
   ```
   ✓ Production
   Your site is ready to visit
   https://your-app-name.vercel.app
   ```

**📌 This is your live app URL!**

---

## **✅ DEPLOYMENT COMPLETE!**

### Your Live App Links

| What | URL |
|------|-----|
| **Your App** (User-Facing) | `https://your-app-name.vercel.app` |
| **API Backend** | `https://ufc-predictions-api.onrender.com` |
| **API Documentation** | `https://ufc-predictions-api.onrender.com/docs` |

---

## **🧪 TEST YOUR APP (5 minutes)**

### Test 1: Open App
1. Go to `https://your-app-name.vercel.app`
2. You should see UFC Predictions landing page
3. ✅ Frontend is working!

### Test 2: Register Account
1. Click **Login** in top right
2. Click **Sign Up**
3. Fill in:
   - Username: `testuser123`
   - Email: `test@example.com`
   - Password: `Test123!Password`
4. Click **Sign Up**
5. ✅ You should be logged in!

### Test 3: Make Prediction
1. You should see: **"Free Predictions Left: 3/3"**
2. You can now:
   - Upload a CSV file (if you have fight data)
   - Or try the sample prediction interface
3. ✅ Predictions working!

### Test 4: Check History
1. Click **History** in navigation
2. You should see your past predictions
3. Charts should display
4. ✅ History working!

---

## **🎉 YOU'RE LIVE!**

Your app is now:
- ✅ **Live on the internet**
- ✅ **Accessible 24/7**
- ✅ **Using real databases**
- ✅ **Ready for users**
- ✅ **Free to host**

---

## **❌ TROUBLESHOOTING**

### Problem: "Cannot reach backend" in app

**Solution**:
1. Check your Vercel env var: `NEXT_PUBLIC_API_URL`
2. Make sure it's exactly: `https://ufc-predictions-api.onrender.com`
3. Go to Vercel → Deployments → Redeploy

### Problem: Backend URL shows "Application Error"

**Solution**:
1. Go to Render → your backend service
2. Click **Logs** tab
3. Look for error messages
4. Common issue: `DATABASE_URL` is wrong
5. Fix and redeploy

### Problem: Can't register - "Server error"

**Solution**:
1. Check browser console: F12 → Console tab
2. Look for error details
3. If database error: check `DATABASE_URL` in Render
4. If JWT error: check `SECRET_KEY` in Render

### Problem: Predictions show but no results

**Solution**:
1. Check if you uploaded a valid CSV
2. CSV must have columns: `ReachDiff`, `HeightDiff`, `AgeDif`, etc.
3. Check Render logs for ML model errors

---

## **💡 TIPS**

- **Auto-deploy**: Every time you `git push origin main`, both sites redeploy automatically
- **Monitor**: Check Render & Vercel dashboards to see uptime
- **Logs**: Always check logs first when something breaks
- **Free tier note**: Render spins down after 15 mins (takes ~30 secs to wake up)

---

## **NEXT STEPS**

1. ✅ Deployment complete
2. 📱 Share app link with friends
3. 📊 Check dashboards periodically
4. 🔄 Update code with `git push origin main`
5. 💳 (Optional) Upgrade to paid tier if needed

---

**Congratulations! Your UFC Predictions app is LIVE! 🚀**
