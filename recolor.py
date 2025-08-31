import argparse, pickle, os
from functions import safeOpenImage, getPalette, runColorPicker
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

    args = parser.parse_args()
    if hasattr(args, "function"):
        args.function(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()