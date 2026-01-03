# Quick Test Guide - UFC Predictor SaaS

## Pre-Test Checklist

- [ ] Backend virtual environment activated
- [ ] `backend/requirements.txt` dependencies installed
- [ ] `backend/.env` created with SECRET_KEY, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY
- [ ] `frontend/.env.local` created with NEXT_PUBLIC_API_URL and NEXT_PUBLIC_STRIPE_KEY
- [ ] Backend running: `python -m uvicorn app.main:app --reload --port 8000`
- [ ] Frontend running: `npm run dev` (port 3000)
- [ ] Model file exists: `backend/models/ufc_prediction_model.pkl`

---

## Test Scenario 1: User Registration & Login

### Step 1: Register New User
1. Open http://localhost:3000
2. Should redirect to `/auth` (no token)
3. Click **"Create one here"** to switch to register mode
4. Fill form:
   - Username: `testuser1`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm: `password123`
5. Click **Register**
6. **Expected**: Redirect to home page, see "Welcome, testuser1"

### Step 2: View Upcoming Fights
1. Home page should show:
   - ✅ Disclaimer banner (yellow)
   - ✅ "Free Predictions Left: 3/3" (blue)
   - ✅ 3 match cards (UFC 302, 303, 304)
2. Each card shows:
   - Event name
   - Fighter names
   - Records & stats (reach, height)
   - Countdown timer
   - "Get Prediction" button

### Step 3: Logout & Login
1. Click **Logout** button
2. Should redirect to `/auth`
3. Fill login form:
   - Username: `testuser1`
   - Password: `password123`
4. Click **Login**
5. **Expected**: Redirect to home, same user stats restored

---

## Test Scenario 2: Free Predictions (3 Limit)

### Step 1: Make Prediction #1
1. Click "Get Prediction" on first match
2. **Modal opens** showing:
   - Fighter names side-by-side
   - Fighter stats (record, reach, age, KO ratio)
   - "Generate Prediction" button
3. Click **Generate Prediction**
4. **Expected**: 
   - Results shown (Red: 58%, Blue: 42%)
   - Confidence intervals displayed
   - Predicted winner highlighted
   - Counter updates: "2/3 free predictions left"

### Step 2: Make Predictions #2 & #3
1. Close modal
2. Make 2 more predictions on different matches
3. **Expected**: Counter goes 2/3 → 1/3 → 0/3

### Step 3: Hit Free Limit
1. Counter shows "0/3 free"
2. Click "Upgrade to Premium" link in counter banner
3. **Expected**: Redirect to `/premium` page
4. OR try to predict again:
   - Click "Get Prediction"
   - **Expected**: Error modal "Out of free predictions"

---

## Test Scenario 3: Premium Upgrade (Stripe)

### Step 1: View Premium Page
1. Navigate to http://localhost:3000/premium
2. **Should show:**
   - ✨ "Upgrade to Premium" heading
   - 💰 "$25 /lifetime" price
   - ✅ Features list (unlimited predictions, etc.)
   - 💳 "Upgrade Now with Stripe" button

### Step 2: Checkout Flow
1. Click **Upgrade Now with Stripe**
2. **Expected**: Redirect to Stripe Checkout (test environment)
3. Fill test payment form:
   - Card: `4242 4242 4242 4242`
   - Expiry: `12/25`
   - CVC: `123`
   - Email: Any email
   - Name: Any name
4. Click **Pay**
5. **Expected**: Success page → Redirect to home

### Step 3: Verify Premium Access
1. Home page now shows:
   - ✨ "PREMIUM MEMBER - Unlimited predictions" (green)
   - Counter no longer visible
2. Make unlimited predictions (no limit)
3. Check user stats:
   - Click browser dev tools → Network
   - GET `/user/stats`
   - Response shows `"is_premium": true`

---

## Test Scenario 4: Prediction History

### Step 1: View History
1. Click **"View Prediction History →"** link at bottom
2. **Expected**: 
   - Table showing all past predictions
   - Columns: Red Fighter, Blue Fighter, Red %, Blue %, Winner
   - At least 3 rows (from free predictions)

