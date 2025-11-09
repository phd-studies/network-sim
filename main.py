import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_tweet_with_gemini():
    """
    Generates a tweet about T-Mobile customer experience using the Gemini model.
    """
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not found in .env file."

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            data=json.dumps({
                "model": "google/gemini-2.5-flash",
                "messages": [
                    {"role": "user", "content": "Write a short, realistic tweet about a customer's experience with T-Mobile, either positive or negative. Keep it under 280 characters."}
                ]
            })
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to OpenRouter: {e}"
    except (KeyError, IndexError):
        return "Error: Could not parse response from OpenRouter."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def classify_tweet_with_nemotron(tweet_text):
    """
    Classifies the sentiment of a tweet using the Nemotron model.
    """
    if not OPENROUTER_API_KEY:
        return "Classification Error: API key not found."

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

        # Log the tweet and sentiment to a file
        with open("tweet_log.txt", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [Sentiment: {sentiment}] {new_tweet_content}\n")

        tweets.insert(0, (new_tweet_content, sentiment))

        # Limit the number of tweets to 4
        if len(tweets) > 4:
            tweets.pop()

        for content, sentiment in tweets:
            print(f"-> {content}\n   [Sentiment: {sentiment}]\n")

        print("---         Updating in 30 seconds         ---")
        time.sleep(30)

if __name__ == "__main__":
    main()
