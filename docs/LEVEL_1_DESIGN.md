# Level 1: "Awakening" - Paper Design

**Level ID**: LVL-001-AWAKENING  
**Created**: January 7, 2026  
**Designer**: Atlas AI  
**Status**: Paper Design (Pre-Implementation)

---

## 🎯 Level Overview

### Purpose
Level 1 serves as the **tutorial and introduction** to Antigravity. Players learn basic movement, jumping, and platforming before unlocking the gravity flip ability at the end.

### Theme
**"Space Station Awakening"** - Bright, clean space station interior with a retro-futuristic aesthetic. The player character (Cosmo) wakes up in a training facility and must reach the gravity core chamber.

### Tone
- **Visual**: Bright, upbeat, colorful (Mario-inspired)
- **Mood**: Curious, exploratory, safe
- **Satirical Edge**: Corporate training facility aesthetic with humorous signage

### Target Completion Time
- **First-time**: 5-8 minutes
- **Speedrun**: 2-3 minutes

---

## 📐 Level Layout

### Overall Structure
```
[START] → [Movement Tutorial] → [Jump Training] → [Platforming Challenge] → [Gravity Core Chamber] → [BOSS/UNLOCK]
```

### Detailed Room Breakdown

#### **Room 1: Awakening Chamber** (Start)
```
┌─────────────────────────────────────┐
│  [Spawn Point]                      │
│       ↓                             │
│    ┌─────┐                          │
│    │Cosmo│                          │
│    └─────┘                          │
│  ═══════════════════════════════════│
│                                     │
│  "Press → to move right"            │
└─────────────────────────────────────┘
```

**Purpose**: Player spawns, learns left/right movement  
**Mechanics**: Movement only  
**Collectibles**: None  
**Enemies**: None  
**Length**: 200px horizontal  
**Tutorial Prompt**: "Use A/D or Arrow Keys to move"

---

#### **Room 2: Jump Introduction**
```
┌─────────────────────────────────────┐
│                    ┌────┐           │
│                    │ ?  │ ← Collectible
│              ┌─────┴────┴─────┐     │
│              │                │     │
│              │                │     │
│    ═══════   │                │     │
│              └────────────────┘     │
│                                     │
│  "Press SPACE to jump"              │
└─────────────────────────────────────┘
```

**Purpose**: Teach jumping mechanic  
**Mechanics**: Jump to reach platform  
**Collectibles**: 1 gravity core (optional, floating above platform)  
**Enemies**: None  
**Gap Size**: 80px (requires jump)  
**Tutorial Prompt**: "Press SPACE, W, or UP to jump"

---

#### **Room 3: Variable Jump Height**
```
┌─────────────────────────────────────┐
│         ┌──┐    ┌────┐    ┌──────┐ │
│         │  │    │    │    │      │ │
│         │  │    │    │    │      │ │
│  ═══    └──┘    └────┘    └──────┘ │
│   ↑      ↑        ↑          ↑     │
│  Low   Medium   High      Max      │
│                                     │
│  "Hold jump for higher jumps"      │
└─────────────────────────────────────┘
```

**Purpose**: Teach variable jump height  
**Mechanics**: Short tap vs. held jump  
**Collectibles**: 3 gravity cores (one on each platform)  
**Enemies**: None  
**Platform Heights**: 60px, 100px, 140px, 180px  
**Tutorial Prompt**: "Hold jump longer to jump higher"

---

#### **Room 4: Coyote Time Demonstration**
```
┌─────────────────────────────────────┐
│                                     │
│  ═════════════                      │
│               ╲                     │
│                ╲ (slope)            │
│                 ╲                   │
│                  ═════════════      │
│                                     │
│  "You can jump shortly after       │
│   leaving a platform"               │
└─────────────────────────────────────┘
```

**Purpose**: Demonstrate coyote time (0.1s grace period)  
**Mechanics**: Walk off platform, jump mid-air  
**Collectibles**: 1 gravity core at gap  
**Enemies**: None  
**Gap Size**: 100px (requires coyote time jump)  
**Tutorial Prompt**: "Jump just after walking off edges"

---

#### **Room 5: Platforming Challenge**
```
┌─────────────────────────────────────────────────┐
│                                                 │
│     ┌──┐      ┌──┐      ┌──┐      ┌──┐        │
│     │  │      │  │      │  │      │  │        │
│  ═══└──┘   ═══└──┘   ═══└──┘   ═══└──┘  ═══   │
│                                                 │
│  [Multiple small platforms]                    │
│                                                 │
│  "Combine movement and jumping"                │
└─────────────────────────────────────────────────┘
```

