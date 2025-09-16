from PIL import Image

from helper_functions import safeOpenImage, getPalette, runColorPicker, savePalette, loadPalette, getClosestMatch
from constants import DATA_DIRECTORY

def palette(args):
    print("run")
    palette = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        palette = getPalette(paletteImage)
    else:
        runColorPicker(palette)
    print(palette)
    savePalette(palette, DATA_DIRECTORY)

def export(args):
    paletteColors = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        paletteColors = getPalette(paletteImage)
    else:
        paletteColors = loadPalette(DATA_DIRECTORY)
    exportedPalette = Image.new("RGB", (len(paletteColors), 1), (255, 255, 255))
    exportedPalettePixels = exportedPalette.load()
    for x in range(len(paletteColors)):
        exportedPalettePixels[x, 0] = paletteColors.pop()
    if args.name:
        exportedPalette.save(args.name+".png")
    else:                
        exportedPalette.save("exported_pallet.png")

def convert(args):
    paletteColors = loadPalette(DATA_DIRECTORY)
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
    else:
        originalImage.save("edited.png")