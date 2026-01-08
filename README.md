# Antigravity

A 2D platformer built in Godot 4.5 featuring gravity manipulation mechanics and a component-based architecture.

## 🎮 Game Concept

Navigate through challenging levels by flipping gravity, avoiding enemies, and collecting power-ups. Master the antigravity mechanic to reach new areas and defeat enemies in creative ways.

## ✨ Features

- **Gravity Manipulation**: Flip gravity to walk on ceilings and walls
- **Component-Based Architecture**: Modular, reusable game systems
- **3 Enemy Types**: Flyer Drone, Turret, Antigrav Orb
- **Smooth Animations**: Character and enemy sprite animations
- **6-8 Planned Levels**: Progressive difficulty and mechanics

## 🛠️ Technical Details

- **Engine**: Godot 4.5
- **Language**: GDScript
- **Architecture**: Component-based with signals
- **Platform**: Windows (primary), cross-platform compatible

## 📁 Project Structure

```
antigravity/
├── assets/           # Sprites, tilesets, audio
├── scenes/           # Player, enemies, levels
├── scripts/
│   ├── components/   # Reusable components
│   ├── autoload/     # Global managers
│   ├── player/       # Player controller
│   ├── enemies/      # Enemy AI
│   └── projectiles/  # Projectile behavior
├── resources/        # Animation data, configs
└── docs/             # Setup guides, documentation
```

## 🎯 Components

### Core Components
- **HealthComponent**: Health, damage, invincibility
- **MovementComponent**: Physics-based movement
- **DamageComponent**: Collision damage and knockback
- **CollectibleComponent**: Pickup system
- **AnimationControllerComponent**: Animation management

### AI Components
- **PatrolAI**: Waypoint-based patrol
- **ChaseAI**: Target pursuit with line-of-sight
- **TurretAI**: Stationary aiming and firing

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/JohnEhresmann3D/antigravity.git
   ```

2. **Open in Godot 4.5**
   - Launch Godot 4.5
   - Click "Import"
   - Navigate to project folder
   - Select `project.godot`

3. **Run the game**
   - Press F5 or click the Play button

## 🧪 Testing

This project follows software development best practices with automated testing using **GUT (Godot Unit Test)**.

[![Tests](https://github.com/JohnEhresmann3D/antigravity/actions/workflows/run-tests.yml/badge.svg)](https://github.com/JohnEhresmann3D/antigravity/actions/workflows/run-tests.yml)

- **78 unit tests** covering core components
- **~85% code coverage** for critical systems
- **CI/CD** via GitHub Actions (automated testing on every push)

See [Testing Guide](docs/TESTING_GUIDE.md) for details on running and writing tests.

---

## 📖 Documentation

### Design Documents
- [Updated Game Design Document](docs/GDD_UPDATED_2026-01-07.md) - Complete game design with 6-8 level structure
- [Level 1 Paper Design](docs/LEVEL_1_DESIGN.md) - Detailed design for tutorial level
- [Scope Definition](docs/SCOPE_DEFINITION.md) - Complete feature scope and timeline
- [Design Session Summary](docs/DESIGN_SESSION_SUMMARY.md) - Overview of design decisions

### Setup Guides
- [Animation Setup Guide](docs/setup/ANIMATION_SETUP_GUIDE.md)
- [Component Guide](scripts/components/COMPONENT_GUIDE.md)
- [Quick Reference](scripts/QUICK_REFERENCE.md)

## 🎨 Assets

All sprites are custom-designed with a 90s cartoon aesthetic:
- Player character: Cosmo (retro astronaut)
- Enemies: Flying drones, turrets, antigrav orbs
- Environment: Platforms, hazards, collectibles

## 🔧 Development Status

### Phase 1: Core Systems (80% Complete)
- [x] Core gravity system
- [x] Player controller with advanced features
- [x] Component library (8 components)
- [x] Enemy AI (3 types: Flyer, Turret, Antigrav Orb)
- [x] Animation system (8 states)
- [x] Projectile system
- [ ] Resource collection system
- [ ] Ability unlock progression

### Phase 2: Level Design (In Progress)
- [ ] Level 1: Awakening (Tutorial) - Paper design complete ✅
- [ ] Level 2: Gravity Training
- [ ] Level 3: The Facility
- [ ] Level 4: Antigrav Labs
- [ ] Level 5: The Depths (Mid-game boss)
- [ ] Level 6: Outer Hull
- [ ] Level 7: Core Reactor (Optional)
- [ ] Level 8: The Singularity (Optional)

### Phase 3: Systems & Polish
- [ ] UI/HUD system
- [ ] Sound effects
- [ ] Music (5-6 tracks)
- [ ] Powerup system (4 types)
- [ ] Boss battles (2-3)
- [ ] Save/load system

**Current Focus**: Level 1 implementation  
**Target**: 6-8 complete levels  
**Timeline**: 3-6 months

## 🤝 Contributing

This is a personal learning project, but feedback and suggestions are welcome!

## 📝 License

This project is for educational purposes. Assets and code are not licensed for commercial use.

## 🙏 Acknowledgments

- Built with Godot Engine
- Inspired by classic platformers
- Component architecture based on modern game design patterns

---

**Status**: Early Development  
**Version**: 0.1.0  
**Last Updated**: January 2026