**Purpose**: Test basic platforming skills  
**Mechanics**: Series of jumps, no new mechanics  
**Collectibles**: 5 gravity cores (one per platform)  
**Enemies**: None  
**Platform Spacing**: 70-90px gaps  
**Difficulty**: Easy (forgiving gaps)  
**Tutorial Prompt**: None (player should know basics)

---

#### **Room 6: Moving Platforms** (Optional Challenge)
```
┌─────────────────────────────────────┐
│                                     │
│         ┌────┐                      │
│         │ ←→ │ (moving platform)    │
│  ═══    └────┘              ═══     │
│                                     │
│  [Platform moves horizontally]     │
│                                     │
│  "Time your jump!"                 │
└─────────────────────────────────────┘
```

**Purpose**: Introduce moving platforms (optional)  
**Mechanics**: Timed jumping  
**Collectibles**: 2 gravity cores (on moving platform)  
**Enemies**: None  
**Platform Speed**: 50px/s  
**Movement Range**: 150px horizontal  
**Tutorial Prompt**: "Wait for the platform"

---

#### **Room 7: Vertical Climb**
```
┌─────────────────────────────────────┐
│                              ═══    │
│                         ┌──┐        │
│                    ┌──┐ │  │        │
│               ┌──┐ │  │ │  │        │
│          ┌──┐ │  │ │  │ │  │        │
│  ═══     │  │ │  │ │  │ │  │        │
│          └──┘ └──┘ └──┘ └──┘        │
│                                     │
│  "Climb to the Gravity Core"       │
└─────────────────────────────────────┘
```

**Purpose**: Vertical platforming challenge  
**Mechanics**: Multiple jumps upward  
**Collectibles**: 4 gravity cores (one per platform)  
**Enemies**: None  
**Platform Spacing**: 80px vertical gaps  
**Height**: 400px total climb  
**Tutorial Prompt**: "Reach the top"

---

#### **Room 8: Gravity Core Chamber** (End)
```
┌─────────────────────────────────────┐
│                                     │
│          ╔═══════════╗              │
│          ║  GRAVITY  ║              │
│          ║   CORE    ║ ← Glowing    │
│          ║  ◉◉◉◉◉   ║              │
│          ╚═══════════╝              │
│  ═══════════════════════════════    │
│                                     │
│  "Approach the Gravity Core"       │
└─────────────────────────────────────┘
```

**Purpose**: Level completion, unlock gravity flip  
**Mechanics**: Cutscene trigger  
**Collectibles**: Gravity Flip ability (permanent unlock)  
**Enemies**: None  
**Event**: Player touches core → ability unlocked → level complete  
**Tutorial Prompt**: "You've unlocked GRAVITY FLIP! Press E or Q to flip gravity."

---

## 🎓 Tutorial Progression

### Mechanics Introduction Order
1. **Horizontal Movement** (Room 1)
2. **Jumping** (Room 2)
3. **Variable Jump Height** (Room 3)
4. **Coyote Time** (Room 4)
5. **Platforming Combination** (Room 5)
6. **Moving Platforms** (Room 6) - Optional
7. **Vertical Climbing** (Room 7)
8. **Ability Unlock** (Room 8)

### Tutorial Prompt System
- **Type**: On-screen text prompts
- **Trigger**: Player enters room for first time
- **Duration**: Stays until player performs action
- **Style**: Simple white text, bottom-center of screen
- **Dismissal**: Automatic after action performed

---

## 🎨 Visual Design

