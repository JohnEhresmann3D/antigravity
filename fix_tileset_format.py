"""
Fix JPEG header issue in AI-generated tilesets
Automatically detects and converts images to proper PNG format for Godot
"""
from PIL import Image
import os

def check_file_format(file_path):
    """
    Check if a PNG file actually has JPEG data
    Returns: ('PNG', True) if proper PNG, ('JPEG', False) if JPEG data in PNG file
    """
    with open(file_path, 'rb') as f:
        header = f.read(16)
    
    # PNG signature: 89 50 4E 47 0D 0A 1A 0A
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # JPEG signature: FF D8 FF
    jpeg_signature = b'\xff\xd8\xff'
    
    if header.startswith(png_signature):
        return ('PNG', True)
    elif header.startswith(jpeg_signature):
        return ('JPEG', False)
    else:
        return ('UNKNOWN', False)

def fix_tileset_format(input_path, output_path):
    """Convert image to proper PNG format"""
    # Check file format first
    format_type, is_valid = check_file_format(input_path)
    
    if is_valid:
        print(f"[OK] {os.path.basename(input_path)} - Already proper PNG format")
        return False
    
    print(f"[WARN] {os.path.basename(input_path)} - Detected {format_type} data in PNG file")
    print(f"  Converting to proper PNG...")
    
    # Open image (PIL will handle JPEG data)
    img = Image.open(input_path)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        print(f"  Converting from {img.mode} to RGBA")
        img = img.convert('RGBA')
    
    # Save as proper PNG
    img.save(output_path, 'PNG', optimize=False)
    
    # Verify the fix
    format_type_after, is_valid_after = check_file_format(output_path)
    if is_valid_after:
        print(f"[OK] Successfully converted to proper PNG format")
        return True
    else:
        print(f"[ERROR] Conversion failed - still {format_type_after}")
        return False

if __name__ == "__main__":
    assets_dir = "assets/sprites/tilesets"
    
    tilesets = [
        "tileset_level1_structure_ai.png",
        "tileset_level1_props_ai.png",
        "tileset_level1_items_ai.png"
    ]
    
    print("Checking tileset formats...\n")
    
    fixed_count = 0
    for tileset in tilesets:
        input_path = os.path.join(assets_dir, tileset)
        if os.path.exists(input_path):
            # Check format first
            format_type, is_valid = check_file_format(input_path)
            
            if not is_valid:
                # Create backup before fixing
                backup_path = input_path + ".backup"
                if not os.path.exists(backup_path):
                    import shutil
                    shutil.copy2(input_path, backup_path)
                    print(f"  Created backup: {os.path.basename(backup_path)}")
                
                # Convert to proper PNG
                if fix_tileset_format(input_path, input_path):
                    fixed_count += 1
            else:
                print(f"[OK] {tileset} - Already proper PNG format")
        else:
            print(f"[ERROR] File not found: {tileset}")
        print()
    
    print("=" * 60)
    if fixed_count > 0:
        print(f"Fixed {fixed_count} tileset(s) with format issues.")
        print("Restart Godot to see the changes.")
    else:
        print("All tilesets are already in proper PNG format!")
    print("=" * 60)
