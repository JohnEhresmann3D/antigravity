# Gravity Stamina System - Technical Specification

**Document ID**: SPEC-GRAVITY-STAMINA-001  
**Created**: January 7, 2026  
**Status**: Active  
**Related**: GDD-2026-01-07-UPDATED

---

## 🎯 Overview

The **Gravity Stamina System** is a resource management mechanic that governs the player's ability to manipulate gravity. It adds strategic depth by requiring players to manage when and how long they maintain altered gravity states.

---

## 🔧 Core Mechanics

### Stamina Resource
- **Type**: Depleting/regenerating resource
- **Range**: 0-100 (percentage-based)
- **Visual**: Displayed as stamina bar in UI
- **Purpose**: Limits duration of gravity manipulation

### Stamina States

#### **1. Normal State** (Default Gravity)
- Stamina **regenerates** over time
- Player can move freely
- No stamina cost

#### **2. Flipped State** (Gravity Flip Active)
- Stamina **drains** over time
- Player maintains flipped gravity
- Drain rate affected by gravity zones

#### **3. Depleted State** (0% Stamina)
- **Auto-flip** back to normal gravity
- **Recharge delay**: 2 seconds before regeneration starts
- Player cannot flip again until stamina > 0

---

## 📊 Default Parameters (Designer-Configurable)

All parameters are exposed via `@export` for designer tuning:

```gdscript
# Stamina Capacity
@export var max_stamina: float = 100.0

# Drain Rate (while gravity is flipped)
@export var stamina_drain_rate: float = 10.0  # 10% per second = 10 second duration

# Restore Rate (while in normal gravity)
@export var stamina_restore_rate: float = 16.67  # ~6 seconds to full recharge

# Depletion Penalty
@export var stamina_depletion_delay: float = 2.0  # 2 second delay before recharge starts

# Minimum stamina to flip
@export var min_stamina_to_flip: float = 5.0  # Need at least 5% to activate
```

### Default Timings
- **Full Duration**: 10 seconds (at 100% stamina)
- **Full Recharge**: 6 seconds (from 0% to 100%)
- **Depletion Penalty**: 2 seconds (no regeneration)
- **Total Recovery**: 8 seconds (2s delay + 6s recharge)

---

## 🌍 Gravity Zone Interactions

Stamina drain rate is **modified by gravity zones** based on gravity strength:

### Zone Multipliers

| Zone Type | Gravity Strength | Stamina Drain Multiplier |
|-----------|------------------|--------------------------|
| **Half Gravity** | 0.5x | **0.5x** (drains slower) |
| **Normal Gravity** | 1.0x | **1.0x** (standard drain) |
| **Double Gravity** | 2.0x | **2.0x** (drains faster) |
| **Zero-G** | 0.0x | **0.0x** (no drain!) |
| **Custom** | Variable | **Matches gravity strength** |

### Calculation
```gdscript
var effective_drain_rate = stamina_drain_rate * current_gravity_strength
```

### Examples
- **Half Gravity Zone** (0.5x): 10s duration → **20s duration** (stamina drains at 5%/s)
- **Double Gravity Zone** (2.0x): 10s duration → **5s duration** (stamina drains at 20%/s)
- **Zero-G Zone** (0.0x): **Infinite duration** (no stamina drain)

### Strategic Implications
- **Zero-G zones** = Safe havens (no stamina cost)
- **Double gravity zones** = High risk (stamina drains fast)
- **Half gravity zones** = Extended exploration (stamina lasts longer)

---

## 🎮 Directional Gravity Control

### Input Method: "Gravity Mode" Toggle (Option B)

#### Activation
1. **Press G** to enter "Gravity Mode"
2. **Arrow Keys** (↑↓←→) set gravity direction
3. **Press G again** to exit "Gravity Mode"

#### Visual Feedback
- **Gravity Mode Active**: 
  - UI indicator appears (e.g., "GRAVITY MODE" text)
  - Directional arrows appear around player
  - Slight screen tint or overlay
  
- **Gravity Mode Inactive**:
  - Normal movement controls
  - Arrow keys move player

#### Gravity Directions (4-Way Cardinal)
- **↑ (Up)**: Gravity pulls upward (walk on ceiling)
- **↓ (Down)**: Gravity pulls downward (normal)
- **← (Left)**: Gravity pulls left (walk on right wall)
- **→ (Right)**: Gravity pulls right (walk on left wall)

#### Stamina Cost
- **Changing direction**: No immediate cost
- **Maintaining non-default direction**: Drains stamina (same as gravity flip)
- **Default direction (Down)**: No stamina drain

---

## 🔄 State Machine

