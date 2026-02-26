import cv2
import whisper
import json
from ultralytics import YOLO
from datetime import datetime
from analyze_text import analyze_text

yolo = YOLO("yolov8n.pt")
whisper_model = whisper.load_model("base")

def analyze_video(video_path: str):

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    detected_objects = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = yolo(frame)

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = yolo.names[cls_id]
            conf = float(box.conf[0])

            detected_objects.append({
                "label": label,
                "confidence": round(conf, 2),
                "frame": frame_count
            })

        frame_count += 30

    cap.release()

    transcript = whisper_model.transcribe(video_path)["text"].strip()
    text_analysis = analyze_text(transcript)

    return {
        "type": "video_event",
        "video_file": video_path,
        "objects": detected_objects,
        "transcript": transcript,
        "text_analysis": text_analysis,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    result = analyze_video("video.mp4")

    with open("video_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("✅ Saved video_output.json")
