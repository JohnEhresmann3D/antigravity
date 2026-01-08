#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Godot Scene Builder - Automate Level 1 scene creation
Creates .tscn files programmatically for Antigravity Level 1
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class GodotSceneBuilder:
    """Builds Godot .tscn scene files programmatically"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.ext_resource_counter = 1
        self.sub_resource_counter = 1
        self.node_counter = 1
        
    def create_gravity_core_scene(self) -> str:
        """Create gravity_core.tscn scene file"""
        scene_content = f"""[gd_scene load_steps=4 format=3 uid="uid://gravity_core_001"]

[ext_resource type="Script" path="res://scripts/collectibles/gravity_core.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/collectibles/gravity_core.png" id="2_texture"]

[sub_resource type="CircleShape2D" id="CircleShape2D_1"]
radius = 16.0

[node name="GravityCore" type="Area2D"]
collision_layer = 8
collision_mask = 1
script = ExtResource("1_script")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture = ExtResource("2_texture")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_1")
"""
        return scene_content
    
    def create_tutorial_prompt_scene(self) -> str:
        """Create tutorial_prompt.tscn scene file"""
        scene_content = f"""[gd_scene load_steps=2 format=3 uid="uid://tutorial_prompt_001"]

[ext_resource type="Script" path="res://scripts/ui/tutorial_prompt.gd" id="1_script"]

[node name="TutorialPrompt" type="CanvasLayer"]
layer = 10
script = ExtResource("1_script")

[node name="Panel" type="Panel" parent="."]
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -200.0
offset_top = 150.0
offset_right = 200.0
offset_bottom = 250.0
grow_horizontal = 2
grow_vertical = 2

[node name="MarginContainer" type="MarginContainer" parent="Panel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
theme_override_constants/margin_left = 10
theme_override_constants/margin_top = 10
theme_override_constants/margin_right = 10
theme_override_constants/margin_bottom = 10

[node name="Label" type="Label" parent="Panel/MarginContainer"]
layout_mode = 2
text = "Tutorial Prompt"
horizontal_alignment = 1
vertical_alignment = 1
autowrap_mode = 2
"""
        return scene_content
    
    def create_game_hud_scene(self) -> str:
        """Create game_hud.tscn scene file"""
        scene_content = f"""[gd_scene load_steps=2 format=3 uid="uid://game_hud_001"]

[ext_resource type="Script" path="res://scripts/ui/game_hud.gd" id="1_script"]

[node name="GameHUD" type="CanvasLayer"]
layer = 5
script = ExtResource("1_script")

[node name="MarginContainer" type="MarginContainer" parent="."]
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
theme_override_constants/margin_left = 10
theme_override_constants/margin_top = 10
theme_override_constants/margin_right = 10
theme_override_constants/margin_bottom = 10

[node name="VBoxContainer" type="VBoxContainer" parent="MarginContainer"]
layout_mode = 2
size_flags_horizontal = 0
size_flags_vertical = 0

[node name="HealthContainer" type="HBoxContainer" parent="MarginContainer/VBoxContainer"]
layout_mode = 2
theme_override_constants/separation = 5

[node name="CoresContainer" type="HBoxContainer" parent="MarginContainer/VBoxContainer"]
layout_mode = 2

[node name="CoresLabel" type="Label" parent="MarginContainer/VBoxContainer/CoresContainer"]
layout_mode = 2
text = "Cores: 0"
"""
        return scene_content
    
    def create_checkpoint_scene(self) -> str:
        """Create checkpoint.tscn scene file"""
        scene_content = f"""[gd_scene load_steps=3 format=3 uid="uid://checkpoint_001"]

[ext_resource type="Script" path="res://scripts/level/checkpoint.gd" id="1_script"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_1"]
size = Vector2(32, 64)

[node name="Checkpoint" type="Area2D"]
collision_layer = 16
collision_mask = 1
script = ExtResource("1_script")

[node name="ColorRect" type="ColorRect" parent="."]
offset_left = -16.0
offset_top = -32.0
offset_right = 16.0
offset_bottom = 32.0
color = Color(0, 1, 0, 0.3)

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_1")
"""
        return scene_content
    
    def create_moving_platform_scene(self) -> str:
        """Create moving_platform.tscn scene file"""
        scene_content = f"""[gd_scene load_steps=3 format=3 uid="uid://moving_platform_001"]

[ext_resource type="Script" path="res://scripts/level/moving_platform.gd" id="1_script"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_1"]
size = Vector2(96, 16)

[node name="MovingPlatform" type="AnimatableBody2D"]
sync_to_physics = true
script = ExtResource("1_script")

[node name="ColorRect" type="ColorRect" parent="."]
offset_left = -48.0
offset_top = -8.0
offset_right = 48.0
offset_bottom = 8.0
color = Color(0.5, 0.7, 0.9, 1)

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_1")
"""
        return scene_content
    
    def create_level_end_trigger_scene(self) -> str:
        """Create level_end_trigger.tscn scene file"""
        scene_content = f"""[gd_scene load_steps=4 format=3 uid="uid://level_end_trigger_001"]

[ext_resource type="Script" path="res://scripts/level/level_end_trigger.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/collectibles/gravity_core_chamber.png" id="2_texture"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_1"]
size = Vector2(128, 128)

[node name="LevelEndTrigger" type="Area2D"]
collision_layer = 16
collision_mask = 1
script = ExtResource("1_script")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture = ExtResource("2_texture")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_1")
"""
        return scene_content
    
    def save_scene(self, content: str, scene_path: Path) -> bool:
        """Save scene content to file"""
        try:
            # Create directory if it doesn't exist
            scene_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write scene file
            with open(scene_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✓ Created: {scene_path.relative_to(self.project_root)}")
            return True
            
        except Exception as e:
            print(f"   ✗ Error creating {scene_path}: {e}")
            return False


def main():
    """Main entry point"""
    
    # Get project root
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    print("="*60)
    print("Godot Scene Builder - Level 1 Automation")
    print("="*60)
    print(f"\nProject Root: {project_root}\n")
    
    builder = GodotSceneBuilder(project_root)
    
    # Define scenes to create
    scenes = [
        ("scenes/collectibles/gravity_core.tscn", builder.create_gravity_core_scene),
        ("scenes/ui/tutorial_prompt.tscn", builder.create_tutorial_prompt_scene),
        ("scenes/ui/game_hud.tscn", builder.create_game_hud_scene),
        ("scenes/level/checkpoint.tscn", builder.create_checkpoint_scene),
        ("scenes/level/moving_platform.tscn", builder.create_moving_platform_scene),
        ("scenes/level/level_end_trigger.tscn", builder.create_level_end_trigger_scene),
    ]
    
    print("[*] Creating scene files...\n")
    
    created_count = 0
    for scene_path, scene_generator in scenes:
        full_path = Path(project_root) / scene_path
        content = scene_generator()
        if builder.save_scene(content, full_path):
            created_count += 1
    
    print(f"\n[SUCCESS] Created {created_count}/{len(scenes)} scene files!")
    print("\n[NEXT STEPS]")
    print("1. Open Godot and let it import the new scenes")
    print("2. Open each scene to verify it looks correct")
    print("3. Create Level 1 main scene manually (too complex to automate)")
    print("4. Instance these scenes in your Level 1 layout")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
