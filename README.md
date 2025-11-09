# T-Mobile Feed Simulator

This project simulates a social media feed of customer experiences with T-Mobile, using an AI-driven, agent-based architecture.

## Architecture

This simulator uses two AI models in a router-agent setup:

1.  **Nemotron (Router):** The `nvidia/nemotron-nano-9b-v2` model, accessed via the OpenRouter API, acts as a dispatcher. Every 30 seconds, it chooses which type of tweet(s) to generate, selecting between one and three of the following sentiments: "positive", "negative", or "neutral".

2.  **Gemini (Agent):** The `gemini-1.5-flash` model, accessed directly via the Google Gemini SDK, acts as the content generation agent. Based on the choice(s) from the Nemotron router, it will generate a tweet for each selected sentiment.

## Features

*   **AI-Powered Dispatcher:** Nemotron dynamically decides the sentiment of the feed at each update.
*   **Targeted Content Generation:** Gemini creates tweets based on the dispatcher's instructions.
*   **Live Feed:** Displays up to 3 new tweets every 30 seconds, showing only the latest generated content.
*   **Logging:** The chosen sentiments and the resulting tweets from each cycle are logged to `tweet_log.txt`.

## Setup

1.  **Clone the repository.**
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Create a `.env` file** in the root directory and add your API keys:
    ```
    OPENROUTER_API_KEY=your_openrouter_api_key_here
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

## Running the Simulator

To start the feed simulator, run the `main.py` script:

```bash
python3 main.py
```
