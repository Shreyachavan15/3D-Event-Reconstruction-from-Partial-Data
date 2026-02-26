import whisper
import json
from datetime import datetime
from analyze_text import analyze_text
model = whisper.load_model("base")

def analyze_audio(audio_path: str):
    result = model.transcribe(audio_path)
    transcript = result["text"].strip()

    text_analysis = analyze_text(transcript)

    text_analysis.update({
        "type": "audio_event",
        "transcript": transcript,
        "audio_file": audio_path,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return text_analysis

if __name__ == "__main__":
    result = analyze_audio("audio.wav")

    with open("audio_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("✅ Saved audio_output.json")
