# Project Naming Convention

**Project**: Antigravity  
**Created**: January 8, 2026  
**Updated**: January 8, 2026  
**Status**: Active Standard

---

## Overview

This document defines the naming conventions for all files and assets in the Antigravity project. Consistent naming improves organization, searchability, and collaboration.

**Key Feature:** Asset type prefixes allow instant identification of file types at a glance.

---

## Core Principles

1. **Asset type prefix** - Indicates what kind of file it is (`spr_`, `ts_`, `scn_`, etc.)
2. **Lowercase with underscores** (`snake_case`) for all files
3. **Descriptive names** that indicate content/purpose
4. **No spaces** in filenames
5. **No version numbers** in filenames (use git for versioning)
6. **Remove suffixes** like `_ai`, `_v2`, `_final` (use git history)

---

## Asset Type Prefixes

| Prefix | Type | Examples |
|--------|------|----------|
| `spr_` | Sprites (images) | `spr_char_cosmo.png`, `spr_enemy_turret.png` |
| `ts_` | Tilesets | `ts_level1_structure.png` |
| `bg_` | Backgrounds | `bg_space_station_layer1.png` |
| `ui_` | UI elements | `ui_button_normal.png`, `ui_health_heart.png` |
| `scn_` | Scenes (.tscn) | `scn_enemy_flyer_drone.tscn`, `scn_level_1.tscn` |
| `res_` | Resources (.tres) | `res_tileset_level1.tres`, `res_theme_main.tres` |
| `sfx_` | Sound effects | `sfx_player_jump.wav` |
| `music_` | Music tracks | `music_level1_exploration.ogg` |

---

## File Naming Patterns

### Sprites (Images)
```
spr_[category]_[name]_[variant].png
```

**Categories:** `char`, `enemy`, `item`, `env`, `proj`

**Examples:**
- `spr_char_cosmo.png`
- `spr_enemy_flyer_drone.png`
- `spr_item_gravity_core.png`
- `spr_env_breakable_wall.png`
- `spr_proj_energy_ball.png`

#### Enemies
```
enemy_[name]_[variant].png
```
**Examples:**
- `enemy_flyer_drone.png`
- `enemy_turret.png`
- `enemy_antigrav_orb.png`
- `enemy_antigrav_orb_glow.png` (for glow maps)

#### Projectiles
```
proj_[type]_[variant].png
```
**Examples:**
- `proj_energy_ball.png`
- `proj_laser_beam.png`
- `proj_turret_bullet.png`

#### Collectibles
```
item_[name]_[variant].png
```
**Examples:**
- `item_gravity_core.png`
- `item_health_pickup.png`
- `item_coin.png`

#### Environment Objects
```
env_[category]_[name].png
```
**Examples:**
- `env_hazard_spikes.png`
- `env_prop_crate.png`
- `env_deco_pipe_horizontal.png`
- `env_breakable_wall.png`

### 2. Tilesets

```
tileset_[level]_[category].png
```

**Categories:**
- `structure` - Walls, floors, platforms
- `props` - Decorative elements, furniture
- `hazards` - Spikes, lasers, etc.
- `interactive` - Doors, switches, breakables

**Examples:**
- `tileset_level1_structure.png`
- `tileset_level1_props.png`
- `tileset_level1_hazards.png`
- `tileset_industrial_structure.png`

### 3. Backgrounds

```
bg_[theme]_[layer].png
```

**Examples:**
- `bg_space_station_layer1.png` (far background)
- `bg_space_station_layer2.png` (mid background)
- `bg_space_station_layer3.png` (near background)
- `bg_industrial_parallax.png`

### 4. UI Elements

```
ui_[element]_[state].png
```

**Examples:**
- `ui_button_normal.png`
- `ui_button_hover.png`
- `ui_button_pressed.png`
- `ui_health_heart_full.png`
- `ui_health_heart_empty.png`
- `ui_icon_gravity_core.png`

### 5. Audio

#### Music
```
music_[context]_[descriptor].ogg
```
**Examples:**
- `music_level1_exploration.ogg`
- `music_boss_battle.ogg`
- `music_menu_theme.ogg`

#### Sound Effects
```
sfx_[category]_[action].wav
```
**Examples:**
- `sfx_player_jump.wav`
- `sfx_player_land.wav`
- `sfx_enemy_death.wav`
- `sfx_item_collect.wav`
- `sfx_ui_click.wav`

---

## Scene Files (.tscn)

### Format
```
[category]_[name].tscn
```

