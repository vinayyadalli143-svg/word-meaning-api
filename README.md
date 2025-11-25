# Word Meaning API

A FastAPI-based REST API that provides word and sentence explanations using OpenAI's GPT-4o model. Optimized for Braille output on Raspberry Pi devices.

## Features

- 🎯 **Smart Detection**: Automatically distinguishes between single words and sentences/paragraphs
- 🤖 **GPT-4o Powered**: Uses OpenAI's latest model for accurate, simple explanations
- ♿ **Braille Compatible**: Removes all punctuation from responses for seamless Braille conversion
- 🚀 **Fast & Reliable**: Built with FastAPI for high performance
- 🌐 **24/7 Availability**: Deploy on Render for continuous uptime
- 📡 **CORS Enabled**: Ready for cross-origin requests from Raspberry Pi devices

## API Endpoints

### Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "ok",
  "message": "Word Meaning API is running",
  "version": "1.0.0"
}
```

### Explain Text
```http
POST /explain
Content-Type: application/json

{
  "text": "serendipity"
}
```

**Response:**
```json
{
  "status": "success",
  "meaning": "finding something good without looking for it"
}
```

## Local Development

### Prerequisites
- Python 3.9 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd word_meaning_antigravity
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

5. **Run the server**
```bash
python main.py
# Or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Deployment to Render

### Method 1: Using Render Dashboard

1. **Push to GitHub**
   - Create a new GitHub repository
   - Push your code to the repository

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Add your `OPENAI_API_KEY` in the environment variables section
   - Click "Create Web Service"

3. **Get Your API URL**
   - Once deployed, Render will provide a URL like `https://word-meaning-api.onrender.com`
   - Use this URL in your Raspberry Pi code

### Method 2: Using Render Blueprint

1. **Push to GitHub** (if not already done)

2. **Create Blueprint**
   - Go to Render Dashboard
   - Click "Blueprints" → "New Blueprint Instance"
   - Connect your repository
   - The `render.yaml` file will be automatically detected
   - Add environment variables and deploy

### Environment Variables

Configure these in your Render dashboard:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `PORT` | Port number (auto-set by Render) | No |

## Usage Examples

### Using curl

**Single Word:**
```bash
curl -X POST https://your-api-url.onrender.com/explain \
  -H "Content-Type: application/json" \
  -d '{"text": "ephemeral"}'
```

**Sentence:**
```bash
curl -X POST https://your-api-url.onrender.com/explain \
  -H "Content-Type: application/json" \
  -d '{"text": "The quick brown fox jumps over the lazy dog"}'
```

### Raspberry Pi Integration

Update your Raspberry Pi code with the deployed API URL:

```python
import requests
import louis

def get_selected_text_explanation(selected_text):
    """
    Gets the explanation of the selected text using online API.
    Args:
        selected_text (str): The selected text to get the explanation of.
    Returns:
        str: The explanation of the selected text in Braille.
    """
    try:
        is_connected = check_for_internet_connection()
        if not is_connected:
            return "No internet connection. Please check your internet connection and try again."
        
        # Your deployed API URL
        url = "https://your-api-url.onrender.com/explain"
        
        response = requests.post(url, json={"text": selected_text})
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                explanation = data["meaning"]
                # Convert explanation to braille using liblouis
                braille_output = louis.translate(["en-us-g1.ctb"], explanation)
                return braille_output[0]
            else:
                return "Error getting explanation"
        else:
            return "Error getting explanation"
    except Exception as e:
        print(f"Error getting explanation of selected text: {e}")
        return "Error getting explanation"
```

### Using Python requests

```python
import requests

url = "https://your-api-url.onrender.com/explain"

# Single word
response = requests.post(url, json={"text": "ubiquitous"})
print(response.json())
# Output: {"status": "success", "meaning": "found everywhere"}

# Sentence
response = requests.post(url, json={"text": "She sells seashells by the seashore"})
print(response.json())
# Output: {"status": "success", "meaning": "..."}
```

## How It Works

1. **Input Detection**: The API analyzes if the input is a single word or multiple words
2. **Prompt Optimization**: Different prompts are used for words vs sentences to get the best explanations
3. **GPT-4o Processing**: OpenAI's GPT-4o model generates a simple, clear explanation
4. **Punctuation Removal**: All punctuation is removed for Braille compatibility
5. **JSON Response**: Returns structured response with status and meaning fields

## Response Format

All responses follow this structure:

```json
{
  "status": "success" | "error",
  "meaning": "explanation text without punctuation"
}
```

## Error Handling

The API handles various error scenarios:

- **Empty input**: Returns 400 Bad Request
- **API failures**: Returns error status with user-friendly message
- **Invalid requests**: Proper HTTP error codes and messages

## Cost Considerations

- Uses OpenAI GPT-4o model (check current pricing at [OpenAI Pricing](https://openai.com/pricing))
- Render free tier includes 750 hours/month (sufficient for 24/7 uptime)
- For high traffic, consider upgrading Render plan

## Troubleshooting

### API returns error
- Check if `OPENAI_API_KEY` is properly set in Render environment variables
- Verify your OpenAI account has API credits

### Slow responses
- First request after inactivity may be slow (Render's free tier spins down after 15 min)
- Consider upgrading to a paid Render plan for always-on service

### CORS issues
- The API allows all origins by default
- Modify `CORSMiddleware` settings in `main.py` if needed

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues or questions, please create an issue in the GitHub repository.
