import sys
from PIL import Image
from helper_functions import safeOpenImage, getPalette, runColorPicker, savePalette, loadPalette, getClosestMatch
from constants import DATA_DIRECTORY

# Runs the palette command, defining the current palette
#   Creates color palette based on image colors if filepath is specified or by color picker if not
#   Resulting palette is saved to the data directory
def palette(args):
    palette = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        palette = getPalette(paletteImage)
    else:
        runColorPicker(palette)
    savePalette(palette, DATA_DIRECTORY)
    print("Palette saved successfully")

# Exports the current palette into a png file
#   If a filepath is specified it will create a palette based on the passed image and save that palette
#   If a filepath isn't specified it will save the currently defined palette saved in the data directory
#   If a name is specified the palette image will be saved with that name, if not it will be titled "exported_palette.png"
def export(args):
    paletteColors = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        paletteColors = getPalette(paletteImage)
    else:
        try:
            paletteColors = loadPalette(DATA_DIRECTORY)
        except FileNotFoundError:
            print("ERROR: Pallet not set!")
            print("Please set a palette using the palette subcommand before exporting a palette.")
            sys.exit()
    exportedPalette = Image.new("RGB", (len(paletteColors), 1), (255, 255, 255))
    exportedPalettePixels = exportedPalette.load()
    for x in range(len(paletteColors)):
        exportedPalettePixels[x, 0] = paletteColors.pop()
    if args.name:
        exportedPalette.save(args.name+".png")
        print(f"Palette exported to {args.name}.png")
    else:                
        exportedPalette.save("exported_palette.png")
        print("Palette exported to exported_palette.png")

# Converts an image into the currently defined color palette
#   If a name is given, the result will be titled with that name, otherwise it will be titled "recolored_image.png"
def convert(args):
    try:
        paletteColors = loadPalette(DATA_DIRECTORY)
    except FileNotFoundError:
        print("ERROR: Pallet not set!")
        print("Please set a palette using the palette subcommand before converting an image.")
        sys.exit()
    originalImage = safeOpenImage(args.filepath)
    originalPixels = originalImage.load()
    width, height = originalImage.size
    colorMap = dict()
    for x in range(width):
        for y in range(height):
            originalColor = originalPixels[x, y]
            if originalColor not in colorMap:
                colorMap[originalColor] = getClosestMatch(originalColor, paletteColors)
            originalPixels[x, y] = colorMap[originalColor]
    if args.name:
        originalImage.save(args.name+".png")
        print(f"Edited image saved to {args.name}.png")
    else:
        originalImage.save("recolored_image.png")
        print("Edited image saved to recolored_image.png")