import argparse
import sys
import json

from lib.EDIParser import EDIParser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse EDIFACT data')
    parser.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)

    parser.add_argument('--from', choices=['edifact'], default='edifact'),
    parser.add_argument('--to', choices=['json', 'raw', 'json-arr'], default='json')

    parser.add_argument('--aperak', action='store_true')

    args = parser.parse_args()

    payload = args.input.read()
    parser = EDIParser(payload)

    if args.to == 'json':
        result = json.dumps(parser.toDict())
    elif args.to == 'json-arr':
        result = json.dumps(parser.toList())
    elif args.to == 'raw':
        result = payload
        

    if args.aperak is True:
        aperak = parser.create_aperak()
        print(aperak)

    print(result)
    