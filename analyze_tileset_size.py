"""
Analyze tileset to determine actual tile dimensions
"""
from PIL import Image
import numpy as np

def analyze_tileset(image_path):
    """Analyze a tileset image to find tile boundaries and dimensions"""
    img = Image.open(image_path)
    img_array = np.array(img)
    
    print(f"Image size: {img.width}x{img.height}")
    print(f"Image mode: {img.mode}")
    
    # Convert to grayscale for edge detection
    if img.mode == 'RGBA':
        # Use alpha channel or convert to grayscale
        gray = np.array(img.convert('L'))
    else:
        gray = np.array(img.convert('L'))
    
    # Find vertical lines (tile boundaries)
    # Look for consistent vertical edges
    vertical_edges = []
    for x in range(1, img.width - 1):
        # Check if this column is significantly different from neighbors
        diff = np.abs(gray[:, x].astype(int) - gray[:, x-1].astype(int))
        if np.mean(diff) > 20:  # Threshold for edge detection
            vertical_edges.append(x)
    
    # Find horizontal lines
    horizontal_edges = []
    for y in range(1, img.height - 1):
        diff = np.abs(gray[y, :].astype(int) - gray[y-1, :].astype(int))
        if np.mean(diff) > 20:
            horizontal_edges.append(y)
    
    # Calculate tile dimensions from edge spacing
    if len(vertical_edges) > 1:
        v_spacing = np.diff(vertical_edges)
        common_v_spacing = np.median(v_spacing[v_spacing > 10])
        print(f"\nVertical edges found at: {vertical_edges[:10]}...")
        print(f"Common vertical spacing (tile width): {common_v_spacing:.0f}px")
    
    if len(horizontal_edges) > 1:
        h_spacing = np.diff(horizontal_edges)
        common_h_spacing = np.median(h_spacing[h_spacing > 10])
        print(f"\nHorizontal edges found at: {horizontal_edges[:10]}...")
        print(f"Common horizontal spacing (tile height): {common_h_spacing:.0f}px")
    
    # Estimate tile size
    if len(vertical_edges) > 1 and len(horizontal_edges) > 1:
        estimated_tile_width = common_v_spacing
        estimated_tile_height = common_h_spacing
        print(f"\n=== ESTIMATED TILE SIZE: {estimated_tile_width:.0f}x{estimated_tile_height:.0f}px ===")
        print(f"Target was: 16x16px")
        print(f"Scale factor: {estimated_tile_width/16:.1f}x too large")

if __name__ == "__main__":
    analyze_tileset("assets/sprites/tilesets/tileset_level1.png")
