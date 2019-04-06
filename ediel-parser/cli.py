import argparse
import sys
import json
from lib.EdielParser import EdielParser
from lib.Generator import Generator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse EDIFACT data')
    parser.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--from', choices=['edifact', 'json'], default='edifact')
    parser.add_argument('--to', choices=['json', 'raw', 'list'], default='json')
    parser.add_argument('--aperak', action='store_true')

    args = parser.parse_args()

    input_data = args.input.read()
    parser = EdielParser(input_data)

    # default output is input
    output = input_data

    if args.to == 'json':
        dictionary = parser.toDict()
        output = json.dumps(dictionary)
    elif args.to == 'list':
        output = parser.msg
    elif args.to == 'raw':
        pass

    if args.aperak is True:
        aperak = Generator.getAperakFor(parser.toDict())
        print(aperak)
        exit(0)

    print(output)