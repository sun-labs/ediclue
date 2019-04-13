import os
from lib.EDICommunicator import EDICommunicator
from lib.EDIParser import EDIParser

def set_args(subparsers):
    parser = subparsers.add_parser('com', description='communication between EDI systems')
    parser.add_argument('--send-to')
    parser.add_argument('--from', dest='from_type', choices=['edi'], default='edi', help='The input content type'),
    parser.add_argument('--username', default=os.environ.get('SL_COM_USERNAME'))
    parser.add_argument('--password', default=os.environ.get('SL_COM_PASSWORD'))
    parser.add_argument('--server', default=os.environ.get('SL_COM_SERVER'))
    parser.add_argument('--outgoing-server', default=os.environ.get('SL_COM_OUTGOING_SERVER'))
    parser.add_argument('--incoming-server', default=os.environ.get('SL_COM_INCOMING_SERVER'))

def run(args):
    # dependencies on other arguments
    args.outgoing_server = args.server if args.outgoing_server is None else args.outgoing_server
    args.incoming_server = args.server if args.incoming_server is None else args.incoming_server
    args.send_to = args.username if args.send_to is None else args.send_to

    payload = args.input.read()

    parser = EDIParser(payload, format=args.from_type)
    subject = parser['UNB'].toEdi()
    print(subject)

    com = EDICommunicator()
    com.server = args.server
    com.username = args.username
    com.password = args.password

    mail = com.create_edi_mail(
        send_from='ediel@data.sunlabs.se',
        send_to=args.send_to,
        subject='UNB Segment',
        file_content=payload
    )
    print(mail)