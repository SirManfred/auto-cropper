"""
PNG Power-of-2 Cropper
A script that processes PNG images with transparency, automatically cropping them 
to the smallest power-of-2 dimensions that can contain the non-transparent content.

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
Version: 1.0.0
"""

import os
from PIL import Image
import numpy as np
from pathlib import Path

def get_next_power_of_2(n):
    """Return the next power of 2 that is >= n"""
    # Convert numpy.int64 to Python int
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

def process_image(input_path, output_dir):
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
            
            # Get next power of 2 dimensions that can contain the content
            new_width = get_next_power_of_2(content_width)
            new_height = get_next_power_of_2(content_height)
            
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
    # Get the directory containing the script
    script_dir = Path(__file__).parent
    
    # Create output directory
    output_dir = script_dir / 'cropped'
    output_dir.mkdir(exist_ok=True)
    
    # Process all PNG files in the script's directory
    for file_path in script_dir.glob('*.png'):
        if file_path.is_file():
            process_image(file_path, output_dir)

if __name__ == '__main__':
    main()