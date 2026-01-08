#!/usr/bin/env python3
"""
Process antigrav orb sprite to ensure pure transparency
Removes any baked-in checkerboard pattern
"""

from PIL import Image
import sys

def ensure_pure_transparency(input_path, output_path):
    """Ensure the sprite has pure transparency with no baked patterns"""
    
    print(f"[*] Processing: {input_path}")
    
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        print(f"  [*] Converting {img.mode} to RGBA")
        img = img.convert('RGBA')
    
    # Get pixel data
    pixels = img.load()
    width, height = img.size
    
    print(f"  [*] Dimensions: {width}x{height}")
    print(f"  [*] Cleaning transparency...")
    
    # Process each pixel
    cleaned_count = 0
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If pixel is mostly transparent or is a gray checkerboard color
            if a < 128 or (abs(r - g) < 10 and abs(g - b) < 10 and abs(b - r) < 10 and r > 100):
                # Make it fully transparent
                pixels[x, y] = (0, 0, 0, 0)
                cleaned_count += 1
    
    print(f"  [*] Cleaned {cleaned_count} pixels")
    
    # Save
    img.save(output_path, 'PNG')
    print(f"  [OK] Saved to: {output_path}")
    
    # Verify
    test_img = Image.open(output_path)
    if test_img.mode == 'RGBA':
        bg_pixel = test_img.getpixel((0, 0))
        if bg_pixel[3] == 0:
            print(f"  [OK] Background is fully transparent")
        else:
            print(f"  [WARN] Background alpha = {bg_pixel[3]}")
    
    return output_path

if __name__ == "__main__":
    input_file = r"C:\Users\ehres\.gemini\antigravity\brain\92c7aa9b-3fce-425c-aa92-f081977915f9\antigrav_orb_proper_1767847517083.png"
    output_file = "assets/sprites/enemies/antigrav_orb.png"
    
    ensure_pure_transparency(input_file, output_file)
    print("\n[SUCCESS] Antigrav orb sprite processed!")
