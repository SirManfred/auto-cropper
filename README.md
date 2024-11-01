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
2. Run the script in one of two modes:

Default mode (each image cropped to its own minimum size):
```bash
python cropper.py
```

Uniform size mode (all images cropped to the same size):
```bash
python cropper.py --uniform
```

Uniform size mode with power-of-two constraint disabled (closest possible crop):
```bash
python cropper.py --uniform --nonpow2
```

The script will:
- Create a 'cropped' subfolder in the same directory
- Process all PNG files in the directory
- Save the cropped versions in the 'cropped' folder
- Print processing information for each file

## Command Line Arguments

- `--uniform`: Make all output images the same size based on the largest content found in any image
- `--uniform --nonpow2`: Disable power-of-two constraint for closest possible crop

## Example

Default mode:
- Input1: sprite1.png (512x256 with content only using 196x111 pixels)
- Output1: cropped/sprite1.png (256x128 with centered content)
- Input2: sprite2.png (512x256 with content only using 434x115 pixels)
- Output2: cropped/sprite2.png (512x128 with centered content)

Uniform mode:
- Input1: sprite1.png (512x256 with content only using 196x111 pixels)
- Input2: sprite2.png (512x256 with content only using 434x115 pixels)
- All outputs: 512x128 (based on largest content dimensions)

Uniform Non-Pow2 mode:
- Input1: sprite1.png (434x115 with content only using 196x111 pixels)
- Input2: sprite2.png (434x115 with content only using 434x115 pixels)
- All outputs: 434x115 (based on largest content dimensions)
- 
[Rest of README remains the same...]