### Gravity States
```
┌─────────────────┐
│  NORMAL GRAVITY │ ← Default state, stamina regenerates
└────────┬────────┘
         │ Press G → Select direction
         ↓
┌─────────────────┐
│  GRAVITY MODE   │ ← Arrow keys change direction
└────────┬────────┘
         │ Press G → Confirm
         ↓
┌─────────────────┐
│ ALTERED GRAVITY │ ← Stamina drains (if not default)
└────────┬────────┘
         │ Stamina = 0
         ↓
┌─────────────────┐
│ FORCED NORMAL   │ ← 2 second delay
└────────┬────────┘
         │ After delay
         ↓
┌─────────────────┐
│ REGENERATING    │ ← Stamina restores
└─────────────────┘
```

### Stamina State Machine
```
REGENERATING ──────→ DRAINING ──────→ DEPLETED
     ↑                   │                │
     │                   │                │
     └───────────────────┴────────────────┘
     (After 2s delay)
```

---

## 💻 Implementation Specification

### Player Script Additions

```gdscript
# ============================================
# GRAVITY STAMINA SYSTEM
# ============================================

# Stamina Parameters (Designer-Configurable)
@export_group("Gravity Stamina")
@export var max_stamina: float = 100.0
@export var stamina_drain_rate: float = 10.0  # % per second
@export var stamina_restore_rate: float = 16.67  # % per second (~6s full recharge)
@export var stamina_depletion_delay: float = 2.0  # seconds
@export var min_stamina_to_flip: float = 5.0  # minimum % to activate

# Stamina State
var current_stamina: float = 100.0
var is_stamina_depleted: bool = false
var depletion_timer: float = 0.0

# Gravity State
var is_gravity_mode_active: bool = false
var current_gravity_direction: Vector2 = Vector2.DOWN
var default_gravity_direction: Vector2 = Vector2.DOWN

# Signals
signal stamina_changed(new_value: float, max_value: float)
signal stamina_depleted()
signal gravity_mode_toggled(active: bool)
signal gravity_direction_changed(new_direction: Vector2)


func _ready():
    current_stamina = max_stamina


func _process(delta):
    _update_stamina(delta)
    _handle_gravity_mode_input()


func _update_stamina(delta: float):
    # Handle depletion delay
    if is_stamina_depleted:
        depletion_timer -= delta
        if depletion_timer <= 0:
            is_stamina_depleted = false
        return
    
    # Get current gravity strength from GravityManager
    var gravity_strength = GravityManager.get_gravity_strength()
    
    # Check if gravity is altered from default
    var is_gravity_altered = current_gravity_direction != default_gravity_direction
    
    if is_gravity_altered:
        # Drain stamina (modified by gravity strength)
        var effective_drain = stamina_drain_rate * gravity_strength * delta
        current_stamina = max(0, current_stamina - effective_drain)
        
        # Check for depletion
        if current_stamina <= 0:
            _on_stamina_depleted()
    else:
        # Restore stamina
        current_stamina = min(max_stamina, current_stamina + stamina_restore_rate * delta)
    
    stamina_changed.emit(current_stamina, max_stamina)


func _on_stamina_depleted():
    is_stamina_depleted = true
    depletion_timer = stamina_depletion_delay
    
    # Force back to default gravity
    _set_gravity_direction(default_gravity_direction)
    
    stamina_depleted.emit()


func _handle_gravity_mode_input():
    # Toggle gravity mode with G key
    if Input.is_action_just_pressed("gravity_mode"):
        is_gravity_mode_active = !is_gravity_mode_active
        gravity_mode_toggled.emit(is_gravity_mode_active)
    
    # Change gravity direction while in gravity mode
    if is_gravity_mode_active:
        if Input.is_action_just_pressed("ui_up"):
            _set_gravity_direction(Vector2.UP)
        elif Input.is_action_just_pressed("ui_down"):
            _set_gravity_direction(Vector2.DOWN)
        elif Input.is_action_just_pressed("ui_left"):
            _set_gravity_direction(Vector2.LEFT)
        elif Input.is_action_just_pressed("ui_right"):
            _set_gravity_direction(Vector2.RIGHT)


func _set_gravity_direction(direction: Vector2):
    # Check if player has enough stamina (only if changing to non-default)
    if direction != default_gravity_direction and current_stamina < min_stamina_to_flip:
        return  # Not enough stamina
    
    current_gravity_direction = direction
    GravityManager.set_gravity_direction(direction)
    gravity_direction_changed.emit(direction)


func can_use_gravity_ability() -> bool:
    return current_stamina >= min_stamina_to_flip and !is_stamina_depleted


# Public API
func get_stamina_percentage() -> float:
    return (current_stamina / max_stamina) * 100.0


func is_gravity_altered() -> bool:
    return current_gravity_direction != default_gravity_direction
```

---

## 🎨 UI Requirements

### Stamina Bar Display

**Location**: Top-left corner (below health)

