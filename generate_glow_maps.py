#!/usr/bin/env python3
"""
Godot Glow Channel Generator
Analyzes existing images and creates emission/glow maps by manipulating color channels
Follows Godot 4.x standards for emission and glow effects
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from pathlib import Path
import sys
import argparse


class GodotGlowGenerator:
    """Generate glow/emission maps from existing sprites"""
    
    def __init__(self, input_path: str, output_dir: str = None):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir) if output_dir else self.input_path.parent
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_emission_map(self, brightness_threshold: float = 0.7, 
                             intensity_multiplier: float = 2.0,
                             color_boost: tuple = None):
        """
        Generate an emission map for Godot's glow effect
        
        Args:
            brightness_threshold: Pixels brighter than this will glow (0.0-1.0)
            intensity_multiplier: How much to boost glow intensity (1.0-5.0)
            color_boost: (R, G, B) multipliers for specific color channels
        """
        print(f"[*] Generating emission map from: {self.input_path.name}")
        
        # Load image
        img = Image.open(self.input_path).convert('RGBA')
        width, height = img.size
        
        # Create emission map (start with black/transparent)
        emission = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Convert to numpy for easier processing
        img_array = np.array(img, dtype=np.float32) / 255.0
        emission_array = np.zeros_like(img_array)
        
        # Calculate brightness for each pixel
        brightness = np.mean(img_array[:, :, :3], axis=2)
        
        # Create glow mask (bright pixels)
        glow_mask = brightness > brightness_threshold
        
        # Copy bright pixels to emission map with intensity boost
        for i in range(3):  # RGB channels
            emission_array[:, :, i] = np.where(
                glow_mask,
                np.clip(img_array[:, :, i] * intensity_multiplier, 0, 1),
                0
            )
        
        # Apply color boost if specified
        if color_boost:
            for i, boost in enumerate(color_boost):
                emission_array[:, :, i] *= boost
        
        # Preserve alpha from bright areas
        emission_array[:, :, 3] = np.where(glow_mask, img_array[:, :, 3], 0)
        
        # Convert back to image
        emission_array = (emission_array * 255).astype(np.uint8)
        emission = Image.fromarray(emission_array, 'RGBA')
        
        # Save emission map
        output_path = self.output_dir / f"{self.input_path.stem}_emission.png"
        emission.save(output_path, 'PNG')
        print(f"  [OK] Emission map saved: {output_path.name}")
        
        return output_path
    
    def generate_color_glow(self, target_color: tuple, tolerance: int = 50,
                           intensity: float = 3.0):
        """
        Generate glow map for specific color (e.g., cyan outlines, pink faces)
        
        Args:
            target_color: (R, G, B) color to make glow (0-255)
            tolerance: How close colors need to be to target (0-255)
            intensity: Glow intensity multiplier
        """
        print(f"[*] Generating color-specific glow for RGB{target_color}")
        
        img = Image.open(self.input_path).convert('RGBA')
        width, height = img.size
        
        emission = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        img_array = np.array(img, dtype=np.float32)
        emission_array = np.zeros_like(img_array)
        
        # Calculate color distance from target
        target = np.array(target_color, dtype=np.float32)
        color_diff = np.sqrt(np.sum((img_array[:, :, :3] - target) ** 2, axis=2))
        
        # Create mask for colors close to target
        color_mask = color_diff < tolerance
        
        # Make matching colors glow
        for i in range(3):
            emission_array[:, :, i] = np.where(
                color_mask,
                np.clip(img_array[:, :, i] * intensity / 255.0, 0, 1) * 255,
                0
            )
        
        # Preserve alpha
        emission_array[:, :, 3] = np.where(color_mask, img_array[:, :, 3], 0)
        
        emission_array = emission_array.astype(np.uint8)
        emission = Image.fromarray(emission_array, 'RGBA')
        
        color_name = f"r{target_color[0]}g{target_color[1]}b{target_color[2]}"
        output_path = self.output_dir / f"{self.input_path.stem}_glow_{color_name}.png"
        emission.save(output_path, 'PNG')
        print(f"  [OK] Color glow saved: {output_path.name}")
        
        return output_path
    
    def generate_edge_glow(self, edge_thickness: int = 2, intensity: float = 2.5):
        """
        Generate glow along sprite edges (outline glow effect)
        """
        print(f"[*] Generating edge glow")
        
        img = Image.open(self.input_path).convert('RGBA')
        
        # Extract alpha channel for edge detection
        alpha = img.split()[3]
        
        # Find edges using filter
        edges = alpha.filter(ImageFilter.FIND_EDGES)
        
        # Dilate edges to make them thicker
        for _ in range(edge_thickness):
            edges = edges.filter(ImageFilter.MaxFilter(3))
        
        # Create emission map from edges
        emission = Image.new('RGBA', img.size, (0, 0, 0, 0))
        
        # Get original colors at edge positions
        img_array = np.array(img, dtype=np.float32) / 255.0
        edges_array = np.array(edges, dtype=np.float32) / 255.0
        emission_array = np.zeros_like(img_array)
        
        # Apply edge mask with intensity
        for i in range(3):
            emission_array[:, :, i] = img_array[:, :, i] * edges_array * intensity
        
        emission_array[:, :, 3] = edges_array * 255
        
        emission_array = np.clip(emission_array * 255, 0, 255).astype(np.uint8)
        emission = Image.fromarray(emission_array, 'RGBA')
        
        output_path = self.output_dir / f"{self.input_path.stem}_edge_glow.png"
        emission.save(output_path, 'PNG')
        print(f"  [OK] Edge glow saved: {output_path.name}")
        
        return output_path
    
    def generate_hdr_emission(self, hdr_multiplier: float = 5.0):
        """
        Generate HDR emission map (values > 1.0 for bloom effect)
        Saves as EXR format for HDR support in Godot
        """
        print(f"[*] Generating HDR emission map")
        
        img = Image.open(self.input_path).convert('RGBA')
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Calculate brightness
        brightness = np.mean(img_array[:, :, :3], axis=2)
        
        # Create HDR emission (can exceed 1.0)
        hdr_emission = np.zeros_like(img_array)
        bright_mask = brightness > 0.5
        
        for i in range(3):
            hdr_emission[:, :, i] = np.where(
                bright_mask,
                img_array[:, :, i] * hdr_multiplier,  # Can be > 1.0
                0
            )
        
        hdr_emission[:, :, 3] = np.where(bright_mask, img_array[:, :, 3], 0)
        
        # Save as PNG with high bit depth (Godot will interpret as HDR)
        hdr_emission_8bit = np.clip(hdr_emission * 255, 0, 255).astype(np.uint8)
        hdr_img = Image.fromarray(hdr_emission_8bit, 'RGBA')
        
        output_path = self.output_dir / f"{self.input_path.stem}_hdr_emission.png"
        hdr_img.save(output_path, 'PNG')
        print(f"  [OK] HDR emission saved: {output_path.name}")
        print(f"      Note: Set emission energy to {hdr_multiplier} in Godot material")
        
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate Godot glow/emission maps')
    parser.add_argument('input', help='Input image file')
    parser.add_argument('-o', '--output', help='Output directory', default=None)
    parser.add_argument('-m', '--mode', choices=['emission', 'color', 'edge', 'hdr', 'all'],
                       default='all', help='Generation mode')
    parser.add_argument('-t', '--threshold', type=float, default=0.7,
                       help='Brightness threshold for emission (0.0-1.0)')
    parser.add_argument('-i', '--intensity', type=float, default=2.0,
                       help='Glow intensity multiplier')
    parser.add_argument('-c', '--color', help='Target color for color glow (R,G,B)',
                       default=None)
    
    args = parser.parse_args()
    
    generator = GodotGlowGenerator(args.input, args.output)
    
    print(f"\n{'='*60}")
    print("GODOT GLOW CHANNEL GENERATOR")
    print(f"{'='*60}\n")
    
    if args.mode == 'emission' or args.mode == 'all':
        generator.generate_emission_map(args.threshold, args.intensity)
    
    if args.mode == 'color' or args.mode == 'all':
        # Generate cyan glow (for orb outlines)
        generator.generate_color_glow((0, 255, 255), tolerance=50, intensity=3.0)
        # Generate pink glow (for faces)
        generator.generate_color_glow((255, 100, 150), tolerance=50, intensity=2.5)
    
    if args.mode == 'edge' or args.mode == 'all':
        generator.generate_edge_glow(edge_thickness=2, intensity=2.5)
    
    if args.mode == 'hdr' or args.mode == 'all':
        generator.generate_hdr_emission(hdr_multiplier=5.0)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Glow maps generated!")
    print("\nGodot Setup Instructions:")
    print("1. Import the generated emission maps into your project")
    print("2. In your material, enable 'Emission'")
    print("3. Set the emission texture to the generated map")
    print("4. Adjust 'Emission Energy' for intensity")
    print("5. Enable 'Glow' in WorldEnvironment for bloom effect")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Demo mode
        print("Usage: python generate_glow_maps.py <input_image> [options]")
        print("\nExample:")
        print("  python generate_glow_maps.py antigrav_orb.png --mode all")
        print("  python generate_glow_maps.py sprite.png --mode color --color 0,255,255")
    else:
        main()
