# llava_test.py (A diagnostic test to check multimodal capabilities)

import requests
import json
import base64

OLLAMA_URL = 'http://localhost:11434/api/generate'
# Let's use the 'boring' image that is most likely to work.
# If you don't have it, any picture of an object will do.
IMAGE_FILE_PATH = 'test_real_damage.jpg' 
PROMPT_TEXT = "Describe what you see in this image."

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

print("--- LLaVA Diagnostic Test ---")
base64_image = image_to_base64(IMAGE_FILE_PATH)

if base64_image:
    print("-> Image encoded.")
    payload = {
        "model": "llava",  # We are using the LLaVA model!
        "prompt": PROMPT_TEXT,
        "images": [base64_image],
        "stream": False
    }

    print("-> Sending prompt and image to LLaVA...")
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        ai_analysis = response_data['response']

        print("\n--- LLaVA's Analysis ---")
        print(ai_analysis)

    except Exception as e:
        print(f"\n--- An Error Occurred: {e}")
else:
    print("-> Could not encode image. Please check the file path.")