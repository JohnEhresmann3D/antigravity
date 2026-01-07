# Component Library - Usage Guide

## Overview

This component library provides reusable, modular components for building game entities in Godot. All components follow a consistent pattern and can be mixed and matched to create different entity behaviors.

## Core Components

### HealthComponent
**Purpose**: Manage entity health, damage, and death  
**Signals**: `health_changed`, `died`, `damaged`, `healed`

```gdscript
# Add to scene
var health = $HealthComponent

# Usage
health.take_damage(10, attacker)
health.heal(5)
health.set_invincible(2.0)

# Listen to events
health.died.connect(_on_died)
health.damaged.connect(_on_damaged)
```

### MovementComponent
**Purpose**: Handle physics-based movement  
**Signals**: `velocity_changed`

```gdscript
var movement = $MovementComponent

# Set target velocity
movement.set_target_direction(Vector2.RIGHT, true)

# Update physics
movement.update(delta)
velocity = movement.velocity
move_and_slide()

# Apply forces
movement.apply_impulse(Vector2(200, -300))
```

### DamageComponent
**Purpose**: Deal damage to other entities  
**Signals**: `hit_target`, `hit_blocked`

```gdscript
var damage = $DamageComponent

# Configure
damage.damage = 5
damage.knockback_force = 300.0
damage.damage_groups = ["player", "enemy"]

# Listen
damage.hit_target.connect(_on_hit_target)
```

### CollectibleComponent
**Purpose**: Handle collectible pickup  
**Signals**: `collected`, `collection_failed`

```gdscript
var collectible = $CollectibleComponent

# Configure
collectible.collectible_type = "coin"
collectible.point_value = 10

# Manual collection
collectible.collect(player)
```

### AnimationControllerComponent
**Purpose**: Manage animations  
**Signals**: `animation_changed`

```gdscript
var anim = $AnimationControllerComponent

# Play animations
anim.play("walk")
anim.play_if_not("idle", ["jump", "attack"])

# Sprite flipping
anim.set_sprite_direction(velocity)
```

## AI Components

### PatrolAI
**Purpose**: Waypoint-based patrol behavior  
**Signals**: `reached_waypoint`, `patrol_direction_changed`

```gdscript
var patrol = $PatrolAI

# Configure waypoints
patrol.patrol_points = [Vector2(0, 0), Vector2(100, 0), Vector2(100, 100)]
patrol.patrol_speed = 100.0
patrol.loop_patrol = true

# Get movement
var target_vel = patrol.get_target_velocity()
```

### ChaseAI
**Purpose**: Chase and pursue targets  
**Signals**: `target_acquired`, `target_lost`, `target_in_range`

```gdscript
var chase = $ChaseAI

# Configure
chase.chase_speed = 150.0
chase.detection_range = 200.0
chase.target_groups = ["player"]

# Get movement
var target_vel = chase.get_target_velocity()

# Check state
if chase.has_target():
    print("Chasing: ", chase.get_target())
```

### TurretAI
**Purpose**: Stationary turret with aiming and firing  
**Signals**: `target_acquired`, `ready_to_fire`, `fired`

```gdscript
var turret = $TurretAI

# Configure
turret.fire_rate = 2.0
turret.projectile_scene = preload("res://scenes/projectiles/energy_ball.tscn")
turret.rotation_speed = 180.0

# Fires automatically when target in range
```

## Common Patterns

### Basic Enemy
```
Enemy (CharacterBody2D)
├── HealthComponent
├── MovementComponent
├── DamageComponent
├── AnimationControllerComponent
└── ChaseAI or PatrolAI
```

### Player Character
```
Player (CharacterBody2D)
├── HealthComponent
├── MovementComponent
├── AnimationControllerComponent
└── player.gd (input handling)
```

### Collectible
```
Coin (Area2D)
├── CollectibleComponent
├── AnimationControllerComponent
└── coin.gd (minimal)
```

## Best Practices

1. **One responsibility per component** - Keep components focused
2. **Use signals for communication** - Avoid tight coupling
3. **Export key values** - Make components configurable in editor
4. **Test components independently** - Verify behavior in isolation
5. **Reuse, don't duplicate** - Share components across entities

## Next Steps

- Refactor existing entities to use components
- Create entity templates with common component combinations
- Build level-specific variants by adjusting component exports
