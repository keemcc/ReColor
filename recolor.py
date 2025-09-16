import argparse
from main_functions import palette, export, convert 

def main():
    parser = argparse.ArgumentParser(prog="recolor", description="tools for recoloring images into rgb palettes")
    subparser = parser.add_subparsers()

    palette_parser = subparser.add_parser('palette')
    palette_parser.add_argument("-f", "--filepath", help="specify file to use for creating palette")
    palette_parser.set_defaults(function=palette)
    palette_subparser = palette_parser.add_subparsers(dest="palette_command")

    export_parser = palette_subparser.add_parser("export")
    export_parser.add_argument("-n", "--name", help="specify result name")
    export_parser.add_argument("-f", "--filepath")
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