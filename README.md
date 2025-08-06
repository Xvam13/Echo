# Echo: Your SOS, Amplified

**A privacy-first, offline-capable emergency response app powered by on-device AI. Submission for the Google - The Gemma 3n Impact Challenge.**

---

### The Mission: Ending the Silence of Crisis

This project was born from personal experience. I have lived through the terrifying silence of a communications blackout during wars and revolutions. My friends and colleagues have experienced the same helpless isolation during natural disasters like the recent earthquake in Turkey. When the lines go down, people are left trapped and unheard.

**Echo was built to break that silence.** It is designed to be a universal lifeline, so simple a child could use it, because in a crisis, simplicity is survival.

---

### What It Does

Echo is an intelligent triage and support engine that works when nothing else does. By leveraging a simulated peer-to-peer connectivity layer, it connects victims directly to nearby rescuers or other civilians—**all without needing internet or mobile service.**

When a user is completely alone, Echo's **"Lone Survivor" mode** activates, transforming the on-device AI into a calm and reassuring **AI Survival Coach**.

### Core AI Features

Powered by Google's `gemma:2b` model running locally via Ollama, and a local Whisper AI model for transcription, Echo's on-device intelligence pipeline can:

*   🎤 **Transcribe Voice:** Instantly converts panicked, multilingual voice messages into text right on the device.
*   🧠 **Triage Emergencies:** Analyzes transcribed voice messages to generate structured, actionable reports for rescuers, extracting location, injuries, status, and urgency.
*   🌐 **Translate Languages:** "Silently" translates messages, breaking down language barriers between victims and responders.
*   ❤️ **Provide AI Coaching:** In "Lone Survivor" mode, provides calming guidance and support to keep a user safe and hopeful until help arrives.

---

### Technology Stack

*   **Backend & Prototyping:** Python
*   **Local LLM Server:** Ollama
*   **Core AI Models:** Google Gemma 3n (`gemma:2b`), OpenAI Whisper (`base`)
*   **UI Framework:** Gradio
*   **Core Libraries:** `requests`, `json`

### How to Run This Prototype

1.  **Prerequisites:**
    *   Ensure you have Python 3.10+ installed and added to your system PATH.
    *   Ensure you have [Ollama](https://ollama.com/) installed and running.

2.  **Download AI Models:**
    *   In your terminal, pull the necessary models:
        ```bash
        ollama pull gemma:2b
        ```

3.  **Clone the Repository:**
    *   `git clone https://github.com/YourUsername/YourRepoName.git`
    *   `cd YourRepoName`

4.  **Install Dependencies:**
    *   Install the required Python libraries:
        ```bash
        pip install -r requirements.txt
        ```
    *   *(Note: You will need to create a `requirements.txt` file)*

5.  **Run the Application:**
    *   Place a test audio file named `test_audio_ar.mp3` in the root folder.
    *   Run the main application script:
        ```bash
        python final_app.py
        ```
    *   Open the local URL provided in your terminal (e.g., `http://127.0.0.1:7860`) in a web browser.

---