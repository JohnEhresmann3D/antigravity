# Animation Setup Guide - Godot 4.5

## Overview

This guide walks you through setting up animations in Godot for the Antigravity game. The scene files and scripts are already created - you just need to configure the SpriteFrames for each character.

## Prerequisites

✅ All sprite sheets imported and visible in Godot  
✅ Scene files generated (player, enemies, projectiles)  
✅ Animation frame data JSON files created

## Quick Start

For each character, you'll need to:
1. Open the scene in Godot
2. Select the AnimatedSprite2D node
3. Create a new SpriteFrames resource
4. Add animations and configure frames
5. Set FPS and loop settings

---

## Part 1: Player (Cosmo) Animations

### Step 1: Open Player Scene

1. In Godot, navigate to `scenes/player/player.tscn`
2. Double-click to open the scene
3. In the Scene tree, select the `AnimatedSprite2D` node

### Step 2: Create SpriteFrames Resource

1. In the Inspector (right panel), find the `Sprite Frames` property
2. Click the dropdown and select `New SpriteFrames`
3. Click the SpriteFrames resource to open the bottom panel

### Step 3: Configure Animations

You'll see the SpriteFrames editor at the bottom. Now add each animation:

#### Animation: idle
1. Click "New Animation" button (+ icon)
2. Name it: `idle`
3. Set FPS: `8`
4. Enable Loop (toggle the loop icon)
5. Click "Add frames from sprite sheet" button
6. Select `cosmo_spritesheet.png`
7. In the grid dialog:
   - Set Horizontal: `6`, Vertical: `8`
   - Select frames from Row 1: frames 0-3 (first 4 frames)
8. Click "Add frames"

#### Animation: walk
1. New Animation: `walk`
2. FPS: `10`, Loop: ON
3. Add frames from sprite sheet
4. Select Row 2: frames 0-5 (all 6 frames)

#### Animation: run
1. New Animation: `run`
2. FPS: `12`, Loop: ON
3. Add frames from sprite sheet
4. Select Row 3: frames 0-5 (all 6 frames)

#### Animation: jump
1. New Animation: `jump`
2. FPS: `12`, Loop: OFF
3. Add frames from sprite sheet
4. Select Row 4: frames 0-3 (4 frames)

#### Animation: fall
1. New Animation: `fall`
2. FPS: `10`, Loop: ON
3. Add frames from sprite sheet
4. Select Row 5: frames 0-2 (3 frames)

#### Animation: land
1. New Animation: `land`
2. FPS: `15`, Loop: OFF
3. Add frames from sprite sheet
4. Select Row 6: frames 0-2 (3 frames)

#### Animation: gravity_flip
1. New Animation: `gravity_flip`
2. FPS: `12`, Loop: OFF
3. Add frames from sprite sheet
4. Select Row 7: frames 0-5 (6 frames)

#### Animation: damage
1. New Animation: `damage`
2. FPS: `15`, Loop: OFF
3. Add frames from sprite sheet
4. Select Row 8: frames 0-2 (3 frames)

### Step 4: Test Player Animations

1. Save the scene (Ctrl+S)
2. Run the scene (F6)
3. The player should appear with idle animation playing
4. Press arrow keys to test walk/run
5. Press Space to test jump

---

## Part 2: Flyer Drone Enemy

### Setup

1. Open `scenes/enemies/flyer_drone.tscn`
2. Select `AnimatedSprite2D` node
3. Create new SpriteFrames resource

### Animations

**Sprite Sheet**: `flyer_drone.png` (32x32 frames)

#### idle
- FPS: `8`, Loop: ON
- Row 1, frames 0-5 (6 frames)

#### flying
- FPS: `10`, Loop: ON
- Row 2, frames 0-5 (6 frames)

#### alert
- FPS: `12`, Loop: OFF
- Row 3, frames 0-3 (4 frames)

#### damaged
- FPS: `15`, Loop: OFF
- Row 4, frames 0-2 (3 frames)

---

## Part 3: Turret Enemy

### Setup

1. Open `scenes/enemies/turret.tscn`
2. Select `AnimatedSprite2D` node
3. Create new SpriteFrames resource

### Animations

**Sprite Sheet**: `turret.png` (32x32 frames)