### Color Palette
- **Walls**: Light gray/white (#E0E0E0)
- **Platforms**: Blue-gray (#5C7CBA)
- **Background**: Dark blue space (#1A1A3E)
- **Accents**: Bright cyan (#00FFFF) for interactive elements
- **Collectibles**: Glowing purple/blue (#8B5CF6)

### Lighting
- **Ambient**: Bright, even lighting
- **Accents**: Glowing panels on walls
- **Gravity Core**: Pulsing blue/purple glow

### Props & Details
- **Signage**: Humorous corporate training signs
  - "GRAVITY TRAINING FACILITY - SECTOR 7"
  - "PLEASE DO NOT RUN IN ZERO-G ZONES"
  - "DAYS SINCE LAST GRAVITY INCIDENT: 0"
- **Background Elements**: Windows showing space, stars
- **Decorative**: Computer terminals, pipes, vents

---

## 📊 Collectibles & Secrets

### Gravity Cores (Resource)
- **Total Available**: 20 cores
- **Required**: 0 (tutorial level)
- **Locations**: 
  - Room 2: 1 core
  - Room 3: 3 cores
  - Room 4: 1 core
  - Room 5: 5 cores
  - Room 6: 2 cores
  - Room 7: 4 cores
  - Room 8: 4 cores (bonus for exploration)

### Hidden Areas
**Secret Room 1**: Behind breakable wall in Room 5
- **Contents**: 5 bonus gravity cores
- **Hint**: Cracked wall texture
- **Access**: Jump into wall (breakable)

**Secret Room 2**: Above Room 7
- **Contents**: Speed boost powerup (preview for later)
- **Hint**: Faint glow above ceiling
- **Access**: Requires precise jump from highest platform

### Completion Rewards
- **100% Collectibles**: Unlock "Perfectionist" achievement
- **Speedrun < 3 min**: Unlock "Speed Demon" achievement
- **No Deaths**: Unlock "Flawless" achievement

---

## ⚙️ Technical Implementation Notes

### Tileset Requirements
- **Platform Tiles**: 32x32px
- **Wall Tiles**: 32x32px
- **Background Tiles**: 64x64px (parallax)
- **Special**: Breakable wall variant

### Scene Structure
```
Level1 (Node2D)
├── Background (ParallaxBackground)
│   ├── SpaceLayer (ParallaxLayer)
│   └── StarsLayer (ParallaxLayer)
├── TileMap (TileMap)
│   ├── Platforms Layer
│   ├── Walls Layer
│   └── Background Layer
├── Collectibles (Node2D)
│   └── GravityCore (x20 instances)
├── MovingPlatforms (Node2D)
│   └── MovingPlatform1 (AnimatableBody2D)
├── TutorialPrompts (CanvasLayer)
│   └── PromptLabel (Label)
├── Player (CharacterBody2D)
└── GravityCore (Area2D) - End trigger
```

### Camera Setup
- **Type**: Camera2D (follows player)
- **Smoothing**: Enabled (5.0)
- **Limits**: Set to level bounds
- **Zoom**: 1.5x (closer view for tutorial)

### Checkpoints
- **Room 1**: Start (auto-checkpoint)
- **Room 5**: After platforming challenge
- **Room 7**: Before vertical climb

---

## 🎮 Playtesting Goals

### What to Test
1. **Tutorial Clarity**: Do players understand controls?
2. **Difficulty Curve**: Is progression smooth?
3. **Pacing**: Does it feel too slow or too fast?
4. **Collectible Placement**: Are cores visible and fair?
5. **Secret Discovery**: Do players find hidden areas?

### Success Metrics
- **Completion Rate**: 95%+ (it's a tutorial)
- **Average Time**: 5-8 minutes
- **Deaths**: < 3 average
- **Collectibles Found**: 60%+ on first playthrough
- **Tutorial Prompts Read**: 80%+ (tracked via analytics)

### Iteration Points
- If players struggle with Room 3: Add more platforms
- If Room 5 is too easy: Increase gap sizes
- If secrets are never found: Add more obvious hints
- If completion time > 10 min: Reduce level length

---

## 🔊 Audio Design (Future)

### Music
- **Track**: "Station Awakening" (upbeat, electronic)
- **Tempo**: 120 BPM
- **Mood**: Curious, exploratory
- **Layers**: Add layers as player progresses

### Sound Effects
- **Movement**: Footstep sounds (soft, robotic)
- **Jump**: Whoosh sound
- **Landing**: Thud (varies by surface)
- **Collectible**: Chime sound (satisfying)
- **Gravity Core**: Deep hum, energy pulse
- **Tutorial Prompt**: Subtle notification beep

### Ambient
- **Background**: Gentle station hum
- **Spatial**: Distant machinery sounds
- **Gravity Core Chamber**: Intensifying energy sound

---

## 📝 Dialogue / Text (Optional)

### Opening Text
```
"Welcome to Gravity Training Facility - Sector 7.
Please proceed to the Gravity Core Chamber for ability calibration."
```

### Gravity Core Unlock
```
"GRAVITY CORE SYNCHRONIZED
New Ability Unlocked: GRAVITY FLIP
Press E or Q to flip gravity 180°"
```

### Completion Text
```
"Training Complete!
Gravity Cores Collected: [X]/20
Time: [MM:SS]
Proceed to Level 2: Gravity Training"
```

---

## 🎯 Design Goals Summary

### Primary Goals
✅ Teach basic movement and jumping  
✅ Introduce collectibles (gravity cores)  
✅ Demonstrate variable jump height  
✅ Show coyote time mechanic  
✅ Unlock gravity flip ability  

### Secondary Goals
✅ Establish visual style and tone  
✅ Introduce tutorial prompt system  
✅ Create sense of progression  
✅ Reward exploration (secrets)  
✅ Set up narrative context (minimal)  

### Stretch Goals
- Add moving platforms (Room 6)
- Include 2 secret areas
- Implement speedrun timer
- Add achievement system

---

## 🚀 Next Steps for Implementation

### Phase 1: Asset Creation
1. Create tileset (platforms, walls, background)
2. Design gravity core sprite (animated)
3. Create tutorial prompt UI
4. Design gravity core chamber centerpiece

### Phase 2: Level Building
1. Set up Level1 scene in Godot
2. Build TileMap layout based on paper design
3. Place collectibles (20 gravity cores)
4. Add moving platform in Room 6

### Phase 3: Scripting
1. Create tutorial prompt system
2. Implement gravity core collection
3. Add end-of-level trigger (gravity core chamber)
4. Set up camera limits and smoothing

### Phase 4: Polish
1. Add background parallax layers
2. Implement lighting effects
3. Add decorative props and signage
4. Playtest and iterate

### Phase 5: Testing
1. Internal playtest (5+ runs)
2. Adjust difficulty based on feedback
3. Verify all collectibles are reachable
4. Test speedrun route

---

## 📐 Level Dimensions

### Overall Size
- **Width**: ~2000px (62.5 tiles @ 32px)
- **Height**: ~1200px (37.5 tiles @ 32px)
- **Aspect Ratio**: 16:10 (optimized for 1920x1200)

### Room Sizes (Approximate)
- Room 1: 200x200px
- Room 2: 300x250px
- Room 3: 400x300px
- Room 4: 300x250px
- Room 5: 500x300px
- Room 6: 300x250px (optional)
- Room 7: 300x500px (vertical)
- Room 8: 400x300px

---

## 🎨 Mockup / Sketch

```
LEVEL 1 - FULL LAYOUT (Side View)

                                    [8: GRAVITY CORE]
                                    ┌─────────────┐
                                    │   ╔═══╗     │
                                    │   ║ ◉ ║     │
                                    │   ╚═══╝     │
                                    └─────────────┘
                                           ↑
                    [7: VERTICAL CLIMB]    │
                    ┌──┐                   │
               ┌──┐ │  │                   │
          ┌──┐ │  │ │  │                   │
     ┌──┐ │  │ │  │ │  │                   │
     │  │ │  │ │  │ │  │                   │
     └──┘ └──┘ └──┘ └──┘                   │
                                           │
[6: MOVING]     ┌────┐                     │
  ┌────┐  ←→    │    │                     │
  │    │        └────┘                     │
  └────┘                                   │
                                           │
[5: PLATFORMING CHALLENGE]                 │
┌──┐   ┌──┐   ┌──┐   ┌──┐                 │
│  │   │  │   │  │   │  │                 │
└──┘   └──┘   └──┘   └──┘                 │
                                           │
[4: COYOTE TIME]                           │
═════════════                              │
             ╲                             │
              ╲                            │
               ═════════════               │
                                           │
[3: VARIABLE JUMP]                         │
┌──┐    ┌────┐    ┌──────┐                │
│  │    │    │    │      │                │
└──┘    └────┘    └──────┘                │
                                           │
[2: JUMP INTRO]                            │
         ┌────────────┐                    │
         │            │                    │
═══      │            │                    │
         └────────────┘                    │
                                           │
[1: START]                                 │
┌─────────────────────────────────────────┘
│  [SPAWN]
│    ↓
│  ┌───┐
│  │ C │
│  └───┘
└═══════════════════════════════════════
```

---

**Status**: Paper Design Complete  
**Ready For**: Asset Creation & Implementation  
**Estimated Build Time**: 4-6 hours  
**Next Document**: Level 2 Design (after Level 1 implementation)