**Visual Design**:
```
┌─────────────────────────────┐
│ ❤❤❤ HP: 3/3               │
│ ⚡ [████████░░] 80%        │  ← Stamina bar
│   GRAVITY MODE             │  ← Only shows when active
└─────────────────────────────┘
```

**Color Coding**:
- **Green** (100-50%): Safe, plenty of stamina
- **Yellow** (49-25%): Warning, running low
- **Red** (24-0%): Critical, about to deplete
- **Gray** (Depleted): Recharging, 2s delay active

**Animations**:
- **Draining**: Bar decreases smoothly
- **Regenerating**: Bar increases smoothly with pulse effect
- **Depleted**: Flash red, then gray during delay
- **Gravity Mode**: Pulsing border or glow

---

## 🧪 Testing Scenarios

### Test Case 1: Basic Stamina Drain
1. Flip gravity to ceiling
2. Verify stamina drains at 10%/s
3. After 10 seconds, verify auto-flip to normal
4. Verify 2 second delay before regeneration
5. Verify full recharge in 6 seconds

### Test Case 2: Zone Interactions
1. Enter double gravity zone (2x strength)
2. Flip gravity
3. Verify stamina drains at 20%/s (5 second duration)
4. Enter zero-G zone
5. Verify stamina stops draining

### Test Case 3: Directional Control
1. Press G to enter gravity mode
2. Press arrow keys to change direction
3. Verify gravity changes
4. Press G to exit gravity mode
5. Verify stamina drains if non-default direction

### Test Case 4: Depletion Recovery
1. Drain stamina to 0%
2. Verify forced return to normal gravity
3. Verify 2 second delay (no regeneration)
4. After delay, verify regeneration starts
5. Verify cannot flip until stamina > 5%

---

## 🎓 Tutorial Integration (Level 1)

### Teaching Stamina Management

**Room 2A: Stamina Introduction** (New room after jump tutorial)
- Tutorial prompt: "Gravity flip drains stamina. Watch the blue bar!"
- Simple ceiling section (3 seconds to cross)
- Stamina bar appears for first time

**Room 4A: Stamina Management** (After coyote time)
- Longer ceiling section (8 seconds)
- Forces player to manage stamina
- Optional collectibles require efficient stamina use

**Room 6A: Stamina Recovery** (New room)
- Ceiling section → floor section → ceiling section
- Teaches that stamina regenerates on floor
- Tutorial prompt: "Return to normal gravity to recharge stamina"

---

## 📊 Balance Considerations

### Default Values Rationale

**10 Second Duration**:
- Long enough for meaningful platforming sections
- Short enough to require strategic planning
- Allows crossing ~2000px at normal speed

**6 Second Recharge**:
- Faster than drain (encourages returning to normal)
- Not instant (prevents spam)
- Total cycle: 10s use + 2s delay + 6s recharge = 18s

**2 Second Delay**:
- Punishes poor stamina management
- Creates tension when stamina runs out mid-section
- Not so long it feels unfair

### Tuning Recommendations

**For Easier Difficulty**:
- Increase `max_stamina` to 150
- Decrease `stamina_drain_rate` to 7.5 (13.3s duration)
- Decrease `stamina_depletion_delay` to 1.0s

**For Harder Difficulty**:
- Decrease `max_stamina` to 75
- Increase `stamina_drain_rate` to 15 (5s duration)
- Increase `stamina_depletion_delay` to 3.0s

---

## 🔮 Future Enhancements (Post-MVP)

### Stamina Upgrades
- **Max Stamina Increase**: Collectible upgrades (100 → 150 → 200)
- **Drain Reduction**: Passive ability unlock (-25% drain rate)
- **Faster Recharge**: Collectible upgrade (+50% restore rate)

### Advanced Mechanics
- **Stamina Boost Powerup**: Temporary infinite stamina (10 seconds)
- **Efficiency Bonus**: Perfect landings restore 10% stamina
- **Combo System**: Rapid flips cost less stamina (skill reward)

### Visual Enhancements
- **Stamina Trail**: Visual effect showing stamina level
- **Low Stamina Warning**: Screen pulse when < 25%
- **Depletion Effect**: Screen flash + sound when stamina hits 0

---

## ✅ Implementation Checklist

- [ ] Add stamina variables to player script
- [ ] Implement stamina drain/restore logic
- [ ] Add gravity mode toggle (G key)
- [ ] Implement 4-way directional control
- [ ] Add zone strength multiplier to drain rate
- [ ] Create stamina UI bar
- [ ] Add color coding to stamina bar
- [ ] Implement depletion delay (2s)
- [ ] Add stamina-related signals
- [ ] Create tutorial prompts for stamina
- [ ] Add "gravity_mode" input action to project settings
- [ ] Test all scenarios
- [ ] Balance stamina parameters

---

**Status**: Specification Complete  
**Ready For**: Implementation  
**Estimated Time**: 4-6 hours  
**Priority**: HIGH (Core mechanic for Level 1)
