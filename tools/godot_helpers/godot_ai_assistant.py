#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Godot AI Assistant - Advanced automation for Godot projects
Allows AI to create scenes, run Godot commands, and more
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class GodotAIAssistant:
    """Advanced Godot automation assistant"""
    
    def __init__(self, project_root: str, godot_executable: Optional[str] = None):
        self.project_root = Path(project_root)
        self.project_file = self.project_root / "project.godot"
        
        # Try to find Godot executable
        if godot_executable:
            self.godot_exe = Path(godot_executable)
        else:
            self.godot_exe = self._find_godot_executable()
        
        if not self.project_file.exists():
            raise FileNotFoundError(f"No project.godot found at {self.project_root}")
    
    def _find_godot_executable(self) -> Optional[Path]:
        """Try to find Godot executable on system"""
        # Common locations
        common_paths = [
            Path("C:/Program Files/Godot/Godot_v4.5-stable_win64.exe"),
            Path("C:/Program Files/Godot/Godot.exe"),
            Path("C:/Godot/Godot.exe"),
            Path.home() / "Godot" / "Godot.exe",
        ]
        
        for path in common_paths:
            if path.exists():
                return path
        
        # Try PATH
        try:
            result = subprocess.run(["where", "godot"], capture_output=True, text=True)
            if result.returncode == 0:
                return Path(result.stdout.strip().split('\n')[0])
        except:
            pass
        
        return None
    
    def run_godot_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run a Godot command-line operation"""
        if not self.godot_exe:
            raise RuntimeError("Godot executable not found. Please specify path.")
        
        cmd = [str(self.godot_exe), "--path", str(self.project_root)] + args
        print(f"[CMD] {' '.join(cmd)}")
        
        return subprocess.run(cmd, capture_output=True, text=True)
    
    def reimport_resources(self):
        """Force Godot to reimport all resources"""
        print("[*] Reimporting resources...")
        result = self.run_godot_command(["--headless", "--quit"])
        
        if result.returncode == 0:
            print("   ✓ Resources reimported successfully")
        else:
            print(f"   ✗ Error: {result.stderr}")
        
        return result.returncode == 0
    
    def export_project(self, preset: str, output_path: str):
        """Export the project using a preset"""
        print(f"[*] Exporting project with preset: {preset}")
        result = self.run_godot_command(["--headless", "--export-release", preset, output_path])
        
        if result.returncode == 0:
            print(f"   ✓ Exported to: {output_path}")
        else:
            print(f"   ✗ Error: {result.stderr}")
        
        return result.returncode == 0
    
    def run_scene(self, scene_path: str):
        """Run a specific scene"""
        print(f"[*] Running scene: {scene_path}")
        result = self.run_godot_command([scene_path])
        return result.returncode == 0
    
    def run_tests(self, test_path: Optional[str] = None):
        """Run GUT tests"""
        print("[*] Running tests...")
        
        args = ["--headless", "-s", "res://addons/gut/gut_cmdln.gd"]
        if test_path:
            args.extend(["-gtest", test_path])
        
        result = self.run_godot_command(args)
        
        if result.returncode == 0:
            print("   ✓ Tests completed")
            print(result.stdout)
        else:
            print(f"   ✗ Test errors: {result.stderr}")
        
        return result.returncode == 0
    
    def create_script_template(self, script_path: str, extends: str = "Node", class_name: Optional[str] = None):
        """Create a GDScript template"""
        full_path = self.project_root / script_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        template = f"extends {extends}\n"
        if class_name:
            template += f"class_name {class_name}\n"
        template += f"## {class_name or 'Script'} description\n\n"
        template += "func _ready() -> void:\n\tpass\n"
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"   ✓ Created script: {script_path}")
        return True
    
    def get_project_info(self) -> Dict:
        """Get project information"""
        info = {
            "root": str(self.project_root),
            "godot_exe": str(self.godot_exe) if self.godot_exe else "Not found",
            "has_git": (self.project_root / ".git").exists(),
            "has_tests": (self.project_root / "tests").exists(),
        }
        
        # Count files
        info["script_count"] = len(list(self.project_root.rglob("*.gd")))
        info["scene_count"] = len(list(self.project_root.rglob("*.tscn")))
        info["asset_count"] = len(list(self.project_root.rglob("*.png"))) + \
                             len(list(self.project_root.rglob("*.jpg")))
        
        return info


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Godot AI Assistant")
    parser.add_argument("project_root", nargs="?", default=os.getcwd(), help="Project root directory")
    parser.add_argument("--godot", help="Path to Godot executable")
    parser.add_argument("--reimport", action="store_true", help="Reimport all resources")
    parser.add_argument("--run", help="Run a specific scene")
    parser.add_argument("--test", nargs="?", const=True, help="Run tests")
    parser.add_argument("--info", action="store_true", help="Show project info")
    
    args = parser.parse_args()
    
    try:
        assistant = GodotAIAssistant(args.project_root, args.godot)
        
        if args.info:
            info = assistant.get_project_info()
            print("\n" + "="*60)
            print("PROJECT INFORMATION")
            print("="*60)
            for key, value in info.items():
                print(f"   {key}: {value}")
            print("="*60)
        
        elif args.reimport:
            assistant.reimport_resources()
        
        elif args.run:
            assistant.run_scene(args.run)
        
        elif args.test:
            test_path = args.test if isinstance(args.test, str) else None
            assistant.run_tests(test_path)
        
        else:
            print("Godot AI Assistant - No action specified")
            print("Use --help for available commands")
            print(f"\nGodot executable: {assistant.godot_exe or 'Not found'}")
            print(f"Project: {assistant.project_root}")
    
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
