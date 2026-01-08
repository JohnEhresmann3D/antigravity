#!/usr/bin/env python3
"""Convert black background to transparent"""

from PIL import Image

def black_to_transparent(input_path, output_path):
    """Convert black pixels to transparent"""
    print(f"Converting: {input_path}")
    
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    width, height = img.size
    
    # Convert black (and near-black) to transparent
    threshold = 30  # Pixels darker than this become transparent
    transparent_count = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If pixel is very dark (near black), make transparent
            if r < threshold and g < threshold and b < threshold:
                pixels[x, y] = (0, 0, 0, 0)
                transparent_count += 1
            else:
                pixels[x, y] = (r, g, b, 255)
    
    img.save(output_path)
    print(f"  [OK] {transparent_count} pixels made transparent")
    print(f"  [OK] Saved to: {output_path}")
    return True

if __name__ == "__main__":
    import sys
    
    files = [
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/gravity_core_clean_1767841208213.png',
         'assets/sprites/collectibles/gravity_core.png'),
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/gravity_core_chamber_clean_1767841223370.png',
         'assets/sprites/collectibles/gravity_core_chamber.png'),
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/health_heart_clean_1767841245273.png',
         'assets/sprites/ui/health_heart.png'),
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/breakable_wall_clean_1767841259121.png',
         'assets/sprites/environment/breakable_wall.png'),
    ]
    
    print("="*60)
    print("Converting black backgrounds to transparency")
    print("="*60)
    print()
    
    for input_file, output_file in files:
        try:
            black_to_transparent(input_file, output_file)
            print()
        except Exception as e:
            print(f"  [ERROR] {e}")
            print()
    
    print("="*60)
    print("All assets converted!")
    print("="*60)
