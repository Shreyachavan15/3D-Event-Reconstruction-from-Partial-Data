import whisper

model = whisper.load_model("base")

result = model.transcribe("audio.wav")

print("Transcribed Text:")
print(result["text"])

with open("audio_text.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Audio processed successfully! Check audio_text.txt")
