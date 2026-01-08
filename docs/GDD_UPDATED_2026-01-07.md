# Antigravity - Game Design Document (Updated)

**Document ID**: GDD-2026-01-07-UPDATED  
**Created**: January 7, 2026  
**Status**: Active  
**Previous Version**: GDD-2026-01-06-001

---

## 📋 Document Purpose

This GDD updates the original design document to reflect **implemented systems** and defines the scope for the full **6-8 level game**. This bridges the gap between the initial prototype design and the current implementation state.

---

## 🎮 Game Overview

**Title**: Antigravity  
**Genre**: 2D Platformer / Metroidvania Hybrid  
**Platforms**: PC (Primary for development), Mobile (Future)  
**Scope**: 6-8 Complete Levels  
**Engine**: Godot 4.5 (Forward Plus)

### Concept

A 2D platformer where players master gravity manipulation to navigate challenging levels. Inspired by classic platformers with modern mechanics including variable jump height, coyote time, and a component-based enemy AI system.

---

## ✅ Implemented Systems (Current State)

### Core Player Mechanics
- ✅ **Movement System**: Acceleration-based movement with run mode
- ✅ **Advanced Jump**: Variable height, coyote time (0.1s), jump buffering (0.1s)
- ✅ **Gravity Flip**: 180° gravity rotation (unlockable ability)
- ✅ **Animation State Machine**: 8 states (idle, walk, run, jump, fall, land, gravity_flip, damage)

### Gravity System
- ✅ **GravityManager** (Singleton): Global gravity control with signals
- ✅ **GravityZone**: Area-based custom gravity (normal, zero-g, custom direction)
- ✅ **Directional Support**: Any gravity direction via Vector2
- ✅ **Strength Modulation**: Adjustable gravity strength per zone

### Component Architecture
**Core Components**:
- ✅ `HealthComponent`: Health, damage, invincibility, death
- ✅ `MovementComponent`: Physics-based movement with friction
- ✅ `DamageComponent`: Collision damage with knockback
- ✅ `CollectibleComponent`: Pickup system with auto-collect
- ✅ `AnimationControllerComponent`: Animation management with sprite flipping

**AI Components**:
- ✅ `PatrolAI`: Waypoint-based patrol with looping
- ✅ `ChaseAI`: Target pursuit with line-of-sight and detection range
- ✅ `TurretAI`: Stationary aiming and firing with rotation

### Enemy Types (3 Implemented)
1. **Flyer Drone**: Patrols and chases player
2. **Turret**: Stationary enemy that aims and fires projectiles
3. **Antigrav Orb**: Floats and performs gravity flips to disorient player

### Projectile System
- ✅ Generic projectile with speed, damage, lifetime
- ✅ Gravity-affected projectiles (optional)
- ✅ Collision detection and cleanup

---

## 🎯 Updated Core Pillars

1. **Gravity Mastery** - Learn and master gravity manipulation
2. **Component-Based Design** - Modular, reusable game systems
3. **Progressive Challenge** - Difficulty increases across 6-8 levels
4. **Exploration & Secrets** - Hidden areas and collectibles

---

## 🗺️ Game Scope: 6-8 Level Structure

### Level Progression

#### **Tutorial Zone (Level 1)**
- **Theme**: Bright, upbeat space station interior
- **Mechanics Introduced**: Basic movement, jumping, collectibles
- **Enemies**: None (tutorial)
- **Gravity**: Standard downward gravity only
- **Goal**: Reach the gravity core chamber
- **Unlock**: Gravity Flip ability

#### **Gravity Training (Level 2)**
- **Theme**: Training facility with alternating bright/dark zones
- **Mechanics**: Gravity flip mastery, ceiling walking
- **Enemies**: Flyer Drones (patrol only, no chase)
- **Gravity**: Standard + flip zones
- **Goal**: Complete obstacle course
- **Unlock**: Access to main facility

