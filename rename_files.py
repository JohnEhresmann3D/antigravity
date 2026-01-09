"""
Rename files to match the new naming convention with asset type prefixes
Run with --dry-run to preview changes without applying them
"""
import os
import shutil
from pathlib import Path

# Define renaming rules with asset type prefixes
RENAME_MAP = {
    # Tilesets - add ts_ prefix, remove _ai suffix
    "assets/sprites/tilesets/tileset_level1_structure_ai.png": "assets/sprites/tilesets/ts_level1_structure.png",
    "assets/sprites/tilesets/tileset_level1_props_ai.png": "assets/sprites/tilesets/ts_level1_props.png",
    "assets/sprites/tilesets/tileset_level1_items_ai.png": "assets/sprites/tilesets/ts_level1_items.png",
    
    # Characters - add spr_char_ prefix
    "assets/sprites/characters/cosmo_spritesheet.png": "assets/sprites/characters/spr_char_cosmo.png",
    
    # Enemies - add spr_enemy_ prefix
    "assets/sprites/enemies/flyer_drone.png": "assets/sprites/enemies/spr_enemy_flyer_drone.png",
    "assets/sprites/enemies/turret.png": "assets/sprites/enemies/spr_enemy_turret.png",
    "assets/sprites/enemies/antigrav_orb.png": "assets/sprites/enemies/spr_enemy_antigrav_orb.png",
    "assets/sprites/enemies/antigrav_orb_glow_r0g255b255.png": "assets/sprites/enemies/spr_enemy_antigrav_orb_glow_cyan.png",
    "assets/sprites/enemies/antigrav_orb_glow_r255g100b150.png": "assets/sprites/enemies/spr_enemy_antigrav_orb_glow_pink.png",
    "assets/sprites/enemies/antigrav_orb_edge_glow.png": "assets/sprites/enemies/spr_enemy_antigrav_orb_edge_glow.png",
    "assets/sprites/enemies/antigrav_orb_emission.png": "assets/sprites/enemies/spr_enemy_antigrav_orb_emission.png",
    "assets/sprites/enemies/antigrav_orb_hdr_emission.png": "assets/sprites/enemies/spr_enemy_antigrav_orb_hdr_emission.png",
    "assets/sprites/enemies/projectiles.png": "assets/sprites/enemies/spr_proj_spritesheet.png",
    
    # Collectibles - add spr_item_ prefix
    "assets/sprites/collectibles/gravity_core.png": "assets/sprites/collectibles/spr_item_gravity_core.png",
    "assets/sprites/collectibles/gravity_core_chamber.png": "assets/sprites/collectibles/spr_item_gravity_core_chamber.png",
    
    # Environment - add spr_env_ prefix
    "assets/sprites/environment/breakable_wall.png": "assets/sprites/environment/spr_env_breakable_wall.png",
    "assets/sprites/environment/flowers_animated.png": "assets/sprites/environment/spr_env_deco_flowers.png",
    "assets/sprites/environment/hazards_animated.png": "assets/sprites/environment/spr_env_hazards_animated.png",
    "assets/sprites/environment/objects_static.png": "assets/sprites/environment/spr_env_props_static.png",
    
    # Backgrounds - already have bg_ prefix, just clean up
    "assets/backgrounds/space_station_bg.png": "assets/backgrounds/bg_space_station_layer1.png",
    "assets/backgrounds/bg_space_station.png": "assets/backgrounds/bg_space_station_layer2.png",
    
    # UI - already have ui_ prefix
    "assets/sprites/ui/health_heart.png": "assets/sprites/ui/ui_health_heart.png",
    
    # Scenes - add scn_ prefix
    "scenes/enemies/flyer_drone.tscn": "scenes/enemies/scn_enemy_flyer_drone.tscn",
    "scenes/enemies/turret.tscn": "scenes/enemies/scn_enemy_turret.tscn",
    "scenes/enemies/antigrav_orb.tscn": "scenes/enemies/scn_enemy_antigrav_orb.tscn",
    "scenes/collectibles/gravity_core.tscn": "scenes/collectibles/scn_item_gravity_core.tscn",
    "scenes/projectiles/energy_ball.tscn": "scenes/projectiles/scn_proj_energy_ball.tscn",
    "scenes/level/checkpoint.tscn": "scenes/level/scn_env_checkpoint.tscn",
    "scenes/level/moving_platform.tscn": "scenes/level/scn_env_moving_platform.tscn",
    "scenes/level/level_end_trigger.tscn": "scenes/level/scn_level_end_trigger.tscn",
    "scenes/levels/level_1.tscn": "scenes/levels/scn_level_1.tscn",
    "scenes/player/player.tscn": "scenes/player/scn_char_cosmo.tscn",
    "scenes/ui/game_hud.tscn": "scenes/ui/scn_ui_game_hud.tscn",
    "scenes/ui/tutorial_prompt.tscn": "scenes/ui/scn_ui_tutorial_prompt.tscn",
}

