#!/usr/bin/env python3
"""Convert new simple assets"""

from PIL import Image

def black_to_transparent(input_path, output_path):
    """Convert black pixels to transparent"""
    print(f"Converting: {input_path}")
    
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    width, height = img.size
    
    threshold = 30
    transparent_count = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            if r < threshold and g < threshold and b < threshold:
                pixels[x, y] = (0, 0, 0, 0)
                transparent_count += 1
            else:
                pixels[x, y] = (r, g, b, 255)
    
    img.save(output_path)
    print(f"  [OK] Saved to: {output_path}")
    return True

if __name__ == "__main__":
    files = [
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/gravity_core_simple_1767844304890.png',
         'assets/sprites/collectibles/gravity_core.png'),
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/breakable_wall_simple_1767844317510.png',
         'assets/sprites/environment/breakable_wall.png'),
        ('C:/Users/ehres/.gemini/antigravity/brain/bd8200f5-93de-4f84-9647-45c1e592f1a4/gravity_core_chamber_clean_1767841223370.png',
         'assets/sprites/collectibles/gravity_core_chamber.png'),
    ]
    
    print("Converting simple assets...")
    for input_file, output_file in files:
        try:
            black_to_transparent(input_file, output_file)
        except Exception as e:
            print(f"  [ERROR] {e}")
    
    print("\nDone!")
