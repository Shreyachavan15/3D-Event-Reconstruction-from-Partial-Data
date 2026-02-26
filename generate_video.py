import json
from moviepy import TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips


VIDEO_SIZE = (1280, 720)
DURATION_PER_SCENE = 5
FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FPS = 24


with open("timeline_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

timeline = data.get("timeline", [])
clips = []


for event in timeline:
    source = event.get("source", "unknown")
    timestamp = event.get("timestamp", "N/A")
    content = event.get("data", {})

    text_lines = [
        f"Source: {source.upper()}",
        f"Time: {timestamp}",
    ]

    if "summary" in content:
        text_lines.append(f"Summary: {content['summary']}")

    if "objects" in content:
        obj_list = list(set(obj["label"] for obj in content["objects"]))
        text_lines.append("Objects: " + ", ".join(obj_list))

    if "transcript" in content and content["transcript"]:
        text_lines.append(f"Transcript: {content['transcript'][:120]}...")

    final_text = "\n\n".join(text_lines)

    background = ColorClip(
        size=VIDEO_SIZE,
        color=(15, 15, 35),
        duration=DURATION_PER_SCENE
    )

    txt_clip = TextClip(
        text=final_text,
        font=FONT_PATH,
        font_size=30,
        color="white",
        size=VIDEO_SIZE,
        method="caption",
        duration=DURATION_PER_SCENE
    )

    scene = CompositeVideoClip(
        [background, txt_clip.with_position("center")],
        size=VIDEO_SIZE
    )

    clips.append(scene)


final_video = concatenate_videoclips(clips, method="compose")


final_video.write_videofile(
    "reliveai_2d_timeline.mp4",
    fps=FPS,
    codec="libx264",
    audio=False
)

print("✅ Video Generated Successfully!")
