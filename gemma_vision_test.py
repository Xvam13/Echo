# gemma_vision_test.py (The Final Test)

import requests
import json
import base64

OLLAMA_URL = 'http://localhost:11434/api/generate'
# Use the image most likely to succeed.
IMAGE_FILE_PATH = 'test_real_damage.jpg' 
PROMPT_TEXT = "Describe this image."

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

print("--- Final Gemma Vision Test (gemma:7b) ---")
base64_image = image_to_base64(IMAGE_FILE_PATH)

if base64_image:
    print("-> Image encoded.")
    # THE ONLY CHANGE IS THE MODEL NAME HERE
    payload = {
        "model": "gemma:7b",  # Testing the 7b model
        "prompt": PROMPT_TEXT,
        "images": [base64_image],
        "stream": False
    }

    print("-> Sending prompt and image to gemma:7b...")
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        ai_analysis = response_data['response']

        print("\n--- Gemma 7b's Analysis ---")
        print(ai_analysis)

    except Exception as e:
        print(f"\n--- An Error Occurred: {e}")
else:
    print("-> Could not encode image. Please check the file path and name.")