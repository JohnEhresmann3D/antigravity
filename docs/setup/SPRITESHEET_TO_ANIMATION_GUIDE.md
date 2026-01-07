# Sprite Sheet to Animation - Visual Guide

## Quick Overview

This guide shows you **exactly** how to turn a sprite sheet into animations in Godot with screenshots and step-by-step instructions.

---

## Step 1: Open Your Scene

1. In Godot's **FileSystem** panel (bottom-left), navigate to your scene
2. Double-click to open (e.g., `scenes/player/player.tscn`)

---

## Step 2: Select AnimatedSprite2D

1. In the **Scene** panel (top-left), click on `AnimatedSprite2D` node
2. The **Inspector** panel (right side) will show its properties

---

## Step 3: Create SpriteFrames Resource

1. In the Inspector, find the **Sprite Frames** property
2. Click the dropdown next to `[empty]`
3. Select **New SpriteFrames**
4. Click on the newly created SpriteFrames resource to open the editor

**Result**: The SpriteFrames editor panel opens at the bottom of the screen

---

## Step 4: Add Your First Animation

### Create Animation
1. In the SpriteFrames panel (bottom), click the **"+"** button (New Animation)
2. Type the animation name: `idle`
3. Press Enter

### Set Animation Properties
1. With `idle` selected, look at the top of the SpriteFrames panel
2. Set **FPS**: `8` (use the number field)
3. Click the **Loop** icon (circular arrows) to enable looping

---

## Step 5: Add Frames from Sprite Sheet

### Open Sprite Sheet Dialog
1. Click the **"Add frames from sprite sheet"** button (grid icon with +)
2. A file browser opens - navigate to your sprite sheet
3. Select `cosmo_spritesheet.png` and click **Open**

### Configure Grid
A dialog appears showing your sprite sheet with a grid overlay:

1. **Horizontal**: `6` (number of columns)
2. **Vertical**: `8` (number of rows)
3. **Size**: Should auto-calculate to `64x64`

**Visual**: You should see a grid dividing your sprite sheet into frames

### Select Frames
1. **For idle animation**: Click frames in Row 1, columns 0-3 (first 4 frames)
   - Click and drag to select multiple frames
   - Selected frames highlight in blue
2. Click **Add X Frame(s)** button at the bottom

**Result**: The frames appear in the animation timeline at the bottom

---

## Step 6: Preview Animation

1. In the SpriteFrames panel, click the **Play** button (▶) next to the animation name
2. Watch your animation play in the preview!
3. If it's too fast/slow, adjust the FPS value

---

## Step 7: Add More Animations

Repeat Steps 4-6 for each animation:

### Example: Walk Animation
1. Click **"+"** to create new animation
2. Name it: `walk`
3. Set FPS: `10`, Loop: ON
4. Add frames from sprite sheet
5. Select Row 2, frames 0-5 (6 frames)
6. Add frames

### Quick Reference Table

| Animation | Row | Frames | FPS | Loop |
|-----------|-----|--------|-----|------|
| idle | 1 | 0-3 (4) | 8 | ✓ |
| walk | 2 | 0-5 (6) | 10 | ✓ |
| run | 3 | 0-5 (6) | 12 | ✓ |
| jump | 4 | 0-3 (4) | 12 | ✗ |
| fall | 5 | 0-2 (3) | 10 | ✓ |
| land | 6 | 0-2 (3) | 15 | ✗ |
| gravity_flip | 7 | 0-5 (6) | 12 | ✗ |
| damage | 8 | 0-2 (3) | 15 | ✗ |

---

## Step 8: Save and Test

1. **Save the scene**: Press `Ctrl+S`
2. **Run the scene**: Press `F6`
3. The idle animation should play automatically!

---

## Visual Tips

### How to Select Frames
```
Grid View:
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  0  │  1  │  2  │  3  │  4  │  5  │ ← Row 1 (idle)
├─────┼─────┼─────┼─────┼─────┼─────┤
│  0  │  1  │  2  │  3  │  4  │  5  │ ← Row 2 (walk)
└─────┴─────┴─────┴─────┴─────┴─────┘

For idle: Select Row 1, frames 0-3
For walk: Select Row 2, frames 0-5
```

### Frame Selection Methods
- **Click**: Select single frame
- **Click + Drag**: Select multiple frames
- **Shift + Click**: Select range
- **Ctrl + Click**: Add to selection

---

## Common Issues & Fixes

### ❌ Grid doesn't align with sprites
**Fix**: Adjust Horizontal/Vertical values until grid matches sprite layout

### ❌ Animation plays too fast/slow
**Fix**: Adjust FPS value (lower = slower, higher = faster)

### ❌ Animation doesn't loop
**Fix**: Click the Loop icon (circular arrows) to enable

### ❌ Sprite looks blurry
**Fix**: 
1. Select AnimatedSprite2D node
2. In Inspector, expand **Texture**
3. Set **Filter** to **Nearest**

### ❌ Background isn't transparent
**Fix**: Already fixed! Sprites are now RGBA with transparency

---

## Keyboard Shortcuts

- `Ctrl+S` - Save scene
- `F6` - Run current scene
- `F5` - Run project
- `Ctrl+Z` - Undo
- `Delete` - Remove selected frame

---

## Next Steps

1. **Add all 8 player animations** (30 minutes)
2. **Test each animation** by running the scene
3. **Repeat for enemies** (15 minutes each)
4. **Create a test level** to see everything in action

---

## Need More Help?

- **Full guide**: See `ANIMATION_SETUP_GUIDE.md`
- **Quick reference**: See `QUICK_ANIMATION_REFERENCE.md`
- **Frame data**: Check `resources/animation_data/*.json`

---

**Estimated Time**: 10-15 minutes per character once you get the hang of it!

🎮 Happy animating!
