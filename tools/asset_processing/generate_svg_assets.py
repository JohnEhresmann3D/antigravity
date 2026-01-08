import os

# Configuration from Brief
COLORS = {
    "platform_fill": "#5C7CBA",  # Blue-Gray
    "platform_stroke": "#87CEEB", # Lighter Blue stroke
    "background": "#1A1A3E",     # Dark Space Blue
    "star": "#FFFFFF",           # White stars
    "star_accent": "#00FFFF"     # Cyan accent stars
}

TILE_SIZE = 32

def create_tileset_svg():
    # A simple 3x3 autotile-compatible structure (simplified for prototype)
    # Just a clean rounded rect block for now
    svg = f'''<svg width="{TILE_SIZE}" height="{TILE_SIZE}" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="{TILE_SIZE-2}" height="{TILE_SIZE-2}" rx="8" ry="8" 
        fill="{COLORS['platform_fill']}" stroke="{COLORS['platform_stroke']}" stroke-width="2"/>
  <!-- "Tech" detail -->
  <circle cx="{TILE_SIZE/2}" cy="{TILE_SIZE/2}" r="4" fill="{COLORS['platform_stroke']}" opacity="0.5"/>
</svg>'''
    
    path = "assets/sprites/tilesets/proto_tileset.svg"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    print(f"Created {path}")

def create_background_svg():
    width = 512
    height = 512
    
    # Generate some random stars
    import random
    stars = ""
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.choice([1, 1.5, 2])
        color = COLORS['star'] if random.random() > 0.3 else COLORS['star_accent']
        opacity = random.uniform(0.5, 1.0)
        stars += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{opacity}"/>\n'

    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{COLORS['background']}"/>
  {stars}
</svg>'''

    path = "assets/sprites/backgrounds/proto_space_bg.svg"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    print(f"Created {path}")

def main():
    create_tileset_svg()
    create_background_svg()

if __name__ == "__main__":
    main()
