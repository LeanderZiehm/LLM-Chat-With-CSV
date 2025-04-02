import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("GROQ_API_KEY")

def get_groq_response(user_message):
    if not API_KEY:
        raise ValueError("API key is missing. Please set GROQ_API_KEY in your .env file.")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "system", "content": "Your task is to recommend anonymization techniques for the user's dataset."},
                     {"role": "user", "content": user_message}],
        "model": "llama-3.3-70b-versatile",
        "temperature": 0,  # Set the temperature to 0
        "max_completion_tokens": 1024,  # Limit the response to 1024 tokens
        "top_p": 1,  # Set top_p to 1
        "stream": False,  # Disable streaming
        "stop": None  # No stopping tokens
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    else:
        return f"Error {response.status_code}: {response.text}"

# Example usage
if __name__ == "__main__":
    user_input = "Explain the importance of fast language models"
    print(get_groq_response(user_input))
