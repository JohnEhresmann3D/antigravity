# Godot Glow Generation Guide

## Overview

The `generate_glow_maps.py` script analyzes sprite sheets and generates emission/glow maps for Godot's lighting system. This creates professional glow effects without manual editing.

## Quick Start

```bash
# Generate all glow types
python generate_glow_maps.py assets/sprites/enemies/antigrav_orb.png --mode all

# Specific glow type
python generate_glow_maps.py sprite.png --mode emission --intensity 3.0
```

## Generation Modes

### 1. Emission Map (`--mode emission`)
Extracts bright pixels for general glow effect.

**Parameters:**
- `--threshold` (0.0-1.0): Brightness threshold (default: 0.7)
- `--intensity` (1.0-5.0): Glow multiplier (default: 2.0)

**Use for:** Making bright areas glow naturally

### 2. Color-Specific Glow (`--mode color`)
Makes specific colors glow (cyan outlines, pink faces, etc.)

**Parameters:**
- `--color R,G,B`: Target color to make glow

**Use for:** Highlighting specific elements like outlines or eyes

### 3. Edge Glow (`--mode edge`)
Creates rim lighting/outline glow.

**Use for:** Character outlines, silhouette enhancement

### 4. HDR Emission (`--mode hdr`)
High dynamic range for intense bloom effects.

**Use for:** Magical effects, energy, intense glow

## Godot Integration

### Step 1: Import Glow Maps
1. Generated maps are saved next to original sprite
2. Godot auto-imports PNG files
3. Check import settings: Compress Mode = Lossless

### Step 2: Apply to Material
1. Select your AnimatedSprite2D/Sprite2D
2. Inspector → CanvasItem → Material → New CanvasItemMaterial
3. Enable **Emission** checkbox
4. Set **Emission Texture** to generated glow map
5. Adjust **Emission Energy** (2.0-5.0 recommended)

### Step 3: Enable Bloom (Optional)
1. Add WorldEnvironment node to scene
2. Create new Environment
3. Enable **Glow** effect
4. Adjust:
   - Intensity: 0.5-1.0
   - Strength: 0.8-1.5
   - Bloom: 0.3-0.7

## Examples

### Antigrav Orb Glow
```bash
python generate_glow_maps.py assets/sprites/enemies/antigrav_orb.png --mode all
```

**Generated files:**
- `antigrav_orb_emission.png` - General bright areas
- `antigrav_orb_glow_r0g255b255.png` - Cyan outline glow
- `antigrav_orb_glow_r255g100b150.png` - Pink face glow
- `antigrav_orb_edge_glow.png` - Rim lighting
- `antigrav_orb_hdr_emission.png` - Intense bloom

**Best for antigrav orb:** Use cyan glow or HDR emission with energy 3.0-5.0

### Custom Color Glow
```bash
# Make red elements glow
python generate_glow_maps.py sprite.png --mode color --color 255,0,0

# Make yellow elements glow
python generate_glow_maps.py sprite.png --mode color --color 255,255,0
```

## Tips & Tricks

### Combining Glow Maps
- Use different maps for different animation states
- Layer multiple emission textures in shader for complex effects

### Performance
- Emission maps don't impact performance significantly
- Bloom effect has moderate GPU cost
- Use sparingly for best performance

### Art Direction
- **Subtle glow** (energy 1.0-2.0): Ambient, magical feel
- **Medium glow** (energy 2.0-4.0): Noticeable, energetic
- **Intense glow** (energy 4.0-8.0): Dramatic, powerful

### Common Issues
**Glow too dim:** Increase Emission Energy
**Glow too bright:** Decrease intensity or use lower threshold
**Wrong colors glowing:** Adjust color tolerance or threshold
**No bloom effect:** Enable Glow in WorldEnvironment

## Advanced Usage

### Batch Processing
```bash
# Process all enemy sprites
for file in assets/sprites/enemies/*.png; do
    python generate_glow_maps.py "$file" --mode all
done
```

### Custom Parameters
```bash
# High-intensity cyan glow
python generate_glow_maps.py sprite.png \
    --mode color \
    --color 0,255,255 \
    --intensity 4.0
```

## Technical Details

- **Output format:** PNG with RGBA
- **Color space:** sRGB
- **Bit depth:** 8-bit per channel
- **Transparency:** Preserved from source
- **HDR values:** Clamped to 0-255 in PNG, use emission energy for HDR effect

## See Also

- [Animation Setup Guide](ANIMATION_SETUP_GUIDE.md)
- [Godot Emission Documentation](https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_2d_shader.html)
