import json

timeline = []

# Image event
timeline.append({
    "time": "00:00",
    "type": "image",
    "description": "Objects detected in image",
    "data": ["car", "person"]
})

# Video event
timeline.append({
    "time": "00:03",
    "type": "video",
    "description": "Car stopped on the road",
    "data": ["car", "road"]
})

# Audio event
with open("audio_text.txt", "r", encoding="utf-8") as f:
    audio_text = f.read()

timeline.append({
    "time": "00:05",
    "type": "audio",
    "description": "Speech detected",
    "data": audio_text
})

# Text event
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = f.read().splitlines()

timeline.append({
    "time": "00:06",
    "type": "text",
    "description": "Keywords extracted",
    "data": keywords
})

# Save timeline to JSON
with open("reliveai_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, indent=4)

print("Timeline created successfully!")
