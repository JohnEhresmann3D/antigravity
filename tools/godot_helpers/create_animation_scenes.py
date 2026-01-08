#!/usr/bin/env python3
"""
Godot Scene Generator - Creates .tscn files for player, enemies, and projectiles
This automates the tedious process of creating scene files with proper node hierarchies
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class GodotSceneGenerator:
    """Generates Godot 4.x scene files"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.scenes_dir = self.project_root / "scenes"
        self.animation_data_dir = self.project_root / "resources" / "animation_data"
        
    def generate_all_scenes(self):
        """Generate all game scenes"""
        print("[*] Godot Scene Generator")
        print(f"[*] Project: {self.project_root}\n")
        
        # Create directories
        (self.scenes_dir / "player").mkdir(parents=True, exist_ok=True)
        (self.scenes_dir / "enemies").mkdir(parents=True, exist_ok=True)
        (self.scenes_dir / "projectiles").mkdir(parents=True, exist_ok=True)
        
        # Generate scenes
        self.generate_player_scene()
        self.generate_flyer_drone_scene()
        self.generate_turret_scene()
        self.generate_antigrav_orb_scene()
        self.generate_projectile_scenes()
        
        print("\n[SUCCESS] All scenes generated!")
        print("\n[NEXT STEPS]")
        print("  1. Open Godot and let it import the new scenes")
        print("  2. Follow the manual setup guide for SpriteFrames configuration")
        print("  3. Test each scene individually")
    
    def generate_player_scene(self):
        """Generate player scene"""
        print("[+] Generating player scene...")
        
        scene_content = '''[gd_scene load_steps=3 format=3 uid="uid://player_scene_001"]

[ext_resource type="Script" path="res://scripts/player/player.gd" id="1_player"]
[ext_resource type="Texture2D" uid="uid://b849931abd9721ce6" path="res://assets/sprites/characters/cosmo_spritesheet.png" id="2_sprite"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_player"]
size = Vector2(40, 56)

[node name="Player" type="CharacterBody2D"]
script = ExtResource("1_player")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1
position = Vector2(0, -28)

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2(0, -28)
shape = SubResource("RectangleShape2D_player")

[node name="Camera2D" type="Camera2D" parent="."]
enabled = false
zoom = Vector2(2, 2)
'''
        
        scene_path = self.scenes_dir / "player" / "player.tscn"
        with open(scene_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(scene_content)
        
        print(f"   Created: {scene_path}")
    
    def generate_flyer_drone_scene(self):
        """Generate flyer drone enemy scene"""
        print("[+] Generating flyer drone scene...")
        
        scene_content = '''[gd_scene load_steps=3 format=3 uid="uid://flyer_drone_001"]

[ext_resource type="Script" path="res://scripts/enemies/flyer_drone.gd" id="1_script"]
[ext_resource type="Texture2D" uid="uid://ddm76exgci13b" path="res://assets/sprites/enemies/flyer_drone.png" id="2_sprite"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_body"]
size = Vector2(28, 28)

[sub_resource type="CircleShape2D" id="CircleShape2D_detection"]
radius = 200.0

[node name="FlyerDrone" type="CharacterBody2D" groups=["enemies"]]
collision_layer = 2
collision_mask = 1
script = ExtResource("1_script")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_body")

[node name="DetectionArea" type="Area2D" parent="."]
collision_layer = 0
collision_mask = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="DetectionArea"]
shape = SubResource("CircleShape2D_detection")

[node name="HurtBox" type="Area2D" parent="." groups=["hurtbox"]]
collision_layer = 2
collision_mask = 0

[node name="CollisionShape2D" type="CollisionShape2D" parent="HurtBox"]
shape = SubResource("RectangleShape2D_body")

[connection signal="body_entered" from="DetectionArea" to="." method="_on_detection_area_body_entered"]
[connection signal="body_exited" from="DetectionArea" to="." method="_on_detection_area_body_exited"]
'''
        
        scene_path = self.scenes_dir / "enemies" / "flyer_drone.tscn"
        with open(scene_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(scene_content)
        
        print(f"   Created: {scene_path}")
    
    def generate_turret_scene(self):
        """Generate turret enemy scene"""
        print("[+] Generating turret scene...")
        
        scene_content = '''[gd_scene load_steps=3 format=3 uid="uid://turret_001"]

[ext_resource type="Script" path="res://scripts/enemies/turret.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/enemies/turret.png" id="2_sprite"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_body"]
size = Vector2(30, 30)

[sub_resource type="CircleShape2D" id="CircleShape2D_detection"]
radius = 300.0

[node name="Turret" type="StaticBody2D" groups=["enemies"]]
collision_layer = 2
collision_mask = 1
script = ExtResource("1_script")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_body")

[node name="DetectionArea" type="Area2D" parent="."]
collision_layer = 0
collision_mask = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="DetectionArea"]
shape = SubResource("CircleShape2D_detection")

[node name="BarrelMarker" type="Marker2D" parent="."]
position = Vector2(16, 0)

[node name="FireTimer" type="Timer" parent="."]
wait_time = 2.0
autostart = true

[node name="HurtBox" type="Area2D" parent="." groups=["hurtbox"]]
collision_layer = 2
collision_mask = 0

[node name="CollisionShape2D" type="CollisionShape2D" parent="HurtBox"]
shape = SubResource("RectangleShape2D_body")

[connection signal="body_entered" from="DetectionArea" to="." method="_on_detection_area_body_entered"]
[connection signal="body_exited" from="DetectionArea" to="." method="_on_detection_area_body_exited"]
[connection signal="timeout" from="FireTimer" to="." method="_on_fire_timer_timeout"]
'''
        
        scene_path = self.scenes_dir / "enemies" / "turret.tscn"
        with open(scene_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(scene_content)
        
        print(f"   Created: {scene_path}")
    
    def generate_antigrav_orb_scene(self):
        """Generate antigrav orb enemy scene"""
        print("[+] Generating antigrav orb scene...")
        
        scene_content = '''[gd_scene load_steps=3 format=3 uid="uid://antigrav_orb_001"]

[ext_resource type="Script" path="res://scripts/enemies/antigrav_orb.gd" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/sprites/enemies/antigrav_orb.png" id="2_sprite"]

[sub_resource type="CircleShape2D" id="CircleShape2D_body"]
radius = 14.0

[sub_resource type="CircleShape2D" id="CircleShape2D_detection"]
radius = 150.0

[node name="AntigravOrb" type="CharacterBody2D" groups=["enemies"]]
collision_layer = 2
collision_mask = 1
script = ExtResource("1_script")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_body")

[node name="DetectionArea" type="Area2D" parent="."]
collision_layer = 0
collision_mask = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="DetectionArea"]
shape = SubResource("CircleShape2D_detection")

[node name="HurtBox" type="Area2D" parent="." groups=["hurtbox"]]
collision_layer = 2
collision_mask = 0

[node name="CollisionShape2D" type="CollisionShape2D" parent="HurtBox"]
shape = SubResource("CircleShape2D_body")

[connection signal="body_entered" from="DetectionArea" to="." method="_on_detection_area_body_entered"]
[connection signal="body_exited" from="DetectionArea" to="." method="_on_detection_area_body_exited"]
'''
        
        scene_path = self.scenes_dir / "enemies" / "antigrav_orb.tscn"
        with open(scene_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(scene_content)
        
        print(f"   Created: {scene_path}")
    
    def generate_projectile_scenes(self):
        """Generate projectile scenes"""
        print("[+] Generating projectile scenes...")
        
        # Energy Ball
        energy_ball_content = '''[gd_scene load_steps=2 format=3 uid="uid://energy_ball_001"]

[ext_resource type="Script" path="res://scripts/projectiles/projectile.gd" id="1_script"]

[sub_resource type="CircleShape2D" id="CircleShape2D_projectile"]
radius = 8.0

[node name="EnergyBall" type="Area2D" groups=["projectiles"]]
collision_layer = 4
collision_mask = 1
script = ExtResource("1_script")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="."]
texture_filter = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("CircleShape2D_projectile")

[node name="VisibleOnScreenNotifier2D" type="VisibleOnScreenNotifier2D" parent="."]

[connection signal="body_entered" from="." to="." method="_on_body_entered"]
[connection signal="screen_exited" from="VisibleOnScreenNotifier2D" to="." method="_on_screen_exited"]
'''
        
        scene_path = self.scenes_dir / "projectiles" / "energy_ball.tscn"
        with open(scene_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(energy_ball_content)
        
        print(f"   Created: {scene_path}")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    try:
        generator = GodotSceneGenerator(project_root)
        generator.generate_all_scenes()
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
