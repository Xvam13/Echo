# image_test.py (Dual-Purpose Test - Environmental Analysis)

import requests
import json
import base64

# --- Configuration ---
OLLAMA_URL = 'http://localhost:11434/api/generate'

# --- Make sure this matches your image file's name ---
IMAGE_FILE_PATH = 'C2.png' 

# --- NEW PROMPT: Focused on the ENVIRONMENT ---
# We are asking the AI to be a structural safety expert, not a medic.
PROMPT_TEXT = """
You are a structural safety inspector. Analyze only the environment in the attached image.
Do not describe or mention any people in the photo.
Describe any visible environmental hazards or materials in a bulleted list. Examples: 'cracked concrete', 'exposed rebar', 'dusty air', 'piled debris'.
"""

# --- Image Encoding Function (This stays the same) ---
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# --- Main Test Logic ---
print("--- Gemma Environmental Hazard Test ---")
print(f"-> Loading and encoding image: {IMAGE_FILE_PATH}")

base64_image = image_to_base64(IMAGE_FILE_PATH)

if base64_image:
    print("-> Image encoded successfully.")
    
    # We create the multimodal payload
    payload = {
        "model": "gemma:2b",
        "prompt": PROMPT_TEXT,
        "images": [base64_image],
        "stream": False
    }

    print("-> Sending Hazard prompt and image to Gemma...")
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        ai_analysis = response_data['response']

        print("\n--- AI ENVIRONMENTAL ANALYSIS ---")
        print(ai_analysis)

    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(f"Error during API call: {e}")
else:
    print("-> Could not encode image. Please check the file path and name.")