#### **The Facility (Level 3)**
- **Theme**: Industrial complex, moody atmosphere
- **Mechanics**: Gravity zones, enemy combat
- **Enemies**: Flyer Drones (chase enabled), Turrets (stationary)
- **Gravity**: Mixed zones, some zero-g sections
- **Challenge**: Navigate through enemy-filled corridors
- **Collectible**: First resource cache

#### **Antigrav Labs (Level 4)**
- **Theme**: Experimental laboratory, satirical bright aesthetic
- **Mechanics**: Zero-gravity navigation, antigrav orb enemies
- **Enemies**: Antigrav Orbs, Turrets
- **Gravity**: Primarily zero-g with gravity flip puzzles
- **Challenge**: Precision platforming in zero-g
- **Unlock**: Directional gravity control (4-way)

#### **The Depths (Level 5)**
- **Theme**: Dark, atmospheric lower levels
- **Mechanics**: 4-way gravity control, complex puzzles
- **Enemies**: All three types, increased difficulty
- **Gravity**: Multi-directional gravity zones
- **Challenge**: Gravity-based puzzles and combat
- **Boss**: Mid-game boss fight

#### **Outer Hull (Level 6)**
- **Theme**: Exterior of station, space backdrop
- **Mechanics**: Advanced gravity manipulation
- **Enemies**: Aggressive enemy formations
- **Gravity**: Variable strength zones, hazards
- **Challenge**: Timed platforming sections
- **Collectible**: Major resource cache

#### **Core Reactor (Level 7)** *(Optional)*
- **Theme**: Bright, energetic, dangerous
- **Mechanics**: All mechanics combined
- **Enemies**: Elite variants of all enemy types
- **Gravity**: Chaotic gravity shifts
- **Challenge**: Gauntlet-style challenge
- **Boss**: Pre-final boss

#### **The Singularity (Level 8)** *(Optional)*
- **Theme**: Abstract, surreal final area
- **Mechanics**: Master-level gravity control
- **Enemies**: Final boss only
- **Gravity**: Boss controls gravity dynamically
- **Challenge**: Final boss fight
- **Ending**: Game completion

### Scope Decision
- **Minimum Viable**: 6 levels (1-6)
- **Full Experience**: 8 levels (1-8)
- **Decision Point**: After Level 6 completion, assess scope

---

## 🔧 Mechanics Deep Dive

### Gravity System (Implemented)

**Current Implementation**:
```gdscript
# Gravity Flip (unlockable)
GravityManager.flip_gravity()  # 180° rotation

# Cardinal Directions
GravityManager.set_cardinal_direction("up")  # up, down, left, right

# Custom Direction
GravityManager.set_gravity_direction(Vector2.LEFT)

# Strength Adjustment
GravityManager.set_gravity_strength(0.5)  # 0.0 to 2.0
```

**Progression**:
- **Level 1**: Standard gravity only
- **Level 2-3**: Gravity flip unlocked
- **Level 4+**: Directional gravity control (4-way)

### Resource System (To Implement)

**Resource Type**: "Gravity Cores"
- **Visual**: Glowing blue/purple energy orbs
- **Acquisition**: 
  - Breakable containers (70%)
  - Enemy drops (30%)
- **Usage**: Powers gravity abilities (flip costs 1 core)
- **Max Capacity**: 10 cores (upgradable to 20)

**Implementation Note**: Use existing `CollectibleComponent` with type "gravity_core"

### Ability System

**Permanent Abilities** (Unlockable):
1. **Gravity Flip** (Level 1 end) - Toggle ceiling/floor
2. **Directional Control** (Level 4 end) - 4-way gravity
3. **Gravity Dash** (Level 5 end) - Quick dash in gravity direction
4. **Gravity Shield** (Level 7 end) - Temporary invincibility

**Temporary Powerups** (To Implement):
- **Speed Boost**: 1.5x movement speed for 10s
- **Double Jump**: Extra jump for 15s
- **Invincibility**: No damage for 8s
- **Magnet**: Auto-collect nearby resources for 12s

---

## 🎨 Visual Design (Updated)

