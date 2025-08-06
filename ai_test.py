# ai_test.py

# Import the libraries we need. 'requests' to talk to Ollama, 'json' for data format.
import requests
import json

# --- Configuration ---
# This is the address where our local Ollama AI server is listening.
OLLAMA_URL = 'http://localhost:11434/api/generate'

# The instructions we want to send to our AI.
PROMPT_TEXT = "Translate the following English text to French: 'Hello, how are you today?'"

# --- The API Request ---
# We package our request in a dictionary.
# IMPORTANT: We are telling it to use the 'gemma:2b' model which we know runs on your computer.
payload = {
    "model": "gemma:2b",        # The smaller model
    "prompt": PROMPT_TEXT,
    "stream": False             # We want the answer all at once.
}

print("--- Sending prompt to Gemma ---")
print(f"Prompt: {PROMPT_TEXT}")

# --- Sending the Request & Getting the Response ---
try:
    # Send the data to the Ollama server and wait for a reply.
    response = requests.post(OLLAMA_URL, json=payload)
    
    # Check if the server reported an error (like a '404 Not Found').
    response.raise_for_status() 

    # Take the raw text of the response and parse it as JSON data.
    response_data = response.json()
    
    # The AI's actual answer is inside a dictionary key called 'response'.
    ai_answer = response_data['response']

    print("\n--- Gemma's Response ---")
    print(ai_answer)

except requests.exceptions.RequestException as e:
    # This block will run if we can't connect to Ollama at all.
    print(f"\n--- An Error Occurred ---")
    print(f"Could not connect to Ollama. Make sure it is running. Error: {e}")