#!/bin/bash
# Generate carousel GIF from all images in img/ folder
# Usage: ./scripts/gen-gif.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
IMG_DIR="$REPO_DIR/img"
OUTPUT_GIF="$IMG_DIR/carousel.gif"

cd "$REPO_DIR"

echo "🎬 Generating carousel GIF from images in $IMG_DIR..."

python3 << 'EOF'
import os
import sys
from PIL import Image
import glob

img_dir = os.environ.get('IMG_DIR', 'img')
output_gif = os.environ.get('OUTPUT_GIF', 'img/carousel.gif')

# Find all image files
image_patterns = ['*.png', '*.jpg', '*.jpeg', '*.webp', '*.gif']
image_files = []

for pattern in image_patterns:
    image_files.extend(glob.glob(os.path.join(img_dir, pattern)))

# Filter out the carousel.gif itself
image_files = [f for f in image_files if not f.endswith('carousel.gif')]

# Custom order if specified, otherwise alphabetical
custom_order = os.environ.get('IMAGE_ORDER', '').split(',')
if custom_order and custom_order[0]:
    # Sort by custom order
    ordered_files = []
    for name in custom_order:
        name = name.strip()
        for img_file in image_files:
            if name in os.path.basename(img_file):
                ordered_files.append(img_file)
                break
    # Add any remaining files not in custom order
    for img_file in image_files:
        if img_file not in ordered_files:
            ordered_files.append(img_file)
    image_files = ordered_files
else:
    image_files = sorted(image_files)  # Sort alphabetically by default

if not image_files:
    print(f"❌ No images found in {img_dir}")
    sys.exit(1)

print(f"📸 Found {len(image_files)} images:")
for img in image_files:
    print(f"  - {os.path.basename(img)}")

# Load and crop all images from center (no distortion)
target_width = 900
target_height = 188
images = []

for img_file in image_files:
    try:
        img = Image.open(img_file).convert('RGB')
        original_width, original_height = img.size
        
        # Calculate aspect ratios
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        
        # Resize to fit one dimension, then crop the other
        if original_ratio > target_ratio:
            # Image is wider - fit height, crop width
            new_height = target_height
            new_width = int(original_width * (target_height / original_height))
        else:
            # Image is taller - fit width, crop height  
            new_width = target_width
            new_height = int(original_height * (target_width / original_width))
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop from center
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        img = img.crop((left, top, right, bottom))
        images.append(img)
        print(f"✓ Loaded & cropped: {os.path.basename(img_file)} ({original_width}x{original_height} → {target_width}x{target_height})")
    except Exception as e:
        print(f"⚠️  Failed to load {os.path.basename(img_file)}: {e}")

if not images:
    print("❌ No images could be loaded")
    sys.exit(1)

print(f"\n🎨 Creating carousel with {len(images)} images...")

frames = []

# For each image
for idx, current_img in enumerate(images):
    # Show current image for 5 seconds (25 frames at 200ms = 5s)
    for i in range(25):
        frames.append(current_img.copy())
    
    # Smooth slide to next image (10 frames = 2 seconds)
    next_img = images[(idx + 1) % len(images)]
    
    for i in range(10):
        alpha = i / 10
        offset = int(900 * alpha)
        
        frame = Image.new('RGB', (900, 188), (0, 0, 0))
        
        # Slide current image to the left
        if offset < 900:
            frame.paste(current_img.crop((offset, 0, 900, 188)), (0, 0))
        
        # Slide next image from right
        if offset > 0:
            frame.paste(next_img.crop((0, 0, offset, 188)), (900 - offset, 0))
        
        frames.append(frame)

print(f"💾 Saving GIF with {len(frames)} frames to {output_gif}...")

# Save as GIF
frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    duration=200,  # 200ms per frame
    loop=0,
    optimize=True,
    quality=85
)

# Get file size
file_size = os.path.getsize(output_gif)
size_mb = file_size / (1024 * 1024)

print(f"\n✅ Carousel created successfully!")
print(f"📦 File: {output_gif}")
print(f"📏 Size: {size_mb:.2f} MB")
print(f"🎞️  Frames: {len(frames)}")
print(f"⏱️  Duration: ~{len(frames) * 0.2:.0f} seconds per loop")
print(f"\n🎬 Images rotate every 5 seconds with 2-second smooth slide transitions!")

EOF

echo ""
echo "🎉 Done! Your carousel is ready at $OUTPUT_GIF"
