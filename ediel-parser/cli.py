import argparse
import sys
import json
import os

from lib.EDIParser import EDIParser
import lib.imapTools as imap


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse EDIFACT data')

    pp = parser.add_argument_group('parser')
    pp.add_argument('--input', type=argparse.FileType('r'), default=sys.stdin)
    pp.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)
    pp.add_argument('--from', dest='from_type', choices=['edi', 'json'], default='edi'),
    pp.add_argument('--to', dest='to_type', choices=['json', 'raw', 'json-arr', 'edi'], default='json')
    pp.add_argument('--aperak', action='store_true')

    ip = parser.add_argument_group('imap')
    ip.add_argument('--username')
    ip.add_argument('--password')
    ip.add_argument('--server')
    ip.add_argument('--output-directory')

    args = parser.parse_args()

    if args.username is not None and args.password is not None and args.server is not None:
        m = imap.connect(args.server, args.username, args.password)
        output_dir = args.output_directory
        if output_dir is not None:
            print("Downloading attachments to {}".format(output_dir))
            imap.downloadAllAttachmentsInInbox(m, output_dir)
        exit(0)

    payload = args.input.read()
    parser = EDIParser(payload, format=args.from_type)

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

    print(result)