**Categories:**
- `level_` - Level scenes
- `char_` - Character scenes
- `enemy_` - Enemy scenes
- `item_` - Collectible/pickup scenes
- `proj_` - Projectile scenes
- `ui_` - UI scenes
- `env_` - Environment object scenes

**Examples:**
- `level_1.tscn`
- `level_tutorial.tscn`
- `char_cosmo.tscn` (player)
- `enemy_flyer_drone.tscn`
- `item_gravity_core.tscn`
- `proj_energy_ball.tscn`
- `ui_main_menu.tscn`
- `ui_pause_menu.tscn`
- `env_moving_platform.tscn`
- `env_checkpoint.tscn`

---

## Script Files (.gd)

### Format
Match the scene name (without category prefix if obvious from folder)

**Examples:**
```
scripts/
├── player/
│   └── player.gd              (for char_cosmo.tscn)
├── enemies/
│   ├── flyer_drone.gd         (for enemy_flyer_drone.tscn)
│   └── turret.gd
├── components/
│   ├── health_component.gd
│   └── movement_component.gd
├── autoload/
│   └── gravity_manager.gd
└── ui/
    └── game_hud.gd
```

**Singletons/Autoloads:**
- Use descriptive names: `gravity_manager.gd`, `game_state.gd`, `audio_manager.gd`

---

## Resource Files (.tres)

### Format
```
[type]_[name].tres
```

**Examples:**
- `tileset_level1.tres`
- `material_glow_cyan.tres`
- `theme_main_ui.tres`
- `anim_cosmo_idle.tres`

---

## Folder Structure

```
assets/
├── sprites/
│   ├── characters/
│   ├── enemies/
│   ├── projectiles/
│   ├── collectibles/
│   ├── environment/
│   ├── tilesets/
│   └── ui/
├── backgrounds/
├── audio/
│   ├── music/
│   └── sfx/
└── fonts/

scenes/
├── levels/
├── player/
├── enemies/
├── collectibles/
├── projectiles/
├── ui/
└── environment/

scripts/
├── player/
├── enemies/
├── components/
├── ai/
├── gravity/
├── level/
├── ui/
└── autoload/

resources/
├── tilesets/
├── materials/
├── themes/
└── animations/
```

---

## Special Cases

### Glow Maps / Emission Maps
```
[original_name]_glow.png
[original_name]_emission.png
```
**Examples:**
- `enemy_antigrav_orb_glow.png`
- `item_gravity_core_emission.png`

### Animation Frames
```
[name]_anim_[frame].png
```
**Examples:**
- `char_cosmo_walk_01.png`
- `char_cosmo_walk_02.png`
- `enemy_flyer_idle_01.png`

### Sprite Sheets
```
[name]_spritesheet.png
```
**Examples:**
- `char_cosmo_spritesheet.png`
- `enemy_flyer_spritesheet.png`

---

## Migration Guide

### Current → New Naming

**Tilesets:**
- ❌ `tileset_level1_structure_ai.png`
- ✅ `tileset_level1_structure.png`

**Sprites:**
- ❌ `cosmo_spritesheet.png`
- ✅ `char_cosmo_spritesheet.png`

- ❌ `antigrav_orb.png`
- ✅ `enemy_antigrav_orb.png`

- ❌ `gravity_core.png`
- ✅ `item_gravity_core.png`

**Backgrounds:**
- ❌ `space_station_bg.png`
- ✅ `bg_space_station_layer1.png`

**Scenes:**
- ❌ `player.tscn`
- ✅ `char_cosmo.tscn` (or keep `player.tscn` if it's the only player)

---

## Exceptions

Some files can keep simpler names if they're unique:
- `player.tscn` / `player.gd` (if there's only one player character)
- `icon.svg` (Godot project icon)
- `project.godot` (Godot project file)

---

## Naming Checklist

Before creating/renaming a file, verify:
- [ ] Uses lowercase with underscores
- [ ] Has appropriate category prefix
- [ ] Descriptive and searchable
- [ ] No version numbers or dates
- [ ] No special characters or spaces
- [ ] Follows the pattern for its type
- [ ] Matches related files (e.g., scene + script)

---

## Benefits

✅ **Searchability**: Easy to find files with prefixes  
✅ **Organization**: Files auto-sort by category  
✅ **Clarity**: Purpose is obvious from filename  
✅ **Consistency**: Predictable naming across project  
✅ **Scalability**: Works as project grows  

---

**Status**: Active Standard  
**Last Updated**: January 8, 2026  
**Applies To**: All new files and renamed files
