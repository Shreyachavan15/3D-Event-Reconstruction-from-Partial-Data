import json
from datetime import datetime
import sys


def load_json(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_name}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format in: {file_name}")
        print(f"   Error: {e}")
        print("   👉 Fix this file before integration.")
        sys.exit(1)


text_event  = load_json("text_output.json")
audio_event = load_json("audio_output.json")
image_event = load_json("image_investigation.json")
video_event = load_json("video_output.json")


def normalize(event, source):
    return {
        "source": source,
        "timestamp": event.get(
            "timestamp",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        "data": event
    }

timeline_events = [
    normalize(text_event, "text"),
    normalize(audio_event, "audio"),
    normalize(image_event, "image"),
    normalize(video_event, "video")
]


timeline_events.sort(key=lambda x: x["timestamp"])


final_timeline = {
    "case_id": "reliveai_case_001",
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "timeline": timeline_events
}


with open("timeline_output.json", "w", encoding="utf-8") as f:
    json.dump(final_timeline, f, indent=4, ensure_ascii=False)

print("✅ Timeline generated successfully!")
print("📁 Output file: timeline_output.json")
