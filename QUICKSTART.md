# Quick Start Guide

## Setup Instructions

### 1. Install Dependencies

First, create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your OpenAI API key:

```bash
# Copy example file
copy .env.example .env

# Then edit .env and add your key:
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Run Locally

```bash
python main.py
```

The API will start at `http://localhost:8000`

### 4. Test the API

Open a new terminal and run:

```bash
python test_api.py
```

## Deploy to Render

### Step-by-Step Deployment

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Word Meaning API"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub account and select your repository
   - Render will auto-detect `render.yaml`
   - Click "Advanced" and add environment variable:
     - Key: `OPENAI_API_KEY`
     - Value: `sk-your-actual-api-key`
   - Click "Create Web Service"

3. **Get Your API URL**
   - Once deployed, copy the URL (e.g., `https://word-meaning-api.onrender.com`)
   - Update `raspi_integration_example.py` with your URL
   - Use this URL in your Raspberry Pi code

## API Usage

### Health Check
```bash
curl http://localhost:8000/
```

### Get Word Meaning
```bash
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"serendipity\"}"
```

### Get Sentence Explanation
```bash
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The quick brown fox jumps over the lazy dog\"}"
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "API key not found" error
- Check if `.env` file exists
- Verify `OPENAI_API_KEY` is set correctly

### Port already in use
```bash
# Change port in .env file
PORT=8080
```

## Next Steps

1. Test locally with `test_api.py`
2. Deploy to Render following the guide above
3. Update your Raspberry Pi code with the deployed URL
4. Monitor API usage in Render dashboard
