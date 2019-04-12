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
    ip.add_argument('--imusername', dest='imap_username')
    ip.add_argument('--impassword', dest='imap_password')
    ip.add_argument('--imserver', dest='imap_server')
    ip.add_argument('--output-directory')

    sp = parser.add_argument_group('smtp')
    sp.add_argument('--smusername', dest='smtp_username')
    sp.add_argument('--smpassword', dest='smtp_password')
    sp.add_argument('--smserver', dest='smtp_server')
    sp.add_argument('--input-directory')

    args = parser.parse_args()

    if args.imap_username is not None and args.imap_password is not None and args.imap_server is not None:
        m = imap.connect(args.imap_server, args.imap_username, args.imap_password)
        output_dir = args.output_directory
        if output_dir is not None:
            print("Downloading attachments to {}".format(output_dir))
            imap.downloadAllAttachmentsInInbox(m, output_dir)
        exit(0)

    if args.smtp_username is not None and args.smtp_password is not None and args.smtp_server is not None:
        m = imap.connect(args.smtp_server, args.smtp_username, args.smtp_password)
        input_dir = args.input_directory
        if input_dir is not None:
            print("Reading attachments in {}".format(input_dir))
            imap.downloadAllAttachmentsInInbox(m, input_dir)
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
