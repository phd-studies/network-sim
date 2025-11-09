import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_tweet():
    """
    Generates a tweet about T-Mobile customer experience using the OpenRouter API.
    """
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not found in .env file."

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            },
            data=json.dumps({
                "model": "nvidia/nemotron-nano-9b-v2",
                "messages": [
                    {"role": "user", "content": "Write a short, realistic tweet about a customer's experience with T-Mobile, either positive or negative. Keep it under 280 characters."}
                ]
            })
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to OpenRouter: {e}"
    except (KeyError, IndexError):
        return "Error: Could not parse the response from OpenRouter."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    """
    Main function to run the T-Mobile feed simulator.
    """
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("--- T-Mobile Customer Experience Feed ---")
        tweet = generate_tweet()
        print(f"-> {tweet}")
        print("\n---         Updating in 5 seconds         ---")
        time.sleep(5)

if __name__ == "__main__":
    main()
