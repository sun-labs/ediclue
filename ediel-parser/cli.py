import argparse
from lib.cli import parse, com

def load_args(module, parser):
    module.set_args(parser)

def run(module, args):
    module.run(args)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='EDI toolbox')
    subparsers = parser.add_subparsers(dest='command')
    load_args(parse, subparsers)
    load_args(com, subparsers)

    args = parser.parse_args()
    command = args.command

    if command == "parse":
        run(parse, args)
    elif command == "com":
        run(com, args)
