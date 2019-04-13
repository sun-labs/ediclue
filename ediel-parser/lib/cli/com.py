import os
from lib.EDICommunicator import EDICommunicator

def set_args(subparsers):
    parser = subparsers.add_parser('com', description='communication between EDI systems')
    parser.add_argument('action', choices=['aperak', 'download'])
    parser.add_argument('--username', default=os.environ.get('SL_COM_USERNAME'))
    parser.add_argument('--password', default=os.environ.get('SL_COM_PASSWORD'))
    parser.add_argument('--server', default=os.environ.get('SL_COM_SERVER'))
    parser.add_argument('--outgoing-server', default=os.environ.get('SL_COM_OUTGOING_SERVER'))
    parser.add_argument('--incoming-server', default=os.environ.get('SL_COM_INCOMING_SERVER'))

def run(args):
    # dependencies on other arguments
    args.outgoing_server = args.server if args.outgoing_server is None else args.outgoing_server
    args.incoming_server = args.server if args.incoming_server is None else args.incoming_server

    communicator = EDICommunicator()
    communicator.server = args.server
    communicator.username = args.username
    communicator.password = args.password