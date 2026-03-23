# ReColor

A command-line tool for recoloring images into RGB color palettes. Define a palette from an existing image or by picking colors directly from your screen, then convert any image so every pixel is remapped to its closest palette color.

## How It Works

1. **Define a palette** — extract colors from a reference image, or use the interactive color picker to sample colors from anywhere on your screen.
2. **Convert an image** — each pixel in the target image is replaced with the closest matching color from the palette, using 3D Euclidean distance in RGB space.
3. **Export the palette** — optionally save your current palette as a PNG for reference.

Palettes are persisted between sessions in a local `data/` directory.

## Installation

**Requirements:** Python 3 and pip.

### Windows (recommended)

Use the included batch script — it automatically creates a virtual environment and installs all dependencies on first run:

```bat
recolor.bat <command> [options]
```

### Manual setup

```bash
pip install -r requirements.txt
python recolor.py <command> [options]
```

## Usage

### Set a palette from an image

Extracts every unique color from the given image and saves it as the current palette.

```bash
python recolor.py palette -f path/to/palette_image.png
```

### Set a palette with the interactive color picker

Launches a color picker that lets you sample colors directly from your screen.

- Press **`p`** while hovering over a color to add it to the palette.
- Press **`Esc`** when finished.

```bash
python recolor.py palette
```

### Convert an image

Recolors an image using the currently saved palette. Each pixel is mapped to the nearest palette color.

```bash
python recolor.py convert path/to/image.png
python recolor.py convert path/to/image.png -n output_name
```

Output defaults to `recolored_image.png` if `-n` is not specified.

### Export the current palette as a PNG

Saves the active palette as a 1-pixel-tall PNG where each pixel is one palette color.

```bash
python recolor.py palette export
python recolor.py palette export -n my_palette
python recolor.py palette export -f path/to/image.png -n my_palette
```

- `-f` — derive the palette from a specific image instead of the saved one.
- `-n` — name for the output file (defaults to `exported_palette.png`).

## Dependencies

| Package     | Version  |
|-------------|----------|
| Pillow      | 11.3.0   |
| PyAutoGUI   | 0.9.54   |
| keyboard    | 0.13.5   |
| MouseInfo   | 0.1.3    |
| PyGetWindow | 0.0.9    |
| PyMsgBox    | 1.0.9    |
| pypercip    | 1.9.0    |
| PyRect      | 0.2.0    |
| PyScreeze   | 1.0.1    |
| pytweening  | 1.2.0    |