### Step 2: Links & Navigation
1. Click **"🥊 UFC Predictor"** header
2. **Expected**: Navigate back to home
3. Click **Logout**
4. **Expected**: Clear token, redirect to `/auth`

---

## Test Scenario 5: Auth Validation

### Step 1: Invalid Credentials
1. Go to `/auth`
2. Login form
3. Fill wrong password:
   - Username: `testuser1`
   - Password: `wrongpassword`
4. Click **Login**
5. **Expected**: Red error banner "Invalid username or password"

### Step 2: Registration Validation
1. Switch to register mode
2. Try with mismatched passwords:
   - Username: `testuser2`
   - Email: `test2@example.com`
   - Password: `password123`
   - Confirm: `different123`
3. Click **Register**
4. **Expected**: Error "Passwords do not match"

### Step 3: Duplicate Username
1. Try to register with existing username:
   - Username: `testuser1`
   - Email: `new@example.com`
   - Password: `password123`
   - Confirm: `password123`
2. Click **Register**
3. **Expected**: Error "Username already exists"

---

## Test Scenario 6: Edge Cases

### Expired Matches
1. **Backend only**: Matches past `event_date` should auto-delete
2. In `crud.py`, `delete_expired_matches()` runs on `/matches/upcoming` call
3. Verify old matches don't appear

### No Matches
1. If all matches expired, `/matches/upcoming` returns empty list
2. Frontend shows: "No upcoming fights at the moment."

### Token Expiration
1. Token expires in 30 days (check in `auth.py`)
2. After 30 days, logout + need to login again
3. Tests can manually manipulate token for testing

---

## Debugging Checklist

**If registration fails:**
- Check backend logs: Look for database errors
- Verify email format (must be valid email)
- Check `.env` file has `DATABASE_URL` set
- Try restarting backend server

**If predictions don't work:**
- Verify model file exists: `backend/models/ufc_prediction_model.pkl`
- Check backend logs for model loading errors
- Test endpoint: `curl http://localhost:8000/health`

**If Stripe fails:**
- Verify `STRIPE_SECRET_KEY` in backend `.env`
- Verify `NEXT_PUBLIC_STRIPE_KEY` in frontend `.env.local`
- Use Stripe test keys (sk_test_*, pk_test_*)
- Test card: `4242 4242 4242 4242` (always fails in test)
- Use `4000002500003155` for successful charge

**If matches don't load:**
- Check `/matches/upcoming` endpoint in backend
- Verify `matches.py` has sample fight data
- Backend should populate matches automatically on first call

**If styles look broken:**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check console for JS errors (F12)

---

## Performance Checks

- **Homepage load time**: Should be < 1 second
- **Prediction generation**: Should be < 2 seconds (model inference)
- **Database queries**: Should be < 100ms
- **API responses**: All should return within 1 second

---

## Security Verification

- ✅ Passwords are hashed (bcrypt) in database
- ✅ JWT tokens include user_id and username
- ✅ API endpoints require Authorization header
- ✅ Stripe handles payment data (PCI compliant)
- ✅ CORS enabled for frontend-backend communication
- ✅ Secret key in environment (not in code)

---

## Success Criteria

| Test | Expected Result | Status |
|------|-----------------|--------|
| Register user | Account created, JWT token returned | ✅/❌ |
| View upcoming matches | 3 fights displayed with stats | ✅/❌ |
| Make free prediction | Win probability calculated, counter decreases | ✅/❌ |
| Hit free limit | Error when trying 4th prediction | ✅/❌ |
| Premium upgrade | Stripe checkout succeeds, user becomes premium | ✅/❌ |
| Unlimited predictions | Premium user can make unlimited predictions | ✅/❌ |
| View history | All past predictions displayed | ✅/❌ |
| Logout | Token cleared, redirect to auth | ✅/❌ |

---

## Notes

- All test data (matches, stats) is **sample data** in `matches.py`
- Replace with real UFC API for production
- Stripe uses **test mode** by default
- No real charges with test card numbers
- Database resets when deleting `predictions.db`

---

**Ready to test? Start with Scenario 1! 🎯**
