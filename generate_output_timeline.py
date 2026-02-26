import torch
from diffusers import AnimateDiffPipeline, MotionAdapter

print("Loading AnimateDiff...")

adapter = MotionAdapter.from_pretrained(
    "guoyww/animatediff-motion-adapter-v1-5-2",
    torch_dtype=torch.float16
)

pipe = AnimateDiffPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    motion_adapter=adapter,
    torch_dtype=torch.float16
)

pipe.to("cuda")   


import json
import torch
from diffusers import AnimateDiffPipeline, MotionAdapter
import imageio
import os


OUTPUT_FOLDER = "timeline_animation"
FRAMES_PER_SCENE = 16
HEIGHT = 512
WIDTH = 512

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


with open("timeline_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

timeline = data["timeline"]


print("Loading AnimateDiff model...")

adapter = MotionAdapter.from_pretrained(
    "guoyww/animatediff-motion-adapter-v1-5-2",
    torch_dtype=torch.float16
)

pipe = AnimateDiffPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    motion_adapter=adapter,
    torch_dtype=torch.float16
)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)

print(f"Using device: {device}")



scene_index = 0
video_frames = []

for event in timeline:
    source = event["source"]
    content = event["data"]

    if source == "image":
        objects = list(set(obj["label"] for obj in content["objects"]))
        prompt = f"2D animation of a busy city street with {', '.join(objects)}, moving traffic, cartoon style"

    elif source == "audio":
        prompt = "2D animation of people talking in a public square, emotional conversation, cartoon style"

    elif source == "text":
        prompt = "2D animation of a boy running in a park in the evening, police arriving, dramatic scene"

    elif source == "video":
        prompt = "2D animation of multiple people walking outdoors, dynamic scene, cinematic cartoon style"

    else:
        prompt = "2D animated scene"

    print(f"\nGenerating Scene {scene_index+1}")
    print("Prompt:", prompt)

    result = pipe(
        prompt=prompt,
        num_frames=FRAMES_PER_SCENE,
        height=HEIGHT,
        width=WIDTH,
        num_inference_steps=25,
        guidance_scale=7.5
    )

    frames = result.frames[0]

    for i, frame in enumerate(frames):
        frame_path = os.path.join(
            OUTPUT_FOLDER,
            f"scene_{scene_index:02d}_frame_{i:03d}.png"
        )
        frame.save(frame_path)

        video_frames.append(frame)

    scene_index += 1


imageio.mimsave(
    os.path.join(OUTPUT_FOLDER, "reliveai_animated_timeline.gif"),
    video_frames,
    fps=8
)

print("\n✅ FULL 2D Animated Timeline Generated!")