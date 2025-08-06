# server.py (The Upgraded v3.0 with Triage Mode)

# Import our necessary tools
import socket
import requests 
import json     

# --- Server Configuration ---
HOST = '127.0.0.1'
PORT = 65432
OLLAMA_URL = 'http://localhost:11434/api/generate'

# --- AI HELPER FUNCTIONS ---

# AI Tool #1: The Translator
def get_ai_translation(text_to_translate):
    print(f"-> Sending to AI for translation: '{text_to_translate}'")
    prompt = f"Translate the following text into clear, modern English. Provide only the translation, no extra commentary. Here is the text: '{text_to_translate}'"
    payload = {"model": "gemma:2b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data['response'].strip()
    except Exception as e:
        print(f"!!! AI TRANSLATION ERROR: {e}")
        return "AI translator is currently unavailable."

# AI Tool #2: The Triage Assistant
def get_ai_triage_summary(emergency_message):
    print(f"-> Sending to AI for triage: '{emergency_message}'")
    prompt = f"""
You are a First Responder Triage Assistant AI. Analyze the following emergency message and create a structured report. 
Do not give advice. Do not add any commentary. Just report the facts in this exact format:
- LOCATION: [Where is the person? If unknown, state 'Unknown'.]
- INJURIES: [What injuries are reported? If none, state 'None Reported'.]
- STATUS: [Is the person trapped, conscious, etc.?]
- IMMEDIATE HAZARDS: [Are there any dangers like fire, water, structural damage? If none, state 'None Reported'.]
- URGENCY: [Rate as Low, Medium, High, or Critical based on the message.]

Here is the message to analyze: "{emergency_message}"
"""
    payload = {"model": "gemma:2b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data['response'].strip()
    except Exception as e:
        print(f"!!! AI TRIAGE ERROR: {e}")
        return "AI triage assistant is currently unavailable."

# --- MAIN SERVER LOGIC ---
print("--- MeshMessenger Server v3.0 (with Triage AI) is starting ---")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print("Client disconnected.")
                break
            print(f"Received from client: '{data}'")

            # --- THE "MANAGER" LOGIC with THREE MODES ---
            if data.startswith("/translate "):
                text_to_process = data.removeprefix("/translate ")
                final_reply = get_ai_translation(text_to_process)
            
            elif data.startswith("/triage "):
                text_to_process = data.removeprefix("/triage ")
                final_reply = get_ai_triage_summary(text_to_process)

            else: # Normal Mode
                final_reply = data 

            # Send the final reply back to the client.
            conn.sendall(final_reply.encode('utf-8'))

print("--- Server is closing ---")