#### idle
- FPS: `6`, Loop: ON
- Row 1, frames 0-3 (4 frames)

#### aiming
- FPS: `10`, Loop: OFF
- Row 2, frames 0-3 (4 frames)

#### firing
- FPS: `12`, Loop: OFF
- Row 3, frames 0-5 (6 frames)

#### damaged
- FPS: `15`, Loop: OFF
- Row 4, frames 0-2 (3 frames)

---

## Part 4: Antigrav Orb Enemy

### Setup

1. Open `scenes/enemies/antigrav_orb.tscn`
2. Select `AnimatedSprite2D` node
3. Create new SpriteFrames resource

> **Note**: The antigrav orb sprite sheet has been optimized for grid alignment. All visual effects (sparkles, energy bursts, trails) are contained within the 32x32 frame boundaries, making it easy to select frames in the grid editor.

### Animations

**Sprite Sheet**: `antigrav_orb.png` (32x32 frames)

#### idle
- FPS: `8`, Loop: ON
- Row 1, frames 0-5 (6 frames)

#### gravity_flip
- FPS: `12`, Loop: OFF
- Row 2, frames 0-5 (6 frames)

#### patrol
- FPS: `10`, Loop: ON
- Row 3, frames 0-5 (6 frames)

#### damaged
- FPS: `15`, Loop: OFF
- Row 4, frames 0-2 (3 frames)

---

## Part 5: Projectiles

### Energy Ball

1. Open `scenes/projectiles/energy_ball.tscn`
2. Select `AnimatedSprite2D` node
3. Create new SpriteFrames resource
4. Add animation: `energy_ball`
   - FPS: `12`, Loop: ON
   - Sprite sheet: `projectiles.png`
   - Frame size: 16x16
   - Select first 4 frames from top row

---

## Tips & Tricks

### Grid Configuration

When adding frames from sprite sheet, use these grid settings:

- **Cosmo (64x64)**: Horizontal: 6, Vertical: 8
- **Enemies (32x32)**: Horizontal: 32, Vertical: 32
- **Projectiles**: Varies by type

### Selecting Frames

- Click and drag to select multiple frames
- Hold Shift to select a range
- The frames will be added in the order you select them

### Testing Animations

- Use the animation preview in the SpriteFrames editor
- Click the play button next to each animation
- Adjust FPS if animations feel too fast/slow

### Common Issues

**Animation doesn't play:**
- Check that the animation name in code matches exactly
- Verify Loop is enabled for looping animations
- Make sure FPS is set (not 0)

**Frames are wrong:**
- Double-check you selected the correct row
- Verify frame count matches the guide
- Delete and re-add frames if needed

**Sprite looks pixelated:**
- Select AnimatedSprite2D node
- In Inspector, set Texture > Filter to "Nearest"
- This gives crisp pixel art look

---

## Verification Checklist

After setting up all animations, verify:

- [ ] Player has all 8 animations configured
- [ ] Flyer Drone has 4 animations
- [ ] Turret has 4 animations
- [ ] Antigrav Orb has 4 animations
- [ ] Energy Ball projectile animated
- [ ] All animations play smoothly in preview
- [ ] FPS settings match the guide
- [ ] Loop settings are correct

---

## Next Steps

Once animations are configured:

1. **Test each scene individually** - Run each enemy scene to see animations
2. **Create a test level** - Add player and enemies to test interactions
3. **Adjust as needed** - Fine-tune FPS and timing based on feel
4. **Add particle effects** - Enhance with visual effects
5. **Implement sound** - Add audio cues for actions

---

## Need Help?

**Reference Files:**
- Frame data: `resources/animation_data/*.json`
- Sprite guides: `assets/sprites/*/GUIDE.txt`
- Quick reference: `scripts/QUICK_REFERENCE.md`

**Common Questions:**

Q: Can I change the FPS later?  
A: Yes! Just select the animation and adjust the FPS value.

Q: How do I add more animations?  
A: Click "New Animation" and follow the same process.

Q: Can I preview animations without running the scene?  
A: Yes, use the play button in the SpriteFrames editor.

---

**Estimated Time**: 30-45 minutes for all characters

Good luck! 🚀
