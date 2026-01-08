#!/usr/bin/env python3
"""
Create Antigrav Orb Sprite Sheet with Pure Transparency
Generates a properly formatted RGBA PNG with transparent background
"""

from PIL import Image, ImageDraw
import os

def create_transparent_orb_sprite():
    """Create antigrav orb sprite sheet with pure transparency"""
    
    # Frame dimensions
    frame_width = 32
    frame_height = 32
    cols = 6
    rows = 4
    
    # Total dimensions
    width = frame_width * cols  # 192
    height = frame_height * rows  # 128
    
    # Create image with RGBA mode and fully transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    purple = (200, 50, 200, 255)  # Purple/magenta
    cyan = (0, 255, 255, 255)     # Cyan outline
    pink = (255, 100, 150, 255)   # Pink face
    
    def draw_orb(x, y, size_offset=0, sparkle_offset=0):
        """Draw a single orb frame"""
        center_x = x + frame_width // 2
        center_y = y + frame_height // 2
        radius = 15 + size_offset  # Increased from 12 to 15 for larger orb
        
        # Cyan outline (2 pixels thick for better visibility)
        draw.ellipse([center_x - radius - 2, center_y - radius - 2,
                     center_x + radius + 2, center_y + radius + 2], 
                    fill=cyan)
        
        # Purple body
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius], 
                    fill=purple)
        
        # Pink face - eyes (larger)
        eye_y = center_y - 4
        draw.ellipse([center_x - 6, eye_y - 2, center_x - 3, eye_y], fill=pink)
        draw.ellipse([center_x + 3, eye_y - 2, center_x + 6, eye_y], fill=pink)
        
        # Pink face - smile (larger)
        draw.arc([center_x - 5, center_y + 1, center_x + 5, center_y + 8], 
                0, 180, fill=pink, width=2)
        
        # Small sparkles (within frame)
        if sparkle_offset > 0:
            sparkle_positions = [
                (center_x - 8, center_y - 8),
                (center_x + 8, center_y - 8),
            ]
            for sx, sy in sparkle_positions:
                draw.point((sx, sy), fill=cyan)
                draw.point((sx + 1, sy), fill=cyan)
    
    # Row 1: IDLE/FLOAT (6 frames)
    for i in range(6):
        x = i * frame_width
        y = 0
        bob = (i % 2) * 2 - 1  # Slight bobbing
        draw_orb(x, y + bob, sparkle_offset=i % 3)
    
    # Row 2: GRAVITY FLIP (6 frames)
    for i in range(6):
        x = i * frame_width
        y = frame_height
        # Energy burst effect (small, contained)
        if i in [1, 4]:
            center_x = x + frame_width // 2
            center_y = y + frame_height // 2
            # Small energy lines
            for offset in range(-6, 7, 3):
                draw.line([center_x + offset, center_y - 10, 
                          center_x + offset, center_y + 10], fill=(255, 100, 200, 200))
        draw_orb(x, y)
    
    # Row 3: PATROL (6 frames)
    for i in range(6):
        x = i * frame_width
        y = frame_height * 2
        # Small trail effect
        if i > 0:
            center_x = x + frame_width // 2
            center_y = y + frame_height // 2
            draw.point((center_x - 8, center_y), fill=(0, 255, 255, 150))
            draw.point((center_x - 9, center_y), fill=(0, 255, 255, 100))
        draw_orb(x, y)
    
    # Row 4: DAMAGED (3 frames + empty)
    for i in range(3):
        x = i * frame_width
        y = frame_height * 3
        wobble = (i % 2) * 3 - 1
        # Flash effect
        if i == 1:
            center_x = x + frame_width // 2
            center_y = y + frame_height // 2
            draw.ellipse([center_x - 14, center_y - 14,
                         center_x + 14, center_y + 14], 
                        fill=(255, 255, 0, 100))
        draw_orb(x + wobble, y)
    
    # Save as PNG with transparency
    output_path = "assets/sprites/enemies/antigrav_orb.png"
    img.save(output_path, 'PNG')
    print(f"[OK] Created transparent sprite sheet: {output_path}")
    print(f"  Dimensions: {width}x{height}")
    print(f"  Mode: {img.mode}")
    print(f"  Frames: {cols}x{rows} = {cols * rows} frames")
    
    # Verify transparency
    if img.mode == 'RGBA':
        print("  [OK] RGBA mode confirmed")
        # Check if background is transparent
        bg_pixel = img.getpixel((0, 0))
        if bg_pixel[3] == 0:
            print("  [OK] Background is fully transparent")
        else:
            print(f"  [WARN] Background alpha = {bg_pixel[3]}")
    
    return output_path

if __name__ == "__main__":
    import sys
    os.chdir(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
    create_transparent_orb_sprite()
