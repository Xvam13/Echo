# voice_test.py (Final Version with File Saving)

import whisper
import codecs # We import this helper for handling different text encodings

print("--- Whisper Arabic Voice Test ---")

print("-> Loading the 'base' AI model...")
model = whisper.load_model("base")
print("-> Model loaded successfully.")

# Make sure this filename matches your audio file
audio_file_path = "test_audio_ar.mp3" 

print(f"\n-> Transcribing the audio file: '{audio_file_path}'...")
result = model.transcribe(audio_file_path, language='ar')
transcribed_text = result["text"]

# --- THE NEW PART: SAVING THE RESULT ---
# We define the name of the file we want to save.
output_filename = "transcription_result.txt"

# 'with open' is the standard way to handle files in Python.
# 'w' means we are opening the file in 'write' mode.
# 'utf-8' is a crucial encoding that supports Arabic and almost all other languages.
with codecs.open(output_filename, 'w', "utf-8") as f:
    # We write the AI's transcribed text into the file.
    f.write(transcribed_text)
# --- END OF NEW PART ---


print("\n--- TRANSCRIPTION COMPLETE ---")
# We still print it to the terminal, even if it looks broken.
print("The AI heard the following text:")
print(f"'{transcribed_text}'")
print(f"\nSUCCESS: The correct result has been saved to the file '{output_filename}'")