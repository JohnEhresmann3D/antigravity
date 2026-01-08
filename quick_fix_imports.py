#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Fix Script - Fixes common Godot import issues
Run this whenever you see "Not a PNG file" or import errors
"""

import os
import sys
import shutil
from pathlib import Path

def fix_godot_imports(project_root):
    """Fix Godot import issues"""
    project_root = Path(project_root)
    
    print("="*60)
    print("Godot Import Quick Fix")
    print("="*60)
    print(f"\nProject: {project_root}\n")
    
    # Step 1: Delete .godot/imported folder
    imported_folder = project_root / ".godot" / "imported"
    if imported_folder.exists():
        print("[*] Deleting .godot/imported folder...")
        try:
            shutil.rmtree(imported_folder)
            print("   ✓ Deleted successfully")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return False
    else:
        print("[*] .godot/imported folder doesn't exist (already clean)")
    
    # Step 2: Run the image fixer
    print("\n[*] Running image fixer...")
    fix_script = project_root / "fix_godot_images.py"
    if fix_script.exists():
        os.system(f'python "{fix_script}"')
    else:
        print("   ⚠ fix_godot_images.py not found, skipping")
    
    print("\n" + "="*60)
    print("[SUCCESS] Import cache cleared!")
    print("\n[NEXT STEPS]")
    print("1. Open Godot")
    print("2. Let it reimport all assets (may take a moment)")
    print("3. Check for any remaining errors")
    print("="*60)
    
    return True

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    fix_godot_imports(project_root)
