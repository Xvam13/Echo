# client.py (Upgraded v2.0 with Voice Transcription "Ears")

import socket
import whisper # We now need the whisper library here!

# --- Configuration ---
HOST = '127.0.0.1' 
PORT = 65432
# --- IMPORTANT: Make sure this is the exact name of your audio file ---
AUDIO_FILE_TO_TRANSCRIBE = "test_audio_ar.mp3" 

# --- AI Helper Function (for the Client) ---
# This is our new "Ear". Its job is to transcribe the audio file.
def transcribe_audio_file():
    """
    Loads the Whisper model, transcribes the specified audio file, and returns the text.
    """
    print("-> Client: Loading transcription model...")
    # Using the same small 'base' model as our test.
    model = whisper.load_model("base")
    print("-> Client: Model loaded. Starting transcription...")

    try:
        # This is the command that does the actual work.
        result = model.transcribe(AUDIO_FILE_TO_TRANSCRIBE, language='ar')
        transcribed_text = result["text"]
        print(f"-> Client: Transcription successful. AI heard: '{transcribed_text}'")
        return transcribed_text
    except Exception as e:
        print(f"!!! CLIENT ERROR: Could not transcribe audio. {e}")
        return "" # Return an empty string if it fails


# --- Main Client Logic ---
print("--- MeshMessenger Client v2.0 is starting ---")
print("Type a normal message, or:")
print("  '/translate [text]' to translate")
print("  '/triage [text]' for triage summary")
print("  '!voice' to simulate sending a voice message for triage")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"--- Connected to server at {HOST}:{PORT} ---")

    while True:
        # Get input from the user.
        message = input("Your command: ")

        # --- NEW CLIENT-SIDE LOGIC ---
        # We check for a new special command: '!voice'
        # We use '!' to show this is a command for the CLIENT, not the server.
        if message == "!voice":
            # 1. Transcribe the audio file to get the text.
            heard_text = transcribe_audio_file()

            # 2. If transcription was successful...
            if heard_text:
                # 3. Format it as a /triage command for the server.
                message_to_send = f"/triage {heard_text}"
                print(f"-> Client: Sending this to server: '{message_to_send}'")
                s.sendall(message_to_send.encode('utf-8'))
            else:
                print("-> Client: Skipping send because transcription failed.")
                continue # Go back to the start of the loop
        
        else:
            # If it's any other command, just send it directly to the server.
            s.sendall(message.encode('utf-8'))
        
        # Wait to receive the server's final reply.
        data = s.recv(1024).decode('utf-8')
        print(f"Server replied: {data}")

print("--- Client is closing ---")