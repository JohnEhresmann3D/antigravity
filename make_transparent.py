#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Better transparency converter - uses edge detection for cleaner results
"""

from PIL import Image, ImageChops

def make_transparent_smart(image_path):
    """Convert image to RGBA with smart background removal"""
    print(f"Processing: {image_path}")
    
    # Open image
    img = Image.open(image_path)
    
    # Convert to RGBA
    img = img.convert('RGBA')
    
    # Get pixel data
    pixels = img.load()
    width, height = img.size
    
    # Sample multiple corner pixels to get average background color
    corners = [
        pixels[0, 0][:3],
        pixels[width-1, 0][:3],
        pixels[0, height-1][:3],
        pixels[width-1, height-1][:3]
    ]
    
    # Average the corners
    bg_r = sum(c[0] for c in corners) // 4
    bg_g = sum(c[1] for c in corners) // 4
    bg_b = sum(c[2] for c in corners) // 4
    bg_color = (bg_r, bg_g, bg_b)
    
    print(f"  Background color detected: RGB{bg_color}")
    
    # More aggressive threshold for better edge detection
    threshold = 50
    
    # Process each pixel
    transparent_count = 0
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Calculate color distance from background
            diff = ((r - bg_color[0])**2 + (g - bg_color[1])**2 + (b - bg_color[2])**2) ** 0.5
            
            # If very similar to background, make fully transparent
            if diff < threshold:
                pixels[x, y] = (r, g, b, 0)
                transparent_count += 1
            # If somewhat similar, make partially transparent
            elif diff < threshold * 2:
                alpha = int((diff / (threshold * 2)) * 255)
                pixels[x, y] = (r, g, b, alpha)
            else:
                # Keep fully opaque
                pixels[x, y] = (r, g, b, 255)
    
    # Save
    img.save(image_path)
    
    transparency_percent = (transparent_count / (width * height)) * 100
    print(f"  [OK] Converted to RGBA")
    print(f"  [OK] {transparency_percent:.1f}% transparent pixels")
    print(f"  [OK] Size: {img.size}, Mode: {img.mode}")
    
    return True

if __name__ == "__main__":
    files = [
        'assets/sprites/collectibles/gravity_core.png',
        'assets/sprites/collectibles/gravity_core_chamber.png',
        'assets/sprites/ui/health_heart.png',
        'assets/sprites/environment/breakable_wall.png'
    ]
    
    print("="*60)
    print("Smart Transparency Converter")
    print("="*60)
    print()
    
    for file in files:
        try:
            make_transparent_smart(file)
            print()
        except Exception as e:
            print(f"  [ERROR] {e}")
            print()
    
    print("="*60)
    print("Conversion complete!")
    print("="*60)
