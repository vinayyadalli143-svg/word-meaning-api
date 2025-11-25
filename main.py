from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import re
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Word Meaning API",
    description="API for providing word and sentence explanations using GPT-4o",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Raspberry Pi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class TextRequest(BaseModel):
    text: str

# Response model
class ExplanationResponse(BaseModel):
    status: int  # HTTP status code: 200, 400, 500
    meaning: str


def remove_punctuation(text: str) -> str:
    """
    Remove all punctuation from text for Braille compatibility.
    Keeps only letters, numbers, and spaces.
    """
    # Remove all punctuation except spaces
    cleaned = re.sub(r'[^\w\s]', '', text)
    # Remove extra spaces
    cleaned = ' '.join(cleaned.split())
    return cleaned


def is_single_word(text: str) -> bool:
    """
    Determine if the input is a single word or a sentence/paragraph.
    """
    # Strip whitespace and check if there are spaces
    words = text.strip().split()
    return len(words) == 1


def get_explanation(text: str) -> str:
    """
    Get explanation from GPT-4o based on input text.
    Uses different prompts for single words vs sentences/paragraphs.
    """
    try:
        if is_single_word(text):
            # Prompt for single word
            prompt = f"""Explain the meaning of the word "{text}" in simple, clear language. 
Use everyday words that anyone can understand. 
Keep it concise and focused only on the core meaning. 
Do not use complex vocabulary or technical terms.
Provide only the explanation without any introductory phrases."""
        else:
            # Prompt for sentence or paragraph
            prompt = f"""Explain the following text in simple, clear language: "{text}"
Use everyday words that anyone can understand.
Provide a concise explanation that captures the main idea.
Do not use complex vocabulary or technical terms.
Provide only the explanation without any introductory phrases."""
        
        # Call OpenAI API with GPT-4o model
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that explains words and sentences in simple, clear language suitable for all audiences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent explanations
            max_tokens=200,  # Limit response length
        )
        
        explanation = response.choices[0].message.content.strip()
        
        # Remove punctuation for Braille compatibility
        explanation_no_punctuation = remove_punctuation(explanation)
        
        return explanation_no_punctuation
    
    except Exception as e:
        logger.error(f"Error getting explanation from GPT-4o: {e}")
        raise


@app.get("/")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "ok",
        "message": "Word Meaning API is running",
        "version": "1.0.0"
    }


@app.post("/explain", response_model=ExplanationResponse)
async def explain_text(request: TextRequest):
    """
    Main endpoint to get explanation of text (word or sentence).
    
    Request body:
        {
            "text": "word or sentence to explain"
        }
    
    Response:
        {
            "status": 200 (success) or 400/500 (error),
            "meaning": "explanation without punctuation"
        }
    """
    try:
        # Validate input
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Text field cannot be empty")
        
        # Get explanation
        logger.info(f"Processing request for text: {request.text[:50]}...")
        explanation = get_explanation(request.text)
        
        return ExplanationResponse(
            status=200,
            meaning=explanation
        )
    
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    
    except Exception as e:
        # Log error and return error response
        logger.error(f"Error processing request: {e}")
        return ExplanationResponse(
            status=500,
            meaning="Error getting explanation Please try again later"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
