# PNG Power-of-2 Cropper

A Python script that processes PNG images with transparency, automatically cropping them to the smallest power-of-2 dimensions that can contain the non-transparent content. This is particularly useful for optimizing sprite sheets, textures, and other game assets where power-of-2 dimensions are required.

## Features

- Automatically detects non-transparent pixels in PNG images
- Crops images to the smallest possible power-of-2 dimensions
- Centers the content in the output image
- Preserves transparency
- Processes multiple files in batch
- Creates a separate 'cropped' folder for output files
- Maintains original filenames

## Requirements

```bash
pip install Pillow numpy
```

## Usage

1. Place the script in the same directory as your PNG files
2. Run the script:
```bash
python cropper.py
```

The script will:
- Create a 'cropped' subfolder in the same directory
- Process all PNG files in the directory
- Save the cropped versions in the 'cropped' folder
- Print processing information for each file

## Example

Input image: `sprite.png` (512x256 with content only using 196x111 pixels)
Output: `cropped/sprite.png` (256x128 with centered content)

## Output Format

- All output images maintain their original format (PNG with transparency)
- Images are cropped to the smallest power-of-2 dimensions that can contain the content
- Content is centered in the new dimensions
- Original files are not modified

## Error Handling

- Skips completely transparent images
- Reports errors for individual files without stopping the batch process
- Creates the output directory if it doesn't exist

## Limitations

- Only processes PNG files
- Input images must have transparency (alpha channel)
- Images without an alpha channel will be converted to RGBA

## Example Power-of-2 Dimensions

Common output dimensions will be:
- 16x16
- 32x32
- 64x64
- 128x128
- 256x256
- 512x512
etc.

Width and height are calculated independently, so outputs like 256x128 or 512x64 are possible.