### Art Style
- **Inspiration**: 90s cartoon aesthetic (current sprites)
- **Player**: Retro astronaut character "Cosmo"
- **Enemies**: Cartoon-style robots and drones
- **Environment**: Mix of industrial and space station themes

### Zone Tones
- **Bright Zones** (Levels 1, 2, 4, 7): Colorful, saturated, satirical
- **Dark Zones** (Levels 3, 5, 8): Moody, atmospheric, mysterious
- **Transition**: Gradual tone shifts between zones

### UI/HUD Requirements
- **Health Bar**: Top-left, heart-based or numeric
- **Resource Counter**: Top-right, gravity core count
- **Ability Icons**: Bottom-center, show unlocked abilities
- **Minimap**: Bottom-left (optional, for larger levels)

---

## 📊 Progression & Difficulty

### Difficulty Curve
```
Level 1: ████░░░░░░ (40%) - Tutorial
Level 2: █████░░░░░ (50%) - Learning
Level 3: ██████░░░░ (60%) - Competent
Level 4: ███████░░░ (70%) - Skilled
Level 5: ████████░░ (80%) - Expert
Level 6: █████████░ (90%) - Master
Level 7: ██████████ (95%) - Elite
Level 8: ██████████ (100%) - Perfect
```

### Gating Mechanics
- **Level 2**: Requires gravity flip
- **Level 4**: Requires gravity flip mastery
- **Level 5**: Requires directional control
- **Level 7**: Requires all abilities + collectibles

---

## 🎯 Prototype vs. Full Game Scope

### Current Prototype Scope (Completed)
- ✅ Core movement and gravity systems
- ✅ Component architecture
- ✅ 3 enemy types with AI
- ✅ Player controller with advanced features
- ✅ Animation system

### Next Phase: Level 1 Implementation
- [ ] Design Level 1 layout (paper design)
- [ ] Create tileset for space station interior
- [ ] Implement tutorial UI prompts
- [ ] Build Level 1 in Godot
- [ ] Playtest and iterate

### Full Game Scope (6-8 Levels)
- [ ] 6-8 complete levels
- [ ] UI/HUD system
- [ ] Resource collection system
- [ ] Ability unlock progression
- [ ] 2-3 boss fights
- [ ] Sound effects and music
- [ ] Save/load system
- [ ] Level selection menu

---

## 🚧 Open Questions (Updated)

### Resolved
- ✅ Gravity flip mechanic (implemented)
- ✅ Component architecture (implemented)
- ✅ Enemy AI patterns (implemented)
- ✅ Player movement feel (implemented)

### Still Open
- ❓ **Mobile controls**: Virtual joystick or gesture-based?
- ❓ **Resource name**: "Gravity Cores" or alternative?
- ❓ **Boss designs**: Specific mechanics and patterns?
- ❓ **Level themes**: Detailed environmental design?
- ❓ **Collectibles**: What hidden items beyond resources?
- ❓ **Narrative**: Any story elements or pure gameplay?

---

## 📝 Next Steps

### Immediate (This Session)
1. ✅ Update GDD with implemented systems
2. 🔄 Define 6-8 level scope
3. 🔄 Create Level 1 paper design

### Short-term (Next 1-2 Sessions)
1. Create tileset for Level 1
2. Implement UI/HUD system
3. Build Level 1 in Godot
4. Add tutorial prompts

### Medium-term (Next 5-10 Sessions)
1. Implement resource collection system
2. Create Levels 2-3
3. Add boss fight for Level 5
4. Implement ability unlock system

### Long-term (Full Game)
1. Complete all 6-8 levels
2. Add sound and music
3. Implement save system
4. Polish and balance
5. Mobile port (if desired)

---

## 🎮 Design Philosophy

1. **Mechanics First**: Prove the gravity mechanics are fun
2. **Modular Systems**: Everything is reusable and testable
3. **Progressive Learning**: Introduce one mechanic at a time
4. **Player Mastery**: Reward skill and exploration
5. **Quality Over Quantity**: 6 great levels > 12 mediocre ones

---

**Status**: Ready for Level 1 Design  
**Next Document**: Level 1 Paper Design
