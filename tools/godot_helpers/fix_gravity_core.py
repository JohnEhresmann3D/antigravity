#!/usr/bin/env python3
"""Fix gravity core transparency - more aggressive"""

from PIL import Image

def fix_gravity_core():
    """Fix gravity core transparency"""
    print("Fixing gravity_core.png transparency...")
    
    img = Image.open('assets/sprites/collectibles/gravity_core.png').convert('RGBA')
    pixels = img.load()
    width, height = img.size
    
    # More aggressive - anything not bright purple/cyan becomes transparent
    transparent_count = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Calculate brightness and saturation
            brightness = (r + g + b) / 3
            
            # If pixel is dark OR very desaturated (grayish), make transparent
            if brightness < 80:  # Dark pixels
                pixels[x, y] = (0, 0, 0, 0)
                transparent_count += 1
            # Check if it's grayish (low color saturation)
            elif abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
                pixels[x, y] = (0, 0, 0, 0)
                transparent_count += 1
            else:
                # Keep colored pixels
                pixels[x, y] = (r, g, b, 255)
    
    img.save('assets/sprites/collectibles/gravity_core.png')
    print(f"  [OK] Made {transparent_count} pixels transparent")
    print(f"  [OK] {((width*height - transparent_count)/(width*height)*100):.1f}% visible")

if __name__ == "__main__":
    fix_gravity_core()
    print("Done!")
