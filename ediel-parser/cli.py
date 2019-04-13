import argparse
from lib import CLIParse, CLICom

def load_args(parser, module):
    module.set_args(parser)

def run(module, args):
    module.run(args)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EDI toolbox')
    subparsers = parser.add_subparsers(dest='command')
    load_args(subparsers.add_parser('com', description='communication between EDI systems'), CLICom)
    load_args(subparsers.add_parser('parse', description='parsing of edi to supported formats and generation of messages'), CLIParse)

    args = parser.parse_args()
    command = args.command

    if command == "parse":
        run(CLIParse, args)
    elif command == "com":
        run(CLICom, args)
