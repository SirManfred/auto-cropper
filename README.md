# PNG Power-of-2 Cropper

A Python script that processes PNG images with transparency, automatically cropping them to the smallest power-of-2 (optional) dimensions that can contain the non-transparent content. This is particularly useful for optimizing sprite sheets, textures, and other game assets where power-of-2 dimensions are required.

## Features

- Automatically detects non-transparent pixels in PNG images
- Crops images to the smallest possible power-of-2 dimensions
- Power of 2 constraint can be disabled for maximum crop
- Centers the content in the output image
- Optional uniform size mode where all images use the same dimensions
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
2. Run the script in one of these modes:

Default mode (each image cropped to power-of-2 size):
```bash
python cropper.py
```

Default mode with exact sizing (closest possible crop for each image):
```bash
python cropper.py --exact
```

Uniform mode (all images cropped to the same power-of-2 size):
```bash
python cropper.py uniform
```

Uniform mode with exact sizing (closest possible crop):
```bash
python cropper.py uniform --exact
```

The script will:
- Create a 'cropped' subfolder in the same directory
- Process all PNG files in the directory
- Save the cropped versions in the 'cropped' folder
- Print processing information for each file

## Command Line Arguments

- Default (no argument): Crop each image independently to its own minimum power-of-2 size
- `--exact`: Crop each image to its exact content size without rounding to power-of-two
- `uniform`: Make all output images the same size based on the largest content found in any image
- `uniform --exact`: Make all output images the same exact size based on largest content

## Example

Default mode:
- Input1: sprite1.png (512x256 with content only using 196x111 pixels)
- Output1: cropped/sprite1.png (256x128 with centered content)
- Input2: sprite2.png (512x256 with content only using 434x115 pixels)
- Output2: cropped/sprite2.png (512x128 with centered content)

Individual exact mode:
- Input1: sprite1.png (512x256 with content only using 196x111 pixels)
- Output1: cropped/sprite1.png (196x111 with centered content)
- Input2: sprite2.png (512x256 with content only using 434x115 pixels)
- Output2: cropped/sprite2.png (434x115 with centered content)

Uniform mode:
- Input1: sprite1.png (512x256 with content only using 196x111 pixels)
- Input2: sprite2.png (512x256 with content only using 434x115 pixels)
- All outputs: 512x128 (based on largest content dimensions)

Uniform exact mode:
- Input1: sprite1.png (434x115 with content only using 196x111 pixels)
- Input2: sprite2.png (434x115 with content only using 434x115 pixels)
- All outputs: 434x115 (based on largest content dimensions)

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
