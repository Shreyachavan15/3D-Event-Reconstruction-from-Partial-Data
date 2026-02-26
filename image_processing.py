import json
import torch
from PIL import Image
from datetime import datetime
from ultralytics import YOLO
from transformers import CLIPProcessor, CLIPModel

yolo = YOLO("yolov8n.pt")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def analyze_image(image_path: str):

    image = Image.open(image_path).convert("RGB")

    results = yolo(image)

    objects = []

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        label = yolo.names[cls_id]
        conf = float(box.conf[0])

        objects.append({
            "label": label,
            "confidence": round(conf, 2)
        })

    return {
        "type": "image_event",
        "image_file": image_path,
        "objects": objects,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    result = analyze_image("image.jpg")

    with open("image_investigation.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("✅ Saved image_investigation.json")
