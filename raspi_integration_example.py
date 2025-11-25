# Example Raspberry Pi integration code
# This demonstrates how to integrate the API with your existing Raspberry Pi code

import requests
import louis  # liblouis for Braille conversion


def check_for_internet_connection():
    """
    Check if internet connection is available.
    Implement this based on your existing code.
    """
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False


def get_selected_text_explanation(selected_text):
    """
    Gets the explanation of the selected text using the deployed API.
    
    Args:
        selected_text (str): The selected text to get the explanation of.
    
    Returns:
        str: The explanation of the selected text in Braille format.
    """
    try:
        # Check internet connection
        is_connected = check_for_internet_connection()
        if not is_connected:
            return "No internet connection Please check your internet connection and try again"
        
        # Your deployed API URL from Render
        # IMPORTANT: Replace this with your actual deployed URL
        API_URL = "https://your-api-name.onrender.com/explain"
        
        # Make POST request to API
        response = requests.post(
            API_URL,
            json={"text": selected_text},
            timeout=30  # 30 second timeout for API response
        )
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Check if explanation was successful (status code 200)
            if data["status"] == 200:
                explanation = data["meaning"]
                
                # The API already removes punctuation, so explanation is ready for Braille
                # Convert explanation to braille using liblouis
                braille_output = louis.translate(["en-us-g1.ctb"], explanation)
                return braille_output[0]
            else:
                return "Error getting explanation Please try again"
        else:
            return "Error getting explanation Server returned error"
            
    except requests.exceptions.Timeout:
        return "Request timed out Please try again"
    except requests.exceptions.ConnectionError:
        return "Cannot connect to API Check internet connection"
    except Exception as e:
        print(f"Error getting explanation of selected text: {e}")
        return "Error getting explanation"


# Example usage
if __name__ == "__main__":
    # Test with a word
    word = "serendipity"
    print(f"Testing with word: {word}")
    result = get_selected_text_explanation(word)
    print(f"Braille output: {result}\n")
    
    # Test with a sentence
    sentence = "The quick brown fox jumps over the lazy dog"
    print(f"Testing with sentence: {sentence}")
    result = get_selected_text_explanation(sentence)
    print(f"Braille output: {result}")
