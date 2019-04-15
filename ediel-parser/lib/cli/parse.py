import argparse
import json
import os
from lib.EDIParser import EDIParser
import lib.cli.tools as tools

def set_args(subparsers):
    parser = subparsers.add_parser('parse', description='parsing of edi to supported formats and generation of messages')
    parser.add_argument('--from', dest='from_type', choices=['edi', 'json', 'mail'], default='edi'),
    parser.add_argument('--to', dest='to_type', choices=['json', 'raw', 'json-arr', 'edi', 'mail'], default='json')
    parser.add_argument('--aperak', action='store_true')
    parser.add_argument('--input-dir')
    parser.add_argument('--output-dir')

def handle_parse(content, args):
    parser = EDIParser(content, format=args.from_type)

    work_result = None
    if args.aperak is True:
        work_result = parser.create_aperak()

    to_type = args.to_type
    if to_type == 'json':
        result = json.dumps(parser.toDict(work_result))
    elif to_type == 'json-arr':
        result = json.dumps(parser.toList(work_result))
    elif to_type == 'edi':
        result = parser.toEdi(work_result)
        result = result.replace("'", "'\n") # pretty print
    elif to_type == 'raw':
        result = payload
    elif to_type == 'mail':
        result = parser.toMail(work_result)

    return result

def run(args):

    if args.input_dir is not None:
        filenames, full_paths = tools.get_files(args.input_dir)
        for path in full_paths:
            extension = tools.extension_for_type(args.to_type)
            filename = '{}.{}'.format(os.path.basename(path), extension)
            fh = open(path, 'r')
            content = fh.read()
            fh.close()
            result = handle_parse(content, args)
            if args.output_dir is None:
                print(result)
            else:
                path = os.path.join(args.output_dir, filename)
                fh = open(path, 'w')
                print(result)
                fh.write(result.__str__())
                fh.close()
        return args.output_dir
    else:
        payload = args.input.read()
        result = handle_parse(payload, args)
        print(result)