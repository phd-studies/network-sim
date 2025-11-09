import os
import time
import requests
import json
import random
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure APIs
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_positive_tweet(history):
    return generate_tweet_with_gemini("a positive", history)

def generate_negative_tweet(history):
    return generate_tweet_with_gemini("a negative", history)

def generate_neutral_tweet(history):
    return generate_tweet_with_gemini("a neutral or informational", history)

def generate_tweet_with_gemini(sentiment_prompt, history):
    """
    Generates a tweet about T-Mobile customer experience using the Gemini SDK, avoiding previous tweets.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in .env file."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        history_prompt = ""
        if history:
            history_prompt = "Do not repeat any of the following tweets:\n- " + "\n- ".join(history)

        prompt = f"Write a short, realistic tweet about a customer's {sentiment_prompt} experience with T-Mobile. Keep it under 280 characters. {history_prompt}"
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
                "model": "nvidia/nemotron-3-8b-instruct",
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

        num_tweets_to_generate = random.randint(2, 6)
        chosen_agents = choose_agents_with_nemotron()
        generated_tweets = []

        if "Error:" in chosen_agents[0]:
            print(f"-> [Error] {chosen_agents[0]}\n")
            generated_tweets.append(("error", chosen_agents[0]))
        else:
            for i in range(num_tweets_to_generate):
                agent_choice = random.choice(chosen_agents)
                if agent_choice in agent_functions:
                    # Pass the list of already generated tweets in this batch to the generation function
                    tweet_history = [tweet for _, tweet in generated_tweets]
                    tweet = agent_functions[agent_choice](tweet_history)
                    generated_tweets.append((agent_choice, tweet))
                    print(f"-> [{agent_choice.capitalize()}] {tweet}\n")
                else:
                    error_msg = f"Invalid agent choice from Nemotron: {agent_choice}"
                    generated_tweets.append(("error", error_msg))
                    print(f"-> [Error] {error_msg}\n")

        with open("tweet_log.txt", "a", encoding="utf-8") as f:
            log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Chosen Agents: {', '.join(chosen_agents)} | Generating {num_tweets_to_generate} tweets\n"
            for agent, tweet in generated_tweets:
                log_entry += f"  - [{agent.capitalize()}]: {tweet}\n"
            f.write(log_entry + "\n")

        print(f"---         Updating in 15 seconds         ---")
        time.sleep(15)

if __name__ == "__main__":
    main()
