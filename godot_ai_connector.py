#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Godot AI Connector - Helper script for Antigravity AI to interact with Godot projects
This script provides utilities to analyze, parse, and understand Godot project structure.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


@dataclass
class GodotScript:
    """Represents a GDScript file"""
    path: str
    name: str
    extends: Optional[str] = None
    class_name: Optional[str] = None
    functions: List[str] = None
    signals: List[str] = None
    exports: List[str] = None
    
    def __post_init__(self):
        if self.functions is None:
            self.functions = []
        if self.signals is None:
            self.signals = []
        if self.exports is None:
            self.exports = []


@dataclass
class GodotScene:
    """Represents a Godot scene file"""
    path: str
    name: str
    root_node: Optional[str] = None
    script: Optional[str] = None
    children: List[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class GodotProjectAnalyzer:
    """Analyzes Godot project structure and provides insights"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.project_file = self.project_root / "project.godot"
        self.scripts: List[GodotScript] = []
        self.scenes: List[GodotScene] = []
        self.project_config: Dict[str, Any] = {}
        
        if not self.project_file.exists():
            raise FileNotFoundError(f"No project.godot found at {self.project_root}")
    
    def analyze(self) -> Dict[str, Any]:
        """Run full project analysis"""
        print(f"[*] Analyzing Godot project at: {self.project_root}")
        
        self._parse_project_config()
        self._scan_scripts()
        self._scan_scenes()
        
        return self.get_summary()
    
    def _parse_project_config(self):
        """Parse project.godot configuration file"""
        print("[+] Parsing project configuration...")
        
        with open(self.project_file, 'r', encoding='utf-8') as f:
            current_section = None
            for line in f:
                line = line.strip()
                
                # Section header
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    self.project_config[current_section] = {}
                
                # Key-value pair
                elif '=' in line and current_section:
                    key, value = line.split('=', 1)
                    self.project_config[current_section][key.strip()] = value.strip()
        
        print(f"   ✓ Project: {self.project_config.get('application', {}).get('config/name', 'Unknown')}")
        print(f"   ✓ Godot Version: {self.project_config.get('application', {}).get('config/features', 'Unknown')}")
    
    def _scan_scripts(self):
        """Scan all GDScript files in the project"""
        print("[+] Scanning GDScript files...")
        
        script_files = list(self.project_root.rglob("*.gd"))
        
        for script_path in script_files:
            script = self._parse_script(script_path)
            if script:
                self.scripts.append(script)
        
        print(f"   ✓ Found {len(self.scripts)} scripts")
    
    def _parse_script(self, script_path: Path) -> Optional[GodotScript]:
        """Parse a single GDScript file"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            script = GodotScript(
                path=str(script_path.relative_to(self.project_root)),
                name=script_path.stem
            )
            
            # Parse extends
            extends_match = re.search(r'extends\s+(\w+)', content)
            if extends_match:
                script.extends = extends_match.group(1)
            
            # Parse class_name
            class_name_match = re.search(r'class_name\s+(\w+)', content)
            if class_name_match:
                script.class_name = class_name_match.group(1)
            
            # Parse functions
            func_pattern = r'func\s+(\w+)\s*\('
            script.functions = re.findall(func_pattern, content)
            
            # Parse signals
            signal_pattern = r'signal\s+(\w+)'
            script.signals = re.findall(signal_pattern, content)
            
            # Parse exports
            export_pattern = r'@export\s+var\s+(\w+)'
            script.exports = re.findall(export_pattern, content)
            
            return script
            
        except Exception as e:
            print(f"   ⚠ Error parsing {script_path}: {e}")
            return None
    
    def _scan_scenes(self):
        """Scan all scene files in the project"""
        print("[+] Scanning scene files...")
        
        scene_files = list(self.project_root.rglob("*.tscn"))
        
        for scene_path in scene_files:
            scene = self._parse_scene(scene_path)
            if scene:
                self.scenes.append(scene)
        
        print(f"   ✓ Found {len(self.scenes)} scenes")
    
    def _parse_scene(self, scene_path: Path) -> Optional[GodotScene]:
        """Parse a single scene file"""
        try:
            with open(scene_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            scene = GodotScene(
                path=str(scene_path.relative_to(self.project_root)),
                name=scene_path.stem
            )
            
            # Parse root node type
            root_match = re.search(r'\[node name="[^"]*" type="([^"]+)"\]', content)
            if root_match:
                scene.root_node = root_match.group(1)
            
            # Parse attached script
            script_match = re.search(r'script\s*=\s*ExtResource\([^)]+\)', content)
            if script_match:
                scene.script = script_match.group(0)
            
            # Parse child nodes
            child_pattern = r'\[node name="([^"]+)"'
            scene.children = re.findall(child_pattern, content)[1:]  # Skip root
            
            return scene
            
        except Exception as e:
            print(f"   ⚠ Error parsing {scene_path}: {e}")
            return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive project summary"""
        return {
            "project_name": self.project_config.get('application', {}).get('config/name', 'Unknown'),
            "project_root": str(self.project_root),
            "godot_version": self.project_config.get('application', {}).get('config/features', 'Unknown'),
            "total_scripts": len(self.scripts),
            "total_scenes": len(self.scenes),
            "scripts": [asdict(s) for s in self.scripts],
            "scenes": [asdict(s) for s in self.scenes],
            "script_categories": self._categorize_scripts(),
            "autoload_scripts": self._get_autoload_scripts()
        }
    
    def _categorize_scripts(self) -> Dict[str, List[str]]:
        """Categorize scripts by directory"""
        categories = defaultdict(list)
        
        for script in self.scripts:
            parts = Path(script.path).parts
            if len(parts) > 1:
                category = parts[1] if parts[0] == 'scripts' else parts[0]
            else:
                category = 'root'
            
            categories[category].append(script.name)
        
        return dict(categories)
    
    def _get_autoload_scripts(self) -> Dict[str, str]:
        """Get autoload (singleton) scripts from project config"""
        autoload_section = self.project_config.get('autoload', {})
        return {k: v for k, v in autoload_section.items()}
    
    def print_summary(self):
        """Print a human-readable summary"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print(f"PROJECT SUMMARY: {summary['project_name']}")
        print("="*60)
        
        print(f"\nStatistics:")
        print(f"   • Total Scripts: {summary['total_scripts']}")
        print(f"   • Total Scenes: {summary['total_scenes']}")
        
        print(f"\nScript Categories:")
        for category, scripts in summary['script_categories'].items():
            print(f"   • {category}: {', '.join(scripts)}")
        
        if summary['autoload_scripts']:
            print(f"\nAutoload Scripts:")
            for name, path in summary['autoload_scripts'].items():
                print(f"   • {name}: {path}")
        
        print(f"\nScripts Overview:")
        for script in self.scripts:
            print(f"\n   {script.name}.gd ({script.path})")
            if script.class_name:
                print(f"      Class: {script.class_name}")
            if script.extends:
                print(f"      Extends: {script.extends}")
            if script.signals:
                print(f"      Signals: {', '.join(script.signals)}")
            if script.exports:
                print(f"      Exports: {', '.join(script.exports)}")
            if script.functions:
                print(f"      Functions: {', '.join(script.functions[:5])}" + 
                      (f" (+{len(script.functions)-5} more)" if len(script.functions) > 5 else ""))
        
        if self.scenes:
            print(f"\nScenes Overview:")
            for scene in self.scenes:
                print(f"\n   {scene.name}.tscn ({scene.path})")
                if scene.root_node:
                    print(f"      Root: {scene.root_node}")
                if scene.children:
                    print(f"      Children: {', '.join(scene.children[:5])}" +
                          (f" (+{len(scene.children)-5} more)" if len(scene.children) > 5 else ""))
        
        print("\n" + "="*60)
    
    def export_json(self, output_path: Optional[str] = None):
        """Export analysis to JSON file"""
        if output_path is None:
            output_path = self.project_root / "project_analysis.json"
        
        summary = self.get_summary()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n[SAVED] Analysis exported to: {output_path}")


def main():
    """Main entry point"""
    import sys
    
    # Get project root from command line or use current directory
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    try:
        analyzer = GodotProjectAnalyzer(project_root)
        analyzer.analyze()
        analyzer.print_summary()
        analyzer.export_json()
        
        print("\n[SUCCESS] Analysis complete!")
        print("\n[TIP] Use this data to help Antigravity AI understand your project structure.")
        
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print(f"Usage: python godot_ai_connector.py [project_root]")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
