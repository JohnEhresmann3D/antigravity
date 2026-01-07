#!/usr/bin/env python3
"""
Fix Godot Image Imports - Validates and fixes image import issues
This script checks PNG files and regenerates proper import settings for Godot 4.x
"""

import os
import sys
from pathlib import Path
from PIL import Image
import hashlib


class GodotImageFixer:
    """Fixes Godot image import issues"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.assets_dir = self.project_root / "assets"
        self.issues_found = []
        self.fixed_count = 0
        
    def validate_and_fix(self):
        """Main validation and fix routine"""
        print("[*] Godot Image Import Fixer")
        print(f"[*] Project: {self.project_root}\n")
        
        # Find all PNG files
        png_files = list(self.assets_dir.rglob("*.png"))
        print(f"[+] Found {len(png_files)} PNG files\n")
        
        for png_file in png_files:
            self._check_image(png_file)
        
        # Summary
        print("\n" + "="*60)
        if self.issues_found:
            print(f"[!] Found {len(self.issues_found)} issues:")
            for issue in self.issues_found:
                print(f"    - {issue}")
        else:
            print("[SUCCESS] All images validated successfully!")
        
        if self.fixed_count > 0:
            print(f"\n[+] Fixed {self.fixed_count} import files")
            print("\n[ACTION REQUIRED] Please:")
            print("  1. Close Godot if it's open")
            print("  2. Delete the .godot/imported folder")
            print("  3. Reopen Godot to reimport all assets")
        
        print("="*60)
    
    def _check_image(self, png_path: Path):
        """Check and fix a single image"""
        rel_path = png_path.relative_to(self.project_root)
        import_path = Path(str(png_path) + ".import")
        
        print(f"[*] Checking: {rel_path}")
        
        # Check if file exists and is readable
        if not png_path.exists():
            self.issues_found.append(f"{rel_path} - File not found")
            print(f"    [ERROR] File not found!")
            return
        
        # Validate PNG format
        try:
            with Image.open(png_path) as img:
                width, height = img.size
                mode = img.mode
                print(f"    [OK] {width}x{height}, mode={mode}")
                
                # Check for common issues
                if mode not in ['RGB', 'RGBA', 'P', 'L']:
                    self.issues_found.append(f"{rel_path} - Unusual color mode: {mode}")
                    print(f"    [WARN] Unusual color mode: {mode}")
                    
                    # Convert to RGBA
                    print(f"    [FIX] Converting to RGBA...")
                    rgba_img = img.convert('RGBA')
                    rgba_img.save(png_path, 'PNG')
                    print(f"    [OK] Converted and saved")
                    self.fixed_count += 1
                
        except Exception as e:
            self.issues_found.append(f"{rel_path} - Invalid PNG: {e}")
            print(f"    [ERROR] Invalid PNG: {e}")
            return
        
        # Check import file
        if import_path.exists():
            with open(import_path, 'r', encoding='utf-8') as f:
                import_content = f.read()
                
            if 'valid=false' in import_content:
                print(f"    [WARN] Import marked as invalid")
                self._fix_import_file(png_path, import_path)
        else:
            print(f"    [INFO] No import file (will be created by Godot)")
    
    def _fix_import_file(self, png_path: Path, import_path: Path):
        """Fix or regenerate import file"""
        rel_path = png_path.relative_to(self.project_root)
        res_path = "res://" + str(rel_path).replace('\\', '/')
        
        # Generate UID based on file path
        uid_hash = hashlib.md5(str(rel_path).encode()).hexdigest()[:16]
        uid = f"uid://b{uid_hash}"
        
        # Determine if this is a sprite sheet or single texture
        is_spritesheet = 'spritesheet' in png_path.stem.lower() or 'sheet' in png_path.stem.lower()
        
        import_content = f"""[remap]

importer="texture"
type="CompressedTexture2D"
uid="{uid}"
path="res://.godot/imported/{png_path.name}-{uid_hash}.ctex"
metadata={{
"vram_texture": false
}}

[deps]

source_file="{res_path}"
dest_files=["res://.godot/imported/{png_path.name}-{uid_hash}.ctex"]

[params]

compress/mode=0
compress/high_quality=false
compress/lossy_quality=0.7
compress/hdr_compression=1
compress/normal_map=0
compress/channel_pack=0
mipmaps/generate=false
mipmaps/limit=-1
roughness/mode=0
roughness/src_normal=""
process/fix_alpha_border=true
process/premult_alpha=false
process/normal_map_invert_y=false
process/hdr_as_srgb=false
process/hdr_clamp_exposure=false
process/size_limit=0
process/hdr_priority=0
detect_3d/compress_to=0
"""
        
        # Write fixed import file
        with open(import_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(import_content)
        
        print(f"    [FIX] Regenerated import file")
        self.fixed_count += 1


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    try:
        fixer = GodotImageFixer(project_root)
        fixer.validate_and_fix()
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
