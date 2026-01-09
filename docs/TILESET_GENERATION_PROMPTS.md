# Tileset Generation Prompts

**Created**: January 8, 2026  
**Purpose**: Document AI prompts for generating pixel art tilesets  
**AI Model**: Gemini (Imagen 3)

---

## Overview

This document contains the expert-level prompts used to generate high-quality pixel art tilesets for Antigravity. These prompts are crafted based on:
- Level 1 Design Document (LEVEL_1_DESIGN.md)
- Visual Design Document (VDD-2026-01-06-001.txt)
- Game Design Document (GDD_UPDATED_2026-01-07.md)

---

## Design Guidelines Summary

### Art Style
- **Inspiration**: SNES-style pixel art, 90s cartoon aesthetic (Super Mario Bros)
- **Perspective**: Flat orthographic side-on view (NO isometric, NO 3D)
- **Tone**: Bright, upbeat, colorful with satirical edge
- **Quality**: Sharp pixels, bold black outlines, no anti-aliasing, no blur

### Color Palette (Level 1 - Space Station)
- **Walls**: Light gray/white (#E0E0E0)
- **Platforms**: Blue-gray (#5C7CBA)
- **Accents**: Bright cyan (#00FFFF)
- **Shading**: Dark blue (#3C5078)
- **Background**: Dark blue space (#1A1A3E)
- **Collectibles**: Glowing purple/blue (#8B5CF6)

### Technical Requirements
- **Tile Size**: 16x16 pixels (SNES-style)
- **Spacing**: 2px between tiles in tileset
- **Format**: Organized grid layout
- **Style**: Limited color palette, clean geometric shapes

---

## Prompt 1: Structure Tiles (Walls & Platforms)

### Generated File
`assets/sprites/tilesets/tileset_level1_structure_ai.png`

### Prompt
```
16x16 pixel art tileset for retro platformer game, SNES style, flat orthographic side-on view, space station interior theme. Includes: 3x3 wall tile grid (top-left corner, top edge, top-right corner, left edge, center fill, right edge, bottom-left corner, bottom edge, bottom-right corner) in light gray/white (#E0E0E0) with bright cyan (#00FFFF) accent details and dark blue (#3C5078) shading. Blue-gray (#5C7CBA) platform tiles (left end, middle, right end) with cyan highlights. Clean geometric shapes, bold black outlines, bright upbeat colorful 90s cartoon aesthetic inspired by Super Mario Bros. Sharp pixels, no anti-aliasing, no blur, no gradients. Organized grid layout with 2px spacing between tiles. High quality pixel art, game asset style, retro game graphics, limited color palette.
```

### Contents
- 3x3 wall tile grid (9 tiles for modular wall construction)
- Platform tiles (left end, middle, right end)
- Light gray walls with cyan accents
- Blue-gray platforms with cyan highlights

---

## Prompt 2: Decorative Props

### Generated File
`assets/sprites/tilesets/tileset_level1_props_ai.png`

### Prompt
```
16x16 pixel art decorative props tileset for retro space station platformer, SNES style, flat orthographic side-on view. Includes: computer terminal with glowing cyan screen, horizontal metal pipe in gray, vertical metal pipe, wooden crate with X pattern, metal barrel, warning sign in orange with exclamation mark, cyan directional arrow, air vent grate in dark blue, door closed (blue-gray with cyan handle), door open showing dark interior, window showing space with white stars on dark blue background. Bright upbeat colorful 90s cartoon aesthetic, clean geometric shapes, bold black outlines, sharp pixels, no anti-aliasing, limited color palette (#E0E0E0 gray, #5C7CBA blue-gray, #00FFFF cyan, #1A1A3E dark blue). Organized grid layout, game asset style, high quality pixel art.
```

### Contents
- Computer terminal (cyan screen)
- Pipes (horizontal and vertical)
- Crate and barrel
- Warning sign (orange with !)
- Directional arrow (cyan)
- Air vent grate
- Doors (closed and open)
- Window (space view with stars)

---

## Prompt 3: Collectibles & Hazards

### Generated File
`assets/sprites/tilesets/tileset_level1_items_ai.png`

### Prompt
```
16x16 pixel art collectibles and hazards tileset for retro platformer, SNES style, flat orthographic side-on view. Includes: glowing purple-blue gravity core orb (#8B5CF6) with bright center, golden coin with shine, red health pickup with cross symbol, upward-pointing red spikes (3 spikes per tile), laser emitter (dark blue box with red glowing center), electric hazard (yellow with black lightning bolt), checkpoint flag (green flag on black pole), teleporter (purple swirl with cyan glow), gravity zone indicator (purple vertical lines with cyan arrows). Bright upbeat colorful 90s cartoon aesthetic, bold black outlines, sharp pixels, no anti-aliasing, no blur, limited color palette. Organized grid layout with 2px spacing, game asset style, high quality pixel art, retro game graphics.
```

### Contents
- Gravity core orb (purple-blue glow) - PRIMARY COLLECTIBLE
- Golden coin
- Health pickup (red cross)
- Spikes (red, upward-pointing)
- Laser emitter (red glow)
- Electric hazard (yellow lightning)
- Checkpoint flag (green)
- Teleporter (purple swirl)
- Gravity zone indicator (purple lines, cyan arrows)

---

## Prompt Engineering Best Practices

Based on research, these prompts follow proven techniques:

### 1. Structure
**Base Style** + **Main Subject** + **Specific Details** + **Quality Modifiers** + **Color Palette**

### 2. Key Elements
- ✅ Specify resolution: "16x16 pixel art"
- ✅ Define style: "SNES style", "retro game graphics"
- ✅ Set perspective: "flat orthographic side-on view"
- ✅ List specific items: Detailed enumeration of all tiles
- ✅ Color codes: Hex values for accuracy
- ✅ Quality terms: "sharp pixels", "no anti-aliasing", "bold black outlines"
- ✅ Aesthetic: "90s cartoon aesthetic", "Super Mario Bros inspired"
- ✅ Technical specs: "organized grid layout", "2px spacing"

### 3. Negative Constraints
- "no anti-aliasing" - prevents smooth edges
- "no blur" - maintains pixel sharpness
- "no gradients" - keeps retro aesthetic
- "flat orthographic side-on view" - prevents isometric/3D perspective

---

## Usage in Godot

### Importing Tilesets
1. Copy generated PNG files to `assets/sprites/tilesets/`
2. Godot will auto-generate `.import` files
3. In Godot, create TileSet resource
4. Configure tile size: 16x16 pixels
5. Set spacing: 2 pixels
6. Define collision shapes for platforms and walls

### Recommended TileMap Layers
- **Layer 0**: Background decorations
- **Layer 1**: Walls (collision enabled)
- **Layer 2**: Platforms (collision enabled)
- **Layer 3**: Foreground props

---

## Regeneration Guide

### When to Regenerate
- Need different tile variations
- Color palette adjustments
- Style refinements
- Additional tile types

### How to Modify Prompts
1. **Change colors**: Update hex codes in prompt
2. **Add tiles**: Append to "Includes:" section
3. **Adjust style**: Modify aesthetic descriptors
4. **Change perspective**: Update view description (keep "flat orthographic side-on")

### Example Modifications

**For darker zones** (Level 3+):
```
Replace: "light gray/white (#E0E0E0)"
With: "dark gray (#2C2C2C)"

Replace: "bright upbeat colorful 90s cartoon aesthetic"
With: "moody atmospheric dark aesthetic inspired by Hollow Knight"
```

**For additional platform types**:
```
Add to "Includes:" section:
"thin platform (one-way passthrough), grate platform (semi-transparent), 
holographic platform (glowing cyan edges)"
```

---

## AI Model Comparison

### Why Gemini (Imagen 3)?
- ✅ Built-in image generation
- ✅ Excellent prompt understanding
- ✅ Consistent style adherence
- ✅ No additional setup required

### Alternatives
- **Stable Diffusion**: More customization with LoRAs, requires local setup
- **DALL-E 3**: Similar quality, good prompt precision
- **PixelLab.ai**: Specialized for game tilesets, subscription required
- **Retro Diffusion**: Aseprite plugin, pixel-perfect output

---

## Version History

### v1.0 (January 8, 2026)
- Initial tileset generation for Level 1
- Three tilesets: Structure, Props, Items
- SNES-style 16x16 pixel art
- Bright upbeat space station theme

---

## Next Steps

### Future Tilesets Needed
- [ ] Level 2: Training facility (alternating bright/dark)
- [ ] Level 3: Industrial complex (moody atmosphere)
- [ ] Level 4: Antigrav labs (zero-g aesthetic)
- [ ] Background parallax layers (64x64 tiles)
- [ ] Animated tiles (gravity core glow, hazards)

### Potential Improvements
- [ ] Generate slope tiles (45° angles)
- [ ] Create breakable wall variants
- [ ] Add more platform variations
- [ ] Design moving platform sprites
- [ ] Create transition tiles between zones

---

**Status**: Active  
**Last Updated**: January 8, 2026  
**Maintained By**: Atlas AI
