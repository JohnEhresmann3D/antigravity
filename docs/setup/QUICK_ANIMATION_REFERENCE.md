# Animation Quick Reference

## Player (Cosmo)
**Sprite**: `cosmo_spritesheet.png` | **Size**: 64x64

| Animation | Frames | FPS | Loop | Row |
|-----------|--------|-----|------|-----|
| idle | 4 | 8 | ✓ | 1 |
| walk | 6 | 10 | ✓ | 2 |
| run | 6 | 12 | ✓ | 3 |
| jump | 4 | 12 | ✗ | 4 |
| fall | 3 | 10 | ✓ | 5 |
| land | 3 | 15 | ✗ | 6 |
| gravity_flip | 6 | 12 | ✗ | 7 |
| damage | 3 | 15 | ✗ | 8 |

---

## Flyer Drone
**Sprite**: `flyer_drone.png` | **Size**: 32x32

| Animation | Frames | FPS | Loop | Row |
|-----------|--------|-----|------|-----|
| idle | 6 | 8 | ✓ | 1 |
| flying | 6 | 10 | ✓ | 2 |
| alert | 4 | 12 | ✗ | 3 |
| damaged | 3 | 15 | ✗ | 4 |

**Stats**: HP: 2 | Speed: 100 | Damage: 1

---

## Turret
**Sprite**: `turret.png` | **Size**: 32x32

| Animation | Frames | FPS | Loop | Row |
|-----------|--------|-----|------|-----|
| idle | 4 | 6 | ✓ | 1 |
| aiming | 4 | 10 | ✗ | 2 |
| firing | 6 | 12 | ✗ | 3 |
| damaged | 3 | 15 | ✗ | 4 |

**Stats**: HP: 3 | Fire Rate: 2.0s | Range: 300

---

## Antigrav Orb
**Sprite**: `antigrav_orb.png` | **Size**: 32x32

| Animation | Frames | FPS | Loop | Row |
|-----------|--------|-----|------|-----|
| idle | 6 | 8 | ✓ | 1 |
| gravity_flip | 6 | 12 | ✗ | 2 |
| patrol | 6 | 10 | ✓ | 3 |
| damaged | 3 | 15 | ✗ | 4 |

**Stats**: HP: 2 | Speed: 80 | Ignores Gravity: ✓

---

## Projectiles
**Sprite**: `projectiles.png`

| Type | Size | Frames | FPS | Row | Speed |
|------|------|--------|-----|-----|-------|
| Energy Ball | 16x16 | 4 | 12 | 1 | 200 |
| Laser Bolt | 24x8 | 4 | 15 | 2 | 300 |
| Plasma Shot | 16x16 | 4 | 10 | 3 | 150 |
| Impact | 32x32 | 6 | 15 | 4 | - |

---

## Grid Settings for Sprite Sheets

- **Cosmo**: Horizontal: 6, Vertical: 8
- **Enemies**: Horizontal: 32, Vertical: 32
- **Projectiles**: Varies (see individual sizes)

---

## File Locations

**Scenes**:
- `scenes/player/player.tscn`
- `scenes/enemies/flyer_drone.tscn`
- `scenes/enemies/turret.tscn`
- `scenes/enemies/antigrav_orb.tscn`
- `scenes/projectiles/energy_ball.tscn`

**Scripts**:
- `scripts/player/player.gd`
- `scripts/enemies/flyer_drone.gd`
- `scripts/enemies/turret.gd`
- `scripts/enemies/antigrav_orb.gd`
- `scripts/projectiles/projectile.gd`

**Data**:
- `resources/animation_data/*.json`

---

## Animation State Transitions

```
Player:
idle → walk → run → jump → fall → land → idle
any → damage → previous
any → gravity_flip → previous

Enemies:
idle → alert → chase/attack → damaged → idle
```
