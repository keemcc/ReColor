import argparse, pickle, os
from functions import safeOpenImage, getPallet, runColorPicker

def savePallet(pallet, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open((path+"/pallet.pkl"), "wb") as file:
        pickle.dump(pallet, file)

def loadPallet(path):
    with open(path, "rb") as file:
        return pickle.load(file)

def pallet(args):
    print("run")
    palletColors = set()
    if args.filepath:
        palletImage = safeOpenImage(filepath=(args.filepath))
        palletColors = getPallet(palletImage)
    else:
        runColorPicker(palletColors)
    print(palletColors)
    savePallet(palletColors, "./data")

def main():
    parser = argparse.ArgumentParser(prog="recolor", description="tools for recoloring images into rgb pallets")
    subparser = parser.add_subparsers()
    parser_pallet = subparser.add_parser('pallet')
    parser_pallet.add_argument("-f", "--filepath", help="specify file to use for creating pallet")
    parser_pallet.set_defaults(function=pallet)
    args = parser.parse_args()
    args.function(args)

if __name__ == "__main__":
    main()