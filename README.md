# T-Mobile Feed Simulator

This project simulates a social media feed of customer experiences with T-Mobile, using a dual-model approach with the OpenRouter API.

## Features

*   **Tweet Generation:** Uses the `google/gemini-2.5-flash` model to generate realistic tweets.
*   **Sentiment Analysis:** Uses the `nvidia/nemotron-nano-9b-v2` model to classify each tweet as positive, negative, or neutral.
*   **Live Feed:** Displays the last 4 tweets and their sentiment, updating every 30 seconds.
*   **Logging:** All generated tweets and their classifications are logged to `tweet_log.txt`.

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
5.  **Create a `.env` file** in the root directory and add your OpenRouter API key:
    ```
    OPENROUTER_API_KEY=your_api_key_here
    ```

## Running the Simulator

To start the feed simulator, run the `main.py` script:

```bash
python3 main.py
```
