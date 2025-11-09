import os
import time
import requests
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure APIs
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_tweet_with_gemini():
    """
    Generates a tweet about T-Mobile customer experience using the Gemini SDK.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in .env file."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Write a short, realistic tweet about a customer's experience with T-Mobile, either positive or negative. Keep it under 280 characters.")
        return response.text.strip()
    except Exception as e:
        return f"An unexpected error occurred with the Gemini API: {e}"

def classify_tweet_with_nemotron(tweet_text):
    """
    Classifies the sentiment of a tweet using the Nemotron model via OpenRouter.
    """
    if not OPENROUTER_API_KEY:
        return "Classification Error: OPENROUTER_API_KEY not found."

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            data=json.dumps({
                "model": "nvidia/nemotron-nano-9b-v2",
                "messages": [
                    {"role": "user", "content": f"Classify the following tweet as 'positive', 'negative', or 'neutral'. Tweet: \"{tweet_text}\""}
                ]
            })
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Classification Error: {e}"
    except (KeyError, IndexError):
        return "Classification Error: Could not parse response."
    except Exception as e:
        return f"An unexpected classification error occurred: {e}"

def main():
    """
    Main function to run the T-Mobile feed simulator.
    """
    tweets = []
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("--- T-Mobile Customer Experience Feed ---")

        new_tweet_content = generate_tweet_with_gemini()
        sentiment = "N/A"
        if "Error:" not in new_tweet_content:
            sentiment = classify_tweet_with_nemotron(new_tweet_content)

        with open("tweet_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [Sentiment: {sentiment}] {new_tweet_content}\n")

        tweets.insert(0, (new_tweet_content, sentiment))

        if len(tweets) > 4:
            tweets.pop()

        for content, sentiment in tweets:
            print(f"-> {content}\n   [Sentiment: {sentiment}]\n")

        print("---         Updating in 30 seconds         ---")
        time.sleep(30)

if __name__ == "__main__":
    main()