def rename_file(old_path, new_path, dry_run=True):
    """Rename a file and its .import file if it exists"""
    old_path = Path(old_path)
    new_path = Path(new_path)
    
    if not old_path.exists():
        print(f"[SKIP] {old_path} - File not found")
        return False
    
    if dry_run:
        print(f"[DRY RUN] {old_path.name} -> {new_path.name}")
        # Check for .import file
        import_old = Path(str(old_path) + ".import")
        if import_old.exists():
            import_new = Path(str(new_path) + ".import")
            print(f"          + {import_old.name} -> {import_new.name}")
        return True
    else:
        # Actual rename
        print(f"[RENAME] {old_path.name} -> {new_path.name}")
        shutil.move(str(old_path), str(new_path))
        
        # Rename .import file if exists
        import_old = Path(str(old_path) + ".import")
        import_new = Path(str(new_path) + ".import")
        if import_old.exists():
            print(f"         + {import_old.name} -> {import_new.name}")
            shutil.move(str(import_old), str(import_new))
        
        return True

if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if dry_run:
        print("=" * 70)
        print("DRY RUN MODE - No files will be renamed")
        print("Run without --dry-run to apply changes")
        print("=" * 70)
        print()
    else:
        print("=" * 70)
        print("RENAMING FILES WITH ASSET TYPE PREFIXES")
        print("=" * 70)
        print()
    
    # Group by category for better readability
    categories = {
        "Tilesets": [],
        "Characters": [],
        "Enemies": [],
        "Collectibles": [],
        "Environment": [],
        "Backgrounds": [],
        "UI": [],
        "Scenes": []
    }
    
    for old_path, new_path in RENAME_MAP.items():
        if "tilesets" in old_path:
            categories["Tilesets"].append((old_path, new_path))
        elif "characters" in old_path:
            categories["Characters"].append((old_path, new_path))
        elif "enemies" in old_path and old_path.endswith(".png"):
            categories["Enemies"].append((old_path, new_path))
        elif "collectibles" in old_path and old_path.endswith(".png"):
            categories["Collectibles"].append((old_path, new_path))
        elif "environment" in old_path:
            categories["Environment"].append((old_path, new_path))
        elif "backgrounds" in old_path:
            categories["Backgrounds"].append((old_path, new_path))
        elif "ui" in old_path and old_path.endswith(".png"):
            categories["UI"].append((old_path, new_path))
        elif old_path.endswith(".tscn"):
            categories["Scenes"].append((old_path, new_path))
    
    renamed_count = 0
    skipped_count = 0
    
    for category, files in categories.items():
        if files:
            print(f"\n{category}:")
            print("-" * 70)
            for old_path, new_path in files:
                if rename_file(old_path, new_path, dry_run):
                    renamed_count += 1
                else:
                    skipped_count += 1
    
    print()
    print("=" * 70)
    if dry_run:
        print(f"Would rename: {renamed_count} files")
        print(f"Would skip: {skipped_count} files (not found)")
        print()
        print("Run without --dry-run to apply changes")
    else:
        print(f"Renamed: {renamed_count} files")
        print(f"Skipped: {skipped_count} files (not found)")
        print()
        print("IMPORTANT: Godot will show missing dependencies.")
        print("You'll need to relink scenes and resources manually.")
        print("Consider using Godot's 'Reload Current Project' after renaming.")
    print("=" * 70)
