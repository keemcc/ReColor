import argparse
from functions import safeOpenImage, getPallet, runColorPicker

def pallet(args):
    print("run")
    palletColors = set()
    if args.filepath:
        palletImage = safeOpenImage(filepath=(args.filepath))
        palletColors = getPallet(palletImage)
    else:
        runColorPicker(palletColors)
    print(palletColors)


def main():
    parser = argparse.ArgumentParser(prog="recolor", description="tools for recoloring images into rgb pallets")
    subparser = parser.add_subparsers()
    parser_pallet = subparser.add_parser('pallet')
    parser_pallet.add_argument("-f", "--filepath", help="specify file to use for creating pallet")
    parser_pallet.set_defaults(function=pallet)
    args = parser.parse_args()
    args.function(args)
    # subparser = parser.add_subparsers(title="subcommands", dest="subcommand", required=False)

    

if __name__ == "__main__":
    main()