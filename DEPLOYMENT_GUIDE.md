# Deployment Guide: Run on Your Phone

This guide will help you deploy your tour guide app to the cloud so you can access it on your phone without your computer.

## Prerequisites

- GitHub account (free)
- Railway.app account (free - no credit card required for trial)
- Your API keys ready

## Step-by-Step Deployment

### 1. Initialize Git Repository (5 minutes)

Open Terminal in your V4 folder and run:

```bash
cd "/Users/kuba_jarzebski/Documents/Portfolio/Unit 9 - Personal Project/App/Tour Guide/OpenAI_API_Version/V3/V4"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: London tour guide app"
```

### 2. Create GitHub Repository (3 minutes)

1. Go to https://github.com
2. Click the **+** button → **New repository**
3. Name it: `london-tour-guide` (or whatever you prefer)
4. Choose **Private** (keeps your API keys safe)
5. **DO NOT** initialize with README (we already have files)
6. Click **Create repository**

### 3. Push to GitHub (2 minutes)

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/london-tour-guide.git
git branch -M main
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username.

### 4. Deploy to Railway (10 minutes)

#### A. Create Railway Account

1. Go to https://railway.app
2. Click **Start a New Project**
3. Sign up with GitHub (easiest option)
4. Authorize Railway to access your repos

#### B. Deploy Project

1. Click **Deploy from GitHub repo**
2. Select `london-tour-guide` (or your repo name)
3. Click **Deploy Now**

Railway will automatically:
- Detect it's a Python app
- Install dependencies from `requirements.txt`
- Start the server

#### C. Add Environment Variables

1. In Railway, click on your project
2. Go to **Variables** tab
3. Click **+ New Variable**
4. Add these two variables:

```
GOOGLE_DIRECTIONS_KEY = REDACTED_GOOGLE_KEY
OPENAI_API_KEY = REDACTED_OPENAI_KEY
```

**Important Security Note:** These are YOUR actual API keys from your `.env` file. Keep them private!

5. Click **Deploy** to restart with the new variables

#### D. Get Your App URL

1. Go to **Settings** tab
2. Click **Generate Domain**
3. Your app will be available at: `your-app-name.railway.app`

### 5. Test on Your Phone (1 minute)

1. Open Safari/Chrome on your phone
2. Go to: `https://your-app-name.railway.app`
3. Bookmark it for easy access!
4. Navigate to `/track?start=...&end=...` to use GPS tracking

## Example URLs

**Route Planner:**
```
https://your-app.railway.app/
```

**Live Tracking (example route):**
```
https://your-app.railway.app/track?start=British%20Museum&end=Tower%20Bridge&mode=fastest
```

## Troubleshooting

### App won't start?
- Check **Deployments** tab for error logs
- Verify environment variables are set correctly
- Make sure `requirements.txt` includes all dependencies

### "500 Internal Server Error"?
- Check if API keys are valid
- Look at Railway logs for Python errors

### GPS not working on phone?
- Make sure you allowed location permissions in browser
- HTTPS is required for GPS (Railway provides this automatically)
- Try the simulator feature if GPS fails

## Cost

**Railway Free Tier:**
- $5 credit/month (free)
- Enough for ~500 hours of runtime
- Perfect for testing and personal use

**When you exceed free tier:**
- Railway charges $0.000463/GB-hour
- Estimated: ~$5-10/month for moderate use
- You can set spending limits

## Updating Your App

When you make changes:

```bash
# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push

# Railway automatically redeploys!
```

## Alternative: Render.com (If Railway doesn't work)

1. Go to https://render.com
2. Create account with GitHub
3. **New** → **Web Service**
4. Select your repo
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (same as Railway)
7. Deploy!

**Note:** Free tier spins down after 15 min inactivity (30s cold start)

## Security Checklist

✅ Never commit `.env` file (already in `.gitignore`)
✅ Use private GitHub repo
✅ Rotate API keys if accidentally exposed
✅ Set Railway/Render environment variables (not in code)
✅ Use HTTPS only (automatic on Railway/Render)

## Next Steps

Once deployed:
1. Test all 3 route modes
2. Walk a short route to test GPS triggering
3. Verify landmarks trigger at correct distances
4. Share the URL with friends to test!

---

**Need help?** Check Railway docs: https://docs.railway.app/
