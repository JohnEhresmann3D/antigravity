# 🤖 Godot AI Connector

A Python utility script that helps **Antigravity AI** understand and interact with your Godot project structure.

## 🎯 Purpose

This script analyzes your Godot project and generates a comprehensive summary that helps me (Antigravity AI) to:
- Understand your project structure
- Identify all scripts and their relationships
- Parse scene hierarchies
- Recognize autoload singletons
- Provide better, context-aware assistance

## 🚀 Quick Start

### Basic Usage

Run from your project root:

```bash
python godot_ai_connector.py
```

Or specify a project path:

```bash
python godot_ai_connector.py "D:\GameDevelopment\Godot\Games\antigravity"
```

### What It Does

1. **Parses `project.godot`** - Extracts project configuration
2. **Scans all `.gd` files** - Analyzes GDScript structure
3. **Scans all `.tscn` files** - Parses scene hierarchies
4. **Generates summary** - Creates both console output and JSON export

## 📊 Output

### Console Output
The script prints a detailed summary including:
- Project statistics
- Script categories
- Autoload scripts
- Function and signal listings
- Scene hierarchies

### JSON Export
Creates `project_analysis.json` with complete project data that I can reference.

## 🔍 What Gets Analyzed

### For GDScript Files (`.gd`)
- `extends` declarations
- `class_name` definitions
- Function definitions
- Signal declarations
- `@export` variables

### For Scene Files (`.tscn`)
- Root node type
- Attached scripts
- Child node hierarchy

### For Project Config
- Project name
- Godot version
- Autoload scripts
- Application settings

## 💡 Use Cases

### 1. Project Overview
When you ask me "What's in my project?", I can run this script to get a complete picture.

### 2. Code Generation
Before creating new scripts, I can check existing patterns and naming conventions.

### 3. Refactoring Help
I can identify all scripts that extend a certain class or use specific signals.

### 4. Documentation
The JSON output serves as living documentation of your project structure.

## 📁 Example Output Structure

```json
{
  "project_name": "Antigravity",
  "godot_version": "4.5",
  "total_scripts": 3,
  "total_scenes": 0,
  "scripts": [
    {
      "name": "player",
      "path": "scripts/player/player.gd",
      "extends": "CharacterBody2D",
      "functions": ["_ready", "_physics_process", "jump"],
      "signals": ["player_died"],
      "exports": ["speed", "jump_force"]
    }
  ],
  "script_categories": {
    "player": ["player"],
    "gravity": ["gravity_zone"],
    "autoload": ["gravity_manager"]
  }
}
```

## 🛠️ Advanced Usage

### Import as Module

You can also import and use the analyzer programmatically:

```python
from godot_ai_connector import GodotProjectAnalyzer

analyzer = GodotProjectAnalyzer("path/to/project")
summary = analyzer.analyze()

# Access specific data
print(f"Found {summary['total_scripts']} scripts")

# Export to custom location
analyzer.export_json("custom_output.json")
```

### Extend Functionality

The script is designed to be extensible. You can add new analysis methods:

```python
class CustomAnalyzer(GodotProjectAnalyzer):
    def analyze_resources(self):
        # Add custom resource analysis
        pass
```

## 🔄 Integration Workflow

1. **You make changes** to your Godot project
2. **Run the connector** to update the analysis
3. **Share the output** with me (or I run it automatically)
4. **I provide better assistance** based on current project state

## 📝 Notes

- The script is read-only and won't modify your project
- It skips `.godot` directory and other build artifacts
- Works with Godot 4.x projects (tested with 4.5)
- Requires Python 3.7+

## 🐛 Troubleshooting

### "No project.godot found"
Make sure you're running the script from your project root or providing the correct path.

### Encoding errors
The script uses UTF-8 encoding. If you have special characters, ensure your files are UTF-8 encoded.

### Missing scripts/scenes
Check that your files have the correct extensions (`.gd`, `.tscn`) and aren't in ignored directories.

## 🎮 Next Steps

After running this script, you can ask me things like:
- "What functions does my player script have?"
- "Show me all scripts that extend CharacterBody2D"
- "What autoload scripts do I have?"
- "Create a new enemy script following my existing patterns"

---

**Made for Antigravity Game Development** 🚀
