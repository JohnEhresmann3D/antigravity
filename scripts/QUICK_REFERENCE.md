# Player Controller - Quick Reference

## Files Created

### Core Scripts
- `scripts/autoload/gravity_manager.gd` - Global gravity system
- `scripts/player/player.gd` - Main player controller  
- `scripts/gravity/gravity_zone.gd` - Gravity zone areas

### Documentation
- `scripts/PLAYER_SETUP_GUIDE.txt` - Complete setup instructions

---

## Quick Setup Checklist

### 1. Autoload Setup
```
Project → Project Settings → Autoload
Add: res://scripts/autoload/gravity_manager.gd
Name: GravityManager
```

### 2. Input Actions
```
Project → Project Settings → Input Map

Add actions:
- move_left (A, Left Arrow)
- move_right (D, Right Arrow)
- jump (Space, W, Up Arrow)
- run (Shift)
- gravity_flip (E, Q)
```

### 3. Player Scene Structure
```
Player (CharacterBody2D) [player.gd]
├── AnimatedSprite2D
└── CollisionShape2D (RectangleShape2D, ~40x56)
```

### 4. Animations Required
```
idle (4f, 8fps, loop)
walk (6f, 10fps, loop)
run (6f, 12fps, loop)
jump (4f, 12fps, no loop)
fall (3f, 10fps, loop)
land (3f, 15fps, no loop)
gravity_flip (6f, 12fps, no loop)
damage (3f, 15fps, no loop)
```

---

## Key Features

### Movement System
- **Acceleration/Friction**: Smooth, responsive movement
- **Run Mode**: Hold Shift for faster movement
- **Sprite Flipping**: Auto-flips based on direction

### Jump System
- **Variable Height**: Release jump early for short hops
- **Coyote Time**: 0.1s grace period after leaving platform
- **Jump Buffering**: Press jump 0.1s before landing
- **Gravity-Aware**: Jumps opposite to gravity direction

### Gravity System
- **Modular Design**: Separate GravityManager singleton
- **Flip Ability**: Rotate 180° (unlockable)
- **Gravity Zones**: Custom gravity areas
- **Directional**: Supports any gravity direction

---

## Default Parameters

```gdscript
# Movement
move_speed = 200.0
run_speed = 300.0
acceleration = 1000.0
friction = 800.0

# Jump
jump_velocity = -400.0
jump_cut_multiplier = 0.5
coyote_time = 0.1
jump_buffer_time = 0.1

# Gravity
fall_gravity_multiplier = 1.5
max_fall_speed = 500.0

# Abilities
has_gravity_flip = false
gravity_flip_cooldown = 0.5
```

---

## Testing Controls

### Keyboard
- **Move**: A/D or Arrow Keys
- **Jump**: Space, W, or Up Arrow
- **Run**: Hold Shift
- **Gravity Flip**: E or Q (when unlocked)

### Debug Mode
Enable in `gravity_manager.gd`:
```gdscript
var debug_mode: bool = true
```
Then use arrow keys to change gravity direction.

---

## Common Functions

### Player Controller

```gdscript
# Unlock gravity flip ability
player.unlock_gravity_flip()

# Take damage
player.take_damage(1)
```

### Gravity Manager

```gdscript
# Flip gravity 180°
GravityManager.flip_gravity()

# Set cardinal direction
GravityManager.set_cardinal_direction("up")

# Set custom direction
GravityManager.set_gravity_direction(Vector2.LEFT)

# Adjust strength
GravityManager.set_gravity_strength(0.5)

# Reset to default
GravityManager.reset_gravity()
```

---

## Gravity Zone Setup

```
GravityZone (Area2D) [gravity_zone.gd]
└── CollisionShape2D

Inspector Settings:
- Zone Type: Normal / Zero-G / Custom
- Custom Gravity Direction: Vector2
- Gravity Strength Multiplier: float
```

---

## Animation State Machine

```
Grounded:
  velocity.x == 0 → idle
  velocity.x != 0 && !running → walk
  velocity.x != 0 && running → run

Airborne:
  velocity.y < 0 → jump
  velocity.y > 0 → fall

Special:
  on_land → land (then → idle)
  gravity_flip → gravity_flip (then → previous)
  hit → damage (then → previous)
```

---

## Troubleshooting

**Player falls through floor**
- Check CollisionShape2D exists
- Verify TileMap collision layers

**Animations don't play**
- Check SpriteFrames configured
- Verify animation names match code
- Ensure node name is "AnimatedSprite2D"

**Gravity flip doesn't work**
- Set `has_gravity_flip = true`
- Check GravityManager in autoload
- Verify input action configured

**Movement feels wrong**
- Adjust speed/acceleration parameters
- Check delta time is being used
- Verify friction is applied

---

## Next Steps

1. Import sprite sheet
2. Configure animations
3. Set up input map
4. Create test level
5. Test movement
6. Add mobile controls
7. Implement abilities

---

## Architecture

```
GravityManager (Singleton)
    ↓
Player Controller
    ↓
CharacterBody2D.move_and_slide()

GravityZone → modifies GravityManager
```

**Modular**: Each system is independent  
**Extensible**: Easy to add new abilities  
**Mobile-Ready**: Optimized for performance
