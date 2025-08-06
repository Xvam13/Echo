# final_app.py - FINAL STABLE VERSION

import gradio as gr
import time
import requests
import json
import whisper

# --- 1. AI ENGINE & CONFIGURATION ---
OLLAMA_URL = 'http://localhost:11434/api/generate'
AUDIO_FILE_TO_TRANSCRIBE = "test_audio_ar.mp3" # Ensure this file is in your folder

def get_ai_triage_summary(emergency_message):
    prompt = f"""<start_of_turn>system
You are “Echo-Triage”, an on-device rescue assistant.
INTERNAL METHOD (never reveal):
1. Read the full user message—even if panicked or misspelled.
2. Extract → LOCATION · INJURIES · STATUS · IMMEDIATE HAZARDS.
3. Infer URGENCY: Low | Medium | High | Critical
      – Critical if life-threatening injuries OR fire/gas/structural collapse.
      – High if serious injuries OR trapped with hazards.
      – Medium if minor injuries OR trapped without hazards.
      – Low if no injuries & no hazards.
4. If a field is missing, write “Not Specified” (or “None Specified” for injuries/hazards).
5. Think silently step-by-step, then output ONLY this bullet list (nothing else):
- Location: …
- Injuries: …
- Status: …
- Hazards: …
- Urgency: …
<end_of_turn><start_of_turn>user
{emergency_message}
<end_of_turn><start_of_turn>model
"""
    payload = {"model": "gemma:2b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()['response'].strip()
    except Exception as e:
        print(f"AI TRIAGE ERROR: {e}")
        return "Error: AI triage assistant is unavailable."

def get_ai_translation(text_to_translate):
    prompt = f"""<start_of_turn>system
You are a "Silent Translator", a highly accurate and efficient translation tool.
INTERNAL METHOD (never reveal):
1. Read the full user text, which may contain typos or grammatical errors.
2. Silently identify the user's likely intended meaning, correcting any clear spelling mistakes.
3. Translate the corrected text into modern, fluent English.
4. Output ONLY the raw translated text.
<end_of_turn><start_of_turn>user
{text_to_translate}
<end_of_turn><start_of_turn>model
"""
    payload = {"model": "gemma:2b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()['response'].strip()
    except Exception as e:
        print(f"AI TRANSLATION ERROR: {e}")
        return "Error: AI translator is unavailable."

def get_ai_coach_response(user_input, history):
    prompt = f"""<start_of_turn>system
You are an AI Survival Coach. The user is trapped and alone. Your goal is to keep them calm, help them assess their situation safely, and provide encouragement. Keep responses concise and supportive. Respond to the user's latest message.
<end_of_turn><start_of_turn>user
{user_input}
<end_of_turn><start_of_turn>model
"""
    payload = {"model": "gemma:2b", "prompt": prompt, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        bot_response = response.json()['response'].strip()
        history.append((user_input, bot_response))
        return "", history
    except Exception as e:
        print(f"AI COACH ERROR: {e}")
        history.append((user_input, "I'm having trouble connecting right now. Let's just focus on staying calm."))
        return "", history
        
def transcribe_audio_file():
    model = whisper.load_model("base")
    result = model.transcribe(AUDIO_FILE_TO_TRANSCRIBE, language='ar')
    return result["text"]

# --- 2. UI LOGIC FUNCTIONS ---
def show_lobby():
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
def show_coach_or_chat(peer_name):
    if peer_name is None: # Bug fix for connecting to nothing
        return gr.update(), gr.update(), gr.update()
    if peer_name == "AI Survival Coach":
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
    else:
        new_header = f"### Secure Channel with: {peer_name}"
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True, value=new_header)
        
def user_sends_message(usr_msg, translate_toggle, history):
    if not usr_msg.strip(): return "", history
    history.append([usr_msg, None])
    yield "", history
    if translate_toggle:
        bot_response = get_ai_translation(usr_msg)
    else:
        bot_response = None
    if bot_response:
        history[-1][1] = bot_response
    yield "", history

def sos_button_click(history):
    history.append(("[SOS Voice Triage Activated]", "...Transcribing audio..."))
    yield history
    transcribed = transcribe_audio_file()
    history[-1][1] = f"...Transcribed: '{transcribed}'\n\nGenerating report..."
    yield history
    report = get_ai_triage_summary(transcribed)
    history[-1][1] = report
    yield history

# --- 3. THE GRADIO UI LAYOUT ---
with gr.Blocks(theme=gr.themes.Monochrome(primary_hue="red", secondary_hue="pink"), title="Echo") as app:
    # --- SCREEN 1: DASHBOARD ---
    with gr.Column(visible=True) as dashboard_screen:
        gr.Markdown("<h1 style='text-align: center;'>Echo</h1><p style='text-align:center;'>Your SOS, Amplified.</p>")
        scan_button = gr.Button("Scan for Nearby Devices", variant="primary")

    # --- SCREEN 2: LOBBY ---
    with gr.Column(visible=False) as lobby_screen:
        gr.Markdown("<h2 style='text-align: center;'>Available Connections</h2>")
        peer_list = gr.Radio(
            ["Red Crescent Team 1", "Civil Defense Unit 7", "Person 1 (20m away)", "AI Survival Coach"], 
            label="Select a connection from the list below"
        )
    
    # --- SCREEN 3: CHAT SCREEN ---
    with gr.Column(visible=False) as chat_screen:
        chat_header = gr.Markdown("### Secure Channel")
        chatbot = gr.Chatbot(bubble_full_width=True, height=450)
        
        with gr.Tab("Rescuer Chat"):
            sos_button = gr.Button("🔴 Triage SOS (Sends Voice Message)", variant="stop")
            with gr.Row():
                text_input = gr.Textbox(placeholder="Type normal message here...", scale=3)
                send_button = gr.Button("Send")
            translate_checkbox = gr.Checkbox(label="Translate normal message")

        with gr.Tab("AI Survival Coach"):
            coach_chatbot = gr.Chatbot(bubble_full_width=True, height=450)
            with gr.Row():
                coach_text = gr.Textbox(placeholder="Talk to your coach...", scale=3)
                coach_send_button = gr.Button("Send", variant="primary")
                
    # --- 4. UI WIRING ---
    scan_button.click(fn=show_lobby, outputs=[dashboard_screen, lobby_screen, chat_screen])
    peer_list.select(fn=show_coach_or_chat, inputs=peer_list, outputs=[dashboard_screen, lobby_screen, chat_screen])

    sos_button.click(fn=sos_button_click, inputs=chatbot, outputs=chatbot)
    send_button.click(fn=user_sends_message, inputs=[text_input, translate_checkbox, chatbot], outputs=[text_input, chatbot])
    text_input.submit(fn=user_sends_message, inputs=[text_input, translate_checkbox, chatbot], outputs=[text_input, chatbot])
    
    coach_send_button.click(fn=get_ai_coach_response, inputs=[coach_text, coach_chatbot], outputs=[coach_text, coach_chatbot])
    coach_text.submit(fn=get_ai_coach_response, inputs=[coach_text, coach_chatbot], outputs=[coach_text, coach_chatbot])
    
app.launch(share=True)
