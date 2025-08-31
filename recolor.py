import argparse, pickle, os
from functions import safeOpenImage, getPalette, runColorPicker

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

def save_palette(args):
    paletteColors = set()
    if args.filepath:
        paletteImage = safeOpenImage(filepath=(args.filepath))
        paletteColors = getPalette(paletteImage)
    else:
        paletteColors = loadPalette(DATA_PATH)
    

def main():
    parser = argparse.ArgumentParser(prog="recolor", description="tools for recoloring images into rgb palettes")
    subparser = parser.add_subparsers()
    parser_palette = subparser.add_parser('palette')
    parser_palette.add_argument("-f", "--filepath", help="specify file to use for creating palette")
    parser_palette.set_defaults(function=palette)
    parser_savepalette = subparser.add_parser("save-palette")
    parser_savepalette.add_argument("-f", "--filepath", help="specify file to create and save palette from")
    args = parser.parse_args()
    args.function(args)

if __name__ == "__main__":
    main()