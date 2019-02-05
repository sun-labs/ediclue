import argparse
import sys
from lib.EdielParser import EdielParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse data from EDIEL via UTILTS and APERAK')
    parser.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--raw', action='store_true')

    args = parser.parse_args()
    segs = args.input.read()
    e = EdielParser(segs)
    e.parse()