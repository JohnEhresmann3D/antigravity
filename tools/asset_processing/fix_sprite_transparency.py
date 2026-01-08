#!/usr/bin/env python3
"""
Fix Sprite Transparency - Converts RGB sprites to RGBA with transparency
"""

import os
import sys
from pathlib import Path
from PIL import Image


def fix_sprite_transparency(project_root: str):
    """Convert all sprite sheets to RGBA with proper transparency"""
    project_root = Path(project_root)
    sprites_dir = project_root / "assets" / "sprites"
    
    print("[*] Fixing sprite transparency...")
    
    # Find all PNG files
    png_files = list(sprites_dir.rglob("*.png"))
    fixed_count = 0
    
    for png_path in png_files:
        try:
            with Image.open(png_path) as img:
                # Check if already RGBA
                if img.mode == 'RGBA':
                    print(f"   [OK] {png_path.name} - Already RGBA")
                    continue
                
                print(f"   [FIX] {png_path.name} - Converting {img.mode} to RGBA")
                
                # Convert to RGBA
                rgba_img = img.convert('RGBA')
                
                # For sprites, we want to make the background transparent
                # Assuming white or a specific color is the background
                # Let's make pure white transparent
                datas = rgba_img.getdata()
                new_data = []
                
                for item in datas:
                    # Change all white (also shades of white) to transparent
                    # Adjust threshold as needed
                    if item[0] > 250 and item[1] > 250 and item[2] > 250:
                        new_data.append((255, 255, 255, 0))  # Transparent
                    else:
                        new_data.append(item)
                
                rgba_img.putdata(new_data)
                
                # Save back
                rgba_img.save(png_path, 'PNG')
                print(f"   [SUCCESS] Converted and saved with transparency")
                fixed_count += 1
                
        except Exception as e:
            print(f"   [ERROR] Failed to process {png_path.name}: {e}")
    
    print(f"\n[COMPLETE] Fixed {fixed_count} sprites")
    print("\n[NEXT STEPS]")
    print("  1. Close Godot if open")
    print("  2. Delete .godot/imported folder")
    print("  3. Reopen Godot to reimport")


def main():
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    try:
        fix_sprite_transparency(project_root)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
