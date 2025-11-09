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

def generate_positive_tweet():
    return generate_tweet_with_gemini("a positive")

def generate_negative_tweet():
    return generate_tweet_with_gemini("a negative")

def generate_neutral_tweet():
    return generate_tweet_with_gemini("a neutral or informational")

def generate_tweet_with_gemini(sentiment_prompt):
    """
    Generates a tweet about T-Mobile customer experience using the Gemini SDK.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in .env file."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Write a short, realistic tweet about a customer's {sentiment_prompt} experience with T-Mobile. Keep it under 280 characters."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An unexpected error occurred with the Gemini API: {e}"

def choose_agents_with_nemotron():
    """
    Uses Nemotron to choose which type of tweets to generate.
    """
    if not OPENROUTER_API_KEY:
        return ["Error: OPENROUTER_API_KEY not found."]

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            data=json.dumps({
                "model": "nvidia/nemotron-nano-9b-v2",
                "messages": [
                    {"role": "user", "content": "You are a dispatcher. Choose between one and three of the following options: 'positive', 'negative', 'neutral'. Return your choices as a simple comma-separated list. For example: 'positive, negative' or 'neutral'."}
                ]
            })
        )
        response.raise_for_status()
        data = response.json()
        choices = data['choices'][0]['message']['content'].strip().lower().split(',')
        return [choice.strip() for choice in choices]
    except Exception as e:
        return [f"An unexpected error occurred with the Nemotron API: {e}"]

def main():
    """
    Main function to run the T-Mobile feed simulator.
    """
    agent_functions = {
        "positive": generate_positive_tweet,
        "negative": generate_negative_tweet,
        "neutral": generate_neutral_tweet
    }

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("--- T-Mobile Customer Experience Feed ---")

        chosen_agents = choose_agents_with_nemotron()
        generated_tweets = []

        for agent in chosen_agents:
            if agent in agent_functions:
                tweet = agent_functions[agent]()
                generated_tweets.append((agent, tweet))
                print(f"-> [{agent.capitalize()}] {tweet}\n")
            else:
                generated_tweets.append(("error", agent))
                print(f"-> [Error] Invalid agent choice from Nemotron: {agent}\n")

        with open("tweet_log.txt", "a", encoding="utf-8") as f:
            log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Chosen Agents: {', '.join(chosen_agents)}\n"
            for agent, tweet in generated_tweets:
                log_entry += f"  - [{agent.capitalize()}]: {tweet}\n"
            f.write(log_entry + "\n")

        print("---         Updating in 30 seconds         ---")
        time.sleep(30)

if __name__ == "__main__":
    main()
