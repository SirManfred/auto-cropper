"""
PNG Power-of-2 Cropper
A script that processes PNG images with transparency, automatically cropping them 
to the smallest power-of-2 (optional) dimensions that can contain the non-transparent content.

Copyright (C) 2024 Frederik Sjölund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Created: 2024-10-31 with help from Claude.ai
Version: 1.2.0
"""

import os
import argparse
from PIL import Image
import numpy as np
from pathlib import Path

def get_next_power_of_2(n):
    """Return the next power of 2 that is >= n"""
    n = int(n)
    return 1 if n == 0 else 2 ** (n - 1).bit_length()

def get_content_bounds(im):
    """Get the bounds of non-transparent content in RGBA image"""
    # Convert image to numpy array
    img_array = np.array(im)
    
    # Get alpha channel
    alpha = img_array[:, :, 3]
    
    # Find non-transparent pixels
    non_transparent = alpha > 0
    
    if not np.any(non_transparent):
        return None  # Image is completely transparent
    
    # Get bounds
    rows = np.any(non_transparent, axis=1)
    cols = np.any(non_transparent, axis=0)
    
    top, bottom = np.where(rows)[0][[0, -1]]
    left, right = np.where(cols)[0][[0, -1]]
    
    return left, top, right + 1, bottom + 1

def get_max_content_dimensions(png_files):
    """Calculate the maximum content dimensions across all PNG files"""
    max_width = 0
    max_height = 0
    
    for file_path in png_files:
        try:
            with Image.open(file_path) as im:
                if im.mode != 'RGBA':
                    im = im.convert('RGBA')
                
                bounds = get_content_bounds(im)
                if bounds is not None:
                    left, top, right, bottom = bounds
                    content_width = right - left
                    content_height = bottom - top
                    max_width = max(max_width, content_width)
                    max_height = max(max_height, content_height)
                    
        except Exception as e:
            print(f"Error processing {file_path} during size calculation: {e}")
    
    return max_width, max_height

def process_image(input_path, output_dir, target_width=None, target_height=None):
    """Process a single image"""
    try:
        # Open image
        with Image.open(input_path) as im:
            # Convert to RGBA if not already
            if im.mode != 'RGBA':
                im = im.convert('RGBA')
            
            # Get content bounds
            bounds = get_content_bounds(im)
            
            if bounds is None:
                print(f"Skipping {input_path} - completely transparent")
                return
            
            left, top, right, bottom = bounds
            
            # Calculate required dimensions
            content_width = right - left
            content_height = bottom - top
            
            # Use target dimensions if provided, otherwise calculate from content
            new_width = target_width if target_width else get_next_power_of_2(content_width)
            new_height = target_height if target_height else get_next_power_of_2(content_height)
            
            # Center the content in the new dimensions
            new_left = (new_width - content_width) // 2
            new_top = (new_height - content_height) // 2
            
            # Create new image with power of 2 dimensions
            new_im = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
            
            # Paste the content
            content = im.crop(bounds)
            new_im.paste(content, (new_left, new_top))
            
            # Save to output directory
            output_path = output_dir / input_path.name
            new_im.save(output_path, 'PNG')
            
            print(f"Processed {input_path.name}: {im.size} -> {new_im.size}")
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def main():
    # Set up main parser
    parser = argparse.ArgumentParser(description='Crop PNG images to (optional) power-of-2 dimensions.')
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Cropping mode')
    
    # Individual mode (default, no arguments needed)
    individual_parser = subparsers.add_parser('individual', help='Crop each image independently')
    
    # Uniform mode
    uniform_parser = subparsers.add_parser('uniform', help='Make all output images the same size based on the largest content')
    uniform_parser.add_argument('--exact', action='store_true',
                              help='Use exact dimensions instead of rounding to power of 2')
    
    args = parser.parse_args()
    
    # Get the directory containing the script
    script_dir = Path(__file__).parent
    
    # Create output directory
    output_dir = script_dir / 'cropped'
    output_dir.mkdir(exist_ok=True)
    
    # Get list of PNG files
    png_files = [f for f in script_dir.glob('*.png') if f.is_file()]
    
    # Handle different modes
    target_width = None
    target_height = None
    
    if args.mode == 'uniform' and png_files:
        max_width, max_height = get_max_content_dimensions(png_files)
        if args.exact:
            target_width = max_width
            target_height = max_height
        else:
            target_width = get_next_power_of_2(max_width)
            target_height = get_next_power_of_2(max_height)
            
        pow2text = "exact" if args.exact else "(power-of-two)"        
        print(f"Using uniform size {pow2text} for all images: {target_width}x{target_height}")
    
    # Process all PNG files
    for file_path in png_files:
        process_image(file_path, output_dir, target_width, target_height)

if __name__ == '__main__':
    main()