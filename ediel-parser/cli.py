import argparse
import sys
import json
from lib.EDIParser import EDIParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse EDIFACT data')
    parser.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)

    parser.add_argument('--from', choices=['edifact'], default='edifact'),
    parser.add_argument('--to', choices=['json', 'raw', 'list'], default='json')

    parser.add_argument('--aperak', action='store_true')

    args = parser.parse_args()

    payload = args.input.read()
    parser = EDIParser(payload)

    if args.aperak is True:
        aperak = parser.create_aperak()
        print(aperak)

    