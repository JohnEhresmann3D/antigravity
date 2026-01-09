"""
Generate a proper 16x16 pixel-art tileset for Level 1
"""
from PIL import Image, ImageDraw
import numpy as np

# Colors from design doc
LIGHT_GRAY = (224, 224, 224)  # #E0E0E0 - walls
BLUE_GRAY = (92, 124, 186)     # #5C7CBA - platforms  
CYAN = (0, 255, 255)           # #00FFFF - accents
DARK_BLUE = (60, 80, 120)      # Darker shade for outlines
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def create_tileset():
    """Create a 1024x1024 tileset with proper 16x16 tiles"""
    # Create canvas
    img = Image.new('RGB', (1024, 1024), WHITE)
    draw = ImageDraw.Draw(img)
    
    tile_size = 16
    spacing = 2  # Space between tiles for visibility
    
    # Helper function to draw a tile at grid position
    def draw_tile_at(grid_x, grid_y, tile_func):
        x = grid_x * (tile_size + spacing)
        y = grid_y * (tile_size + spacing)
        tile_func(x, y)
    
    # === WALL/FLOOR TILES (3x3 grid) ===
    def draw_corner_tl(x, y):
        # Top-left corner
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+2, y+2, x+4, y+4], fill=CYAN)  # Corner accent
        draw.line([x+1, y+tile_size-2, x+tile_size-2, y+tile_size-2], fill=DARK_BLUE, width=1)
        draw.line([x+tile_size-2, y+1, x+tile_size-2, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    def draw_top_edge(x, y):
        # Top edge
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.line([x+4, y+2, x+12, y+2], fill=CYAN, width=1)
        draw.line([x+1, y+tile_size-2, x+tile_size-2, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    def draw_corner_tr(x, y):
        # Top-right corner
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+tile_size-5, y+2, x+tile_size-3, y+4], fill=CYAN)
        draw.line([x+1, y+tile_size-2, x+tile_size-2, y+tile_size-2], fill=DARK_BLUE, width=1)
        draw.line([x+1, y+1, x+1, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    def draw_left_edge(x, y):
        # Left edge
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.line([x+2, y+4, x+2, y+12], fill=CYAN, width=1)
        draw.line([x+tile_size-2, y+1, x+tile_size-2, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    def draw_center(x, y):
        # Center fill
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.point([x+4, y+4], fill=CYAN)
        draw.point([x+11, y+11], fill=CYAN)
    
    def draw_right_edge(x, y):
        # Right edge
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.line([x+tile_size-3, y+4, x+tile_size-3, y+12], fill=CYAN, width=1)
        draw.line([x+1, y+1, x+1, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    def draw_corner_bl(x, y):
        # Bottom-left corner
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+2, y+tile_size-5, x+4, y+tile_size-3], fill=CYAN)
        draw.line([x+1, y+1, x+tile_size-2, y+1], fill=DARK_BLUE, width=1)
        draw.line([x+tile_size-2, y+1, x+tile_size-2, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    def draw_bottom_edge(x, y):
        # Bottom edge
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.line([x+4, y+tile_size-3, x+12, y+tile_size-3], fill=CYAN, width=1)
        draw.line([x+1, y+1, x+tile_size-2, y+1], fill=DARK_BLUE, width=1)
    
    def draw_corner_br(x, y):
        # Bottom-right corner
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+tile_size-5, y+tile_size-5, x+tile_size-3, y+tile_size-3], fill=CYAN)
        draw.line([x+1, y+1, x+tile_size-2, y+1], fill=DARK_BLUE, width=1)
        draw.line([x+1, y+1, x+1, y+tile_size-2], fill=DARK_BLUE, width=1)
    
    # Draw 3x3 wall grid
    draw_tile_at(0, 0, draw_corner_tl)
    draw_tile_at(1, 0, draw_top_edge)
    draw_tile_at(2, 0, draw_corner_tr)
    draw_tile_at(0, 1, draw_left_edge)
    draw_tile_at(1, 1, draw_center)
    draw_tile_at(2, 1, draw_right_edge)
    draw_tile_at(0, 2, draw_corner_bl)
    draw_tile_at(1, 2, draw_bottom_edge)
    draw_tile_at(2, 2, draw_corner_br)
    
    # === PLATFORM TILES ===
    def draw_platform_left(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=BLUE_GRAY, outline=BLACK)
        draw.rectangle([x+2, y+6, x+tile_size-2, y+8], fill=CYAN)
        draw.arc([x-4, y+2, x+4, y+tile_size-3], 90, 180, fill=DARK_BLUE, width=1)
    
    def draw_platform_mid(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=BLUE_GRAY, outline=BLACK)
        draw.rectangle([x+2, y+6, x+tile_size-3, y+8], fill=CYAN)
    
    def draw_platform_right(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=BLUE_GRAY, outline=BLACK)
        draw.rectangle([x+2, y+6, x+tile_size-3, y+8], fill=CYAN)
        draw.arc([x+tile_size-5, y+2, x+tile_size+3, y+tile_size-3], 0, 90, fill=DARK_BLUE, width=1)
    
    draw_tile_at(0, 4, draw_platform_left)
    draw_tile_at(1, 4, draw_platform_mid)
    draw_tile_at(2, 4, draw_platform_right)
    
    # === SLOPE TILES ===
    def draw_slope_up(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        points = [(x, y+tile_size-1), (x+tile_size-1, y), (x+tile_size-1, y+tile_size-1)]
        draw.polygon(points, fill=LIGHT_GRAY, outline=BLACK)
        draw.line([x+4, y+tile_size-5, x+4, y+tile_size-7], fill=CYAN, width=1)
    
    def draw_slope_down(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        points = [(x, y), (x, y+tile_size-1), (x+tile_size-1, y+tile_size-1)]
        draw.polygon(points, fill=LIGHT_GRAY, outline=BLACK)
        draw.line([x+tile_size-5, y+tile_size-5, x+tile_size-5, y+tile_size-7], fill=CYAN, width=1)
    
    draw_tile_at(0, 6, draw_slope_up)
    draw_tile_at(1, 6, draw_slope_down)
    
    # === PROPS ===
    def draw_warning_sign(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+2, y+2, x+tile_size-3, y+tile_size-3], fill=(255, 165, 0), outline=BLACK)
        draw.text((x+6, y+4), "!", fill=BLACK)
    
    def draw_arrow_right(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        points = [(x+3, y+5), (x+10, y+8), (x+3, y+11)]
        draw.polygon(points, fill=CYAN, outline=BLACK)
    
    def draw_vent(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=DARK_BLUE, outline=BLACK)
        for i in range(3, 13, 2):
            draw.line([x+3, y+i, x+12, y+i], fill=(100, 100, 100), width=1)
    
    draw_tile_at(0, 8, draw_warning_sign)
    draw_tile_at(1, 8, draw_arrow_right)
    draw_tile_at(2, 8, draw_vent)
    
    # === ADDITIONAL WALL VARIATIONS ===
    def draw_wall_panel_1(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+3, y+3, x+12, y+12], fill=(200, 200, 200), outline=DARK_BLUE)
        draw.point([x+8, y+8], fill=CYAN)
    
    def draw_wall_panel_2(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        for i in range(2, 14, 4):
            draw.line([x+i, y+2, x+i, y+13], fill=DARK_BLUE, width=1)
    
    def draw_wall_tech(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+4, y+4, x+11, y+11], fill=BLUE_GRAY)
        draw.line([x+5, y+7, x+10, y+7], fill=CYAN, width=1)
    
    draw_tile_at(4, 0, draw_wall_panel_1)
    draw_tile_at(5, 0, draw_wall_panel_2)
    draw_tile_at(6, 0, draw_wall_tech)
    
    # === MORE PLATFORM VARIATIONS ===
    def draw_thin_platform(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+1, y+7, x+tile_size-2, y+9], fill=BLUE_GRAY, outline=BLACK)
        draw.line([x+3, y+8, x+12, y+8], fill=CYAN, width=1)
    
    def draw_grate_platform(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+1, y+6, x+tile_size-2, y+10], fill=DARK_BLUE, outline=BLACK)
        for i in range(3, 13, 2):
            draw.line([x+i, y+7, x+i, y+9], fill=(100, 100, 100), width=1)
    
    def draw_holographic_platform(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+2, y+6, x+tile_size-3, y+10], fill=(0, 200, 255, 128), outline=CYAN)
        for i in range(4, 12, 2):
            draw.point([x+i, y+8], fill=CYAN)
    
    draw_tile_at(4, 4, draw_thin_platform)
    draw_tile_at(5, 4, draw_grate_platform)
    draw_tile_at(6, 4, draw_holographic_platform)
    
    # === HAZARDS ===
    def draw_spike_up(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        # Draw 3 spikes
        for i in range(0, 3):
            sx = x + 2 + i * 5
            points = [(sx, y+tile_size-2), (sx+2, y+tile_size-8), (sx+4, y+tile_size-2)]
            draw.polygon(points, fill=(200, 50, 50), outline=BLACK)
    
    def draw_laser_emitter(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+4, y+4, x+11, y+11], fill=DARK_BLUE, outline=BLACK)
        draw.ellipse([x+6, y+6, x+9, y+9], fill=(255, 0, 0))
    
    def draw_electric_hazard(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+3, y+3, x+12, y+12], fill=(255, 255, 0), outline=BLACK)
        # Lightning bolt
        points = [(x+8, y+5), (x+6, y+8), (x+9, y+8), (x+7, y+11)]
        draw.line(points, fill=BLACK, width=1)
    
    draw_tile_at(0, 10, draw_spike_up)
    draw_tile_at(1, 10, draw_laser_emitter)
    draw_tile_at(2, 10, draw_electric_hazard)
    
    # === COLLECTIBLES ===
    def draw_coin(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.ellipse([x+4, y+4, x+11, y+11], fill=(255, 215, 0), outline=BLACK)
        draw.ellipse([x+6, y+6, x+9, y+9], fill=(255, 255, 150))
    
    def draw_energy_orb(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.ellipse([x+4, y+4, x+11, y+11], fill=(139, 92, 246), outline=CYAN)
        draw.ellipse([x+6, y+6, x+9, y+9], fill=(200, 150, 255))
    
    def draw_health_pickup(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        # Red cross
        draw.rectangle([x+7, y+4, x+8, y+11], fill=(255, 50, 50), outline=BLACK)
        draw.rectangle([x+4, y+7, x+11, y+8], fill=(255, 50, 50), outline=BLACK)
    
    draw_tile_at(4, 10, draw_coin)
    draw_tile_at(5, 10, draw_energy_orb)
    draw_tile_at(6, 10, draw_health_pickup)
    
    # === DOORS & WINDOWS ===
    def draw_door_closed(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=BLUE_GRAY, outline=BLACK)
        draw.rectangle([x+3, y+2, x+12, y+13], fill=(80, 100, 140), outline=DARK_BLUE)
        draw.rectangle([x+10, y+7, x+11, y+9], fill=CYAN)  # Handle
    
    def draw_door_open(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+2, y+2, x+5, y+13], fill=BLUE_GRAY, outline=DARK_BLUE)
        draw.rectangle([x+6, y+3, x+13, y+12], fill=BLACK)  # Opening
    
    def draw_window(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        draw.rectangle([x+3, y+3, x+12, y+12], fill=(20, 20, 60), outline=DARK_BLUE)
        # Stars
        draw.point([x+5, y+5], fill=WHITE)
        draw.point([x+9, y+7], fill=WHITE)
        draw.point([x+7, y+10], fill=WHITE)
    
    draw_tile_at(0, 12, draw_door_closed)
    draw_tile_at(1, 12, draw_door_open)
    draw_tile_at(2, 12, draw_window)
    
    # === DECORATIVE ELEMENTS ===
    def draw_computer_terminal(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+3, y+4, x+12, y+12], fill=BLUE_GRAY, outline=BLACK)
        draw.rectangle([x+4, y+5, x+11, y+10], fill=(0, 100, 150))
        draw.line([x+5, y+7, x+10, y+7], fill=CYAN, width=1)
    
    def draw_pipe_horizontal(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x, y+6, x+tile_size-1, y+9], fill=(120, 120, 120), outline=BLACK)
        draw.line([x+4, y+7, x+11, y+7], fill=(80, 80, 80), width=1)
    
    def draw_pipe_vertical(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+6, y, x+9, y+tile_size-1], fill=(120, 120, 120), outline=BLACK)
        draw.line([x+7, y+4, x+7, y+11], fill=(80, 80, 80), width=1)
    
    def draw_crate(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+2, y+2, x+13, y+13], fill=(139, 90, 43), outline=BLACK)
        draw.line([x+3, y+3, x+12, y+12], fill=(100, 60, 20), width=1)
        draw.line([x+12, y+3, x+3, y+12], fill=(100, 60, 20), width=1)
    
    def draw_barrel(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.ellipse([x+4, y+2, x+11, y+4], fill=(100, 100, 100), outline=BLACK)
        draw.rectangle([x+4, y+3, x+11, y+12], fill=(120, 120, 120), outline=BLACK)
        draw.ellipse([x+4, y+11, x+11, y+13], fill=(80, 80, 80), outline=BLACK)
    
    draw_tile_at(4, 12, draw_computer_terminal)
    draw_tile_at(5, 12, draw_pipe_horizontal)
    draw_tile_at(6, 12, draw_pipe_vertical)
    draw_tile_at(0, 14, draw_crate)
    draw_tile_at(1, 14, draw_barrel)
    
    # === SIGNAGE ===
    def draw_arrow_up(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        points = [(x+5, y+10), (x+8, y+3), (x+11, y+10)]
        draw.polygon(points, fill=CYAN, outline=BLACK)
    
    def draw_arrow_down(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        points = [(x+5, y+5), (x+8, y+12), (x+11, y+5)]
        draw.polygon(points, fill=CYAN, outline=BLACK)
    
    def draw_arrow_left(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        points = [(x+10, y+5), (x+3, y+8), (x+10, y+11)]
        draw.polygon(points, fill=CYAN, outline=BLACK)
    
    def draw_checkpoint_flag(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.line([x+3, y+2, x+3, y+13], fill=BLACK, width=2)
        draw.polygon([(x+4, y+2), (x+12, y+5), (x+4, y+8)], fill=(0, 255, 0), outline=BLACK)
    
    draw_tile_at(2, 14, draw_arrow_up)
    draw_tile_at(3, 14, draw_arrow_down)
    draw_tile_at(4, 14, draw_arrow_left)
    draw_tile_at(5, 14, draw_checkpoint_flag)
    
    # === BREAKABLE BLOCKS ===
    def draw_breakable_block(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=(180, 140, 100), outline=BLACK)
        # Cracks
        draw.line([x+2, y+4, x+6, y+8], fill=(100, 80, 60), width=1)
        draw.line([x+9, y+3, x+12, y+7], fill=(100, 80, 60), width=1)
        draw.rectangle([x+5, y+5, x+6, y+6], fill=(255, 215, 0))  # Hint of treasure
    
    def draw_cracked_wall(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=LIGHT_GRAY, outline=BLACK)
        # Multiple cracks
        draw.line([x+3, y+2, x+5, y+6], fill=DARK_BLUE, width=1)
        draw.line([x+8, y+4, x+11, y+8], fill=DARK_BLUE, width=1)
        draw.line([x+4, y+9, x+7, y+12], fill=DARK_BLUE, width=1)
    
    draw_tile_at(0, 16, draw_breakable_block)
    draw_tile_at(1, 16, draw_cracked_wall)
    
    # === SPECIAL TILES ===
    def draw_teleporter(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.ellipse([x+3, y+3, x+12, y+12], fill=(100, 50, 200), outline=CYAN)
        # Simpler swirl effect using points
        draw.ellipse([x+6, y+6, x+9, y+9], fill=CYAN)
        draw.point([x+5, y+8], fill=WHITE)
        draw.point([x+10, y+8], fill=WHITE)
    
    def draw_gravity_zone(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        # Gravity field indicator
        for i in range(3, 13, 3):
            draw.line([x+i, y+3, x+i, y+12], fill=(200, 100, 255), width=1)
        draw.polygon([(x+7, y+4), (x+9, y+4), (x+8, y+2)], fill=CYAN)
        draw.polygon([(x+7, y+11), (x+9, y+11), (x+8, y+13)], fill=CYAN)
    
    def draw_checkpoint_pad(x, y):
        draw.rectangle([x, y, x+tile_size-1, y+tile_size-1], fill=WHITE, outline=None)
        draw.rectangle([x+2, y+10, x+13, y+13], fill=(0, 200, 100), outline=BLACK)
        draw.ellipse([x+6, y+11, x+9, y+12], fill=(0, 255, 150))
    
    draw_tile_at(2, 16, draw_teleporter)
    draw_tile_at(3, 16, draw_gravity_zone)
    draw_tile_at(4, 16, draw_checkpoint_pad)
    
    return img

if __name__ == "__main__":
    print("Generating 16x16 pixel-art tileset...")
    tileset = create_tileset()
    output_path = "assets/sprites/tilesets/tileset_level1.png"
    tileset.save(output_path)
    print(f"Saved to: {output_path}")
    print(f"Image size: {tileset.width}x{tileset.height}")
    print("Tile size: 16x16px")
    print("Tiles per row: ~56 (with 2px spacing)")
