# 🚀 Complete Deployment Guide for Render

## ✅ Local Testing (Already Complete!)

Your API is **already running successfully** on your computer at `http://localhost:8000`!

**Test Results:**
- ✅ Health check: Working
- ✅ Word explanations: Working (tested with "serendipity")
- ✅ Sentence explanations: Working  
- ✅ Punctuation removal: Working (Braille-ready!)
- ✅ GPT-4o integration: Working

---

## 🌐 Deploy to Render (24/7 Online)

Follow these steps to make your API available online 24/7:

### Step 1: Push Code to GitHub

1. **Initialize Git (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Word Meaning API with GPT-4o"
   ```

2. **Create GitHub Repository**
   - Go to https://github.com/new
   - Repository name: `word-meaning-api`
   - Description: `API for word meanings using GPT-4o`
   - Keep it **Public** or **Private** (both work)
   - Click **"Create repository"**

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/word-meaning-api.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username.

---

### Step 2: Deploy on Render

#### 2.1 Create Render Account
1. Go to https://render.com/
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account** (recommended)

#### 2.2 Create New Web Service
1. After logging in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. **Connect GitHub repository:**
   - You'll see "Connect a repository"
   - Click **"Connect account"** if you haven't connected GitHub
   - Find your `word-meaning-api` repository
   - Click **"Connect"**

#### 2.3 Configure Web Service

When configuring your service, use these settings:

| Field | Value |
|-------|-------|
| **Name** | `word-meaning-api` (or any name you prefer) |
| **Region** | Choose closest to your location |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

> **Note:** Render auto-detects Python and should fill these automatically from `render.yaml`!

#### 2.4 Set Environment Variables

**CRITICAL STEP:**

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add your OpenAI API key:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `your-openai-api-key-here` (Get your key from https://platform.openai.com/)

4. Click **"Add"**

#### 2.5 Choose Plan

1. Select **"Free"** plan
   - Free tier: 750 hours/month
   - Perfect for 24/7 operation (720 hours/month)
   - API will sleep after 15 min of inactivity
   - First request after sleep takes ~30 seconds

2. Click **"Create Web Service"**

---

### Step 3: Wait for Deployment

1. **Watch the build process:**
   - You'll see a live log of your app building
   - Takes about 2-3 minutes

2. **Wait for deployment:**
   - Status will change from "Building" → "Live"
   - You'll see: ✅ **"Your service is live"**

3. **Get your URL:**
   - At the top, you'll see your URL
   - Example: `https://word-meaning-api-abcd.onrender.com`
   - **Copy this URL!**

---

### Step 4: Test Your Deployed API

#### Test 1: Health Check

Open your browser and go to:
```
https://your-app-name.onrender.com/
```

You should see:
```json
{
  "status": "ok",
  "message": "Word Meaning API is running",
  "version": "1.0.0"
}
```

#### Test 2: Word Explanation

Using PowerShell:
```powershell
# Replace with your actual Render URL
$url = "https://your-app-name.onrender.com/explain"

# Test with a word
Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body '{"text":"serendipity"}'
```

Or using Python:
```python
import requests

url = "https://your-app-name.onrender.com/explain"
response = requests.post(url, json={"text": "serendipity"})
print(response.json())
```

Expected output:
```json
{
  "status": "success",
  "meaning": "finding something good by chance when you werent looking for it"
}
```

---

### Step 5: Update Your Raspberry Pi Code

Now update your Raspberry Pi code with the deployed URL:

```python
# In your Raspberry Pi code, update the URL:

def get_selected_text_explanation(selected_text):
    try:
        is_connected = check_for_internet_connection()
        if not is_connected:
            return "No internet connection Please check your internet connection and try again"
        
        # ⭐ USE YOUR DEPLOYED URL HERE ⭐
        API_URL = "https://your-app-name.onrender.com/explain"
        
        response = requests.post(
            API_URL,
            json={"text": selected_text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                explanation = data["meaning"]
                braille_output = louis.translate(["en-us-g1.ctb"], explanation)
                return braille_output[0]
            else:
                return "Error getting explanation"
        else:
            return "Error getting explanation Server returned error"
            
    except Exception as e:
        print(f"Error: {e}")
        return "Error getting explanation"
```

---

## 🎯 Important Notes

### Free Tier Limitations
- ✅ **750 hours/month** (perfect for 24/7!)
- ⚠️ **Spins down after 15 min** of no activity
- ⏱️ First request after sleep: ~30-60 seconds
- 💡 Next requests: Fast (~1-3 seconds)

### Upgrade to Paid Plan (Optional)
If you need always-on service without sleep:
- Starter Plan: $7/month
- No sleep, instant responses
- Good for high-traffic applications

### Keep API Awake (Free Tier Hack)
If you want to prevent sleep on free tier:
- Use a service like **UptimeRobot** (free)
- Ping your health endpoint every 10 minutes
- Go to: https://uptimerobot.com/
- Add monitor: `https://your-app.onrender.com/`
- Interval: 5 minutes

---

## 📊 Monitor Your API

### View Logs
1. Go to Render Dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time requests and responses

### View Metrics
1. In your service dashboard
2. Click **"Metrics"** tab
3. See:
   - Request count
   - Response times
   - Error rates
   - CPU/Memory usage

---

## 🔧 Update Your API

When you make code changes:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Updated API feature"
   git push
   ```

2. **Render auto-deploys:**
   - Render detects the git push
   - Automatically rebuilds and deploys
   - Takes 2-3 minutes
   - Zero downtime!

---

## ❓ Troubleshooting

### Problem: "Service Failed to Start"
**Solution:**
- Check Render logs for error messages
- Verify `OPENAI_API_KEY` is set correctly
- Ensure `requirements.txt` is up to date

### Problem: "API returns 500 error"
**Solution:**
- Check if OpenAI API key is valid
- Check if you have OpenAI credits
- View Render logs for detailed error

### Problem: "Slow first response after sleep"
**Solution:**
- This is normal on free tier
- Upgrade to paid plan for instant responses
- Or use UptimeRobot to keep it awake

### Problem: "OpenAI quota exceeded"
**Solution:**
- Add credits to your OpenAI account
- Go to: https://platform.openai.com/account/billing
- Add payment method and credits

---

## 🎉 You're Done!

Your API is now:
- ✅ **Live 24/7** at your Render URL
- ✅ **Accessible** from anywhere (including Raspberry Pi)
- ✅ **Automatically deployed** when you push code
- ✅ **Monitored** with logs and metrics
- ✅ **Braille-ready** with punctuation removal
- ✅ **GPT-4o powered** for accurate explanations

**Your Deployed URL:**
```
https://your-app-name.onrender.com
```

Use this URL in your Raspberry Pi code and you're all set! 🚀
