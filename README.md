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
   git clone https://github.com/YOUR_USERNAME/antigravity.git
   ```

2. **Open in Godot 4.5**
   - Launch Godot 4.5
   - Click "Import"
   - Navigate to project folder
   - Select `project.godot`

3. **Run the game**
   - Press F5 or click the Play button

## 📖 Documentation

- [Animation Setup Guide](docs/setup/ANIMATION_SETUP_GUIDE.md)
- [Component Guide](scripts/components/COMPONENT_GUIDE.md)
- [Quick Reference](docs/setup/QUICK_ANIMATION_REFERENCE.md)

## 🎨 Assets

All sprites are custom-designed with a 90s cartoon aesthetic:
- Player character: Cosmo (retro astronaut)
- Enemies: Flying drones, turrets, antigrav orbs
- Environment: Platforms, hazards, collectibles

## 🔧 Development Status

- [x] Core gravity system
- [x] Player controller
- [x] Component library
- [x] Enemy AI (3 types)
- [x] Animation system
- [ ] Level design (0/8)
- [ ] UI/HUD
- [ ] Sound effects
- [ ] Music
- [ ] Power-ups
- [ ] Boss battles

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
