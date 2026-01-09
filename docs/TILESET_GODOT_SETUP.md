# Tileset Setup Guide for Godot

**Created**: January 8, 2026  
**Purpose**: Instructions for importing and using AI-generated tilesets in Godot

---

## Quick Start

The AI-generated tilesets are ready to use in Godot! Import files have been created with optimal settings for pixel art.

---

## Files Location

```
assets/sprites/tilesets/
├── tileset_level1_structure_ai.png        (Walls & platforms)
├── tileset_level1_structure_ai.png.import (Import config)
├── tileset_level1_props_ai.png            (Decorative props)
├── tileset_level1_props_ai.png.import     (Import config)
├── tileset_level1_items_ai.png            (Collectibles & hazards)
└── tileset_level1_items_ai.png.import     (Import config)
```

---

## Import Settings

All tilesets are configured with:
- ✅ **No compression** (`compress/mode=0`) - Preserves pixel-perfect quality
- ✅ **No mipmaps** - Prevents blurring
- ✅ **detect_3d disabled** - Optimized for 2D
- ✅ **Alpha border fix** - Prevents edge artifacts

---

## Creating TileSet Resources

### Method 1: Using Godot Editor (Recommended)

1. **Open Godot** and navigate to your project
2. **Create TileSet resource**:
   - Right-click in FileSystem
   - New Resource → TileSet
   - Save as `resources/tilesets/level1_tileset.tres`

3. **Add Structure Tiles**:
   - Open the TileSet resource
   - Click "Add Texture(s) to TileSet"
   - Select `tileset_level1_structure_ai.png`
   - Set **Tile Size**: 16x16
   - Set **Separation**: 2px (spacing between tiles)
   - Click "Create from Scene"

4. **Configure Collision** (for walls and platforms):
   - Select each platform/wall tile
   - Click "Collision" tab
   - Draw collision shapes (rectangles for solid tiles)
   - For platforms: Use one-way collision (enable "One Way Collision")

5. **Add Props and Items**:
   - Repeat steps 3-4 for `tileset_level1_props_ai.png`
   - Repeat for `tileset_level1_items_ai.png`
   - Props typically don't need collision
   - Items (collectibles) should be separate scenes, not in tileset

---

## Tile Mapping

### Structure Tileset Layout

The structure tileset contains a **3x3 wall grid** and **platform tiles**:

```
Row 1: [TL Corner] [Top Edge] [TR Corner]
Row 2: [Left Edge] [Center]   [Right Edge]
Row 3: [BL Corner] [Bot Edge]  [BR Corner]

Row 4: [Platform L] [Platform M] [Platform R]
```

**Autotile Setup** (Optional):
- Create 3x3 bitmask for walls
- Godot will auto-select correct tile based on neighbors

### Props Tileset

Individual decorative elements:
- Computer terminal
- Pipes (horizontal/vertical)
- Crates, barrels
- Warning signs
- Doors (closed/open)
- Windows
- Vents

### Items Tileset

Game objects (consider making these **separate scenes** instead):
- Gravity cores (collectible)
- Coins
- Health pickups
- Hazards (spikes, lasers)
- Checkpoints
- Special tiles (teleporter, gravity zones)

---

## Creating a Level with TileMap

### 1. Create Level Scene

```
Level1 (Node2D)
├── Background (ParallaxBackground)
├── TileMap (TileMap)
├── Collectibles (Node2D)
└── Player (CharacterBody2D)
```

### 2. Configure TileMap

1. **Add TileMap node** to your level scene
2. **Assign TileSet**: 
   - Inspector → TileSet → Load `level1_tileset.tres`
3. **Create Layers**:
   - Layer 0: Background decorations (props)
   - Layer 1: Walls (collision enabled)
   - Layer 2: Platforms (collision enabled)

### 3. Paint Tiles

1. **Select layer** in TileMap editor
2. **Choose tile** from palette
3. **Paint** by clicking in the scene
4. **Use bucket fill** for large areas
5. **Use line tool** for platforms

---

## Tile Size Reference

All tiles are **16x16 pixels** with **2px spacing** in the tileset image.

**In Godot TileMap**:
- Cell Size: 16x16
- Separation: 2
- Texture Filter: Nearest (for pixel art)

---

## Collision Setup

### Walls (Full Collision)
```gdscript
# Full tile collision (16x16 rectangle)
collision_shape = RectangleShape2D.new()
collision_shape.extents = Vector2(8, 8)  # Half of 16x16
```

### Platforms (One-Way Collision)
```gdscript
# Top surface only
collision_shape = RectangleShape2D.new()
collision_shape.extents = Vector2(8, 2)  # Thin top surface
# Enable "One Way Collision" in TileSet
```

---

## Testing in Godot

### Quick Test Scene

1. **Create test scene**: `scenes/test_tileset.tscn`
2. **Add TileMap** with your tileset
3. **Paint some tiles**:
   - Build a small platform
   - Add walls
   - Place decorative props
4. **Add player** (if available)
5. **Run scene** (F6) to test

### What to Check

- ✅ Tiles render crisp (no blurring)
- ✅ Collision works correctly
- ✅ Colors match design (light gray, blue-gray, cyan)
- ✅ Tiles align properly (no gaps or overlaps)
- ✅ Platform one-way collision allows jumping through

---

## Common Issues

### Blurry Tiles
**Fix**: Ensure texture filter is set to "Nearest"
- Project Settings → Rendering → Textures → Default Texture Filter → Nearest

### Gaps Between Tiles
**Fix**: Check separation setting
- TileSet → Separation should be 2px

### Collision Not Working
**Fix**: Verify collision shapes are created
- Open TileSet resource
- Select tile → Collision tab
- Draw collision rectangle

### Wrong Colors
**Fix**: Check import settings
- Ensure `compress/mode=0` (no compression)
- Reimport texture if needed

---

## Advanced: Autotiling

For the 3x3 wall grid, you can set up **autotiling**:

1. **Select wall tiles** in TileSet
2. **Enable Autotile**
3. **Set Bitmask Mode**: 3x3 (minimal)
4. **Configure bitmask** for each tile:
   ```
   TL Corner: ┌─
   Top Edge:  ──
   TR Corner: ─┐
   Left Edge: │
   Center:    (all sides)
   Right Edge: │
   BL Corner: └─
   Bot Edge:  ──
   BR Corner: ─┘
   ```
5. **Paint walls**: Godot auto-selects correct tile!

---

## Next Steps

1. ✅ Import tilesets into Godot
2. ✅ Create TileSet resource
3. ✅ Build test level
4. ✅ Configure collision
5. [ ] Create Level 1 layout (see LEVEL_1_DESIGN.md)
6. [ ] Add collectibles as separate scenes
7. [ ] Test with player controller

---

## Related Documentation

- [TILESET_GENERATION_PROMPTS.md](file:///d:/GameDevelopment/Godot/Games/antigravity/docs/TILESET_GENERATION_PROMPTS.md) - AI prompt documentation
- [LEVEL_1_DESIGN.md](file:///d:/GameDevelopment/Godot/Games/antigravity/docs/LEVEL_1_DESIGN.md) - Level 1 layout and design

---

**Status**: Ready for Godot import  
**Last Updated**: January 8, 2026
