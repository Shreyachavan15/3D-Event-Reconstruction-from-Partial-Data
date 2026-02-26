import imageio
import os

folder = "timeline_animation"
output_video = "final_timeline.mp4"

frames = []

# Sort files properly
files = sorted([f for f in os.listdir(folder) if f.endswith(".png")])

for file in files:
    path = os.path.join(folder, file)
    frames.append(imageio.imread(path))

# Create video (fps = 8, you can change)
imageio.mimsave(output_video, frames, fps=8)

print("✅ Video created: final_timeline.mp4")