#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find all placeholder assets in Godot project
Searches for PLACEHOLDER comments in scene files
"""

import os
import re
from pathlib import Path

def find_placeholders(project_root):
    """Find all PLACEHOLDER comments in .tscn and .gd files"""
    project_root = Path(project_root)
    
    placeholders = []
    
    # Search .tscn files
    scene_files = list(project_root.rglob("*.tscn"))
    for scene_file in scene_files:
        try:
            with open(scene_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                if 'PLACEHOLDER' in line.upper():
                    placeholders.append({
                        'file': str(scene_file.relative_to(project_root)),
                        'line': line_num,
                        'content': line.strip(),
                        'type': 'scene'
                    })
        except Exception as e:
            print(f"Error reading {scene_file}: {e}")
    
    # Search .gd files
    script_files = list(project_root.rglob("*.gd"))
    for script_file in script_files:
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                if 'PLACEHOLDER' in line.upper() or 'TODO' in line.upper():
                    placeholders.append({
                        'file': str(script_file.relative_to(project_root)),
                        'line': line_num,
                        'content': line.strip(),
                        'type': 'script'
                    })
        except Exception as e:
            print(f"Error reading {script_file}: {e}")
    
    return placeholders

def print_report(placeholders):
    """Print formatted report of placeholders"""
    print("="*70)
    print("PLACEHOLDER ASSETS REPORT")
    print("="*70)
    print()
    
    if not placeholders:
        print("No placeholders found! All assets are final.")
        print()
        return
    
    # Group by type
    scenes = [p for p in placeholders if p['type'] == 'scene']
    scripts = [p for p in placeholders if p['type'] == 'script']
    
    if scenes:
        print(f"SCENE PLACEHOLDERS ({len(scenes)} found)")
        print("-"*70)
        for p in scenes:
            print(f"\n  File: {p['file']}")
            print(f"  Line: {p['line']}")
            print(f"  Note: {p['content']}")
        print()
    
    if scripts:
        print(f"SCRIPT PLACEHOLDERS/TODOs ({len(scripts)} found)")
        print("-"*70)
        for p in scripts:
            print(f"\n  File: {p['file']}")
            print(f"  Line: {p['line']}")
            print(f"  Note: {p['content']}")
        print()
    
    print("="*70)
    print(f"TOTAL: {len(placeholders)} placeholders to address")
    print("="*70)

def main():
    import sys
    
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    print(f"Scanning project: {project_root}\n")
    
    placeholders = find_placeholders(project_root)
    print_report(placeholders)
    
    # Save to file
    output_file = Path(project_root) / "PLACEHOLDERS.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("PLACEHOLDER ASSETS REPORT\n")
        f.write("="*70 + "\n\n")
        
        for p in placeholders:
            f.write(f"File: {p['file']}\n")
            f.write(f"Line: {p['line']}\n")
            f.write(f"Note: {p['content']}\n")
            f.write("-"*70 + "\n\n")
    
    print(f"\nReport saved to: {output_file}")

if __name__ == "__main__":
    main()
