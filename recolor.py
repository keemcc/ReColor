import argparse, pickle, os
from functions import safeOpenImage, getPalette, runColorPicker, getClosestMatch
from PIL import Image

DATA_PATH = "./data"

def savePalette(palette, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open((path+"/palette.pkl"), "wb") as file:
        pickle.dump(palette, file)

def loadPalette(path):
    with open(path+"/palette.pkl", "rb") as file:
        return pickle.load(file)

def palette(args):
    print("run")
    palette = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        palette = getPalette(paletteImage)
    else:
        runColorPicker(palette)
    print(palette)
    savePalette(palette, "./data")

def export(args):
    paletteColors = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        paletteColors = getPalette(paletteImage)
    else:
        paletteColors = loadPalette(DATA_PATH)
    exportedPalette = Image.new("RGB", (len(paletteColors), 1), (255, 255, 255))
    exportedPalettePixels = exportedPalette.load()
    for x in range(len(paletteColors)):
        exportedPalettePixels[x, 0] = paletteColors.pop()
    exportedPalette.save("exported_pallet.png")

def convert(args):
    paletteColors = loadPalette(DATA_PATH)
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

    


def main():
    parser = argparse.ArgumentParser(prog="recolor", description="tools for recoloring images into rgb palettes")
    subparser = parser.add_subparsers()

    palette_parser = subparser.add_parser('palette')
    palette_parser.add_argument("-f", "--filepath", help="specify file to use for creating palette")
    palette_parser.set_defaults(function=palette)
    palette_subparser = palette_parser.add_subparsers(dest="palette_command")

    export_parser = palette_subparser.add_parser("export")
    export_parser.add_argument("-n", "--name", help="specify result name")
    export_parser.set_defaults(function=export)

    convert_parser = subparser.add_parser("convert")
    convert_parser.add_argument("filepath")
    convert_parser.add_argument("-n", "--name")
    convert_parser.set_defaults(function=convert)

    args = parser.parse_args()
    if hasattr(args, "function"):
        args.function(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()