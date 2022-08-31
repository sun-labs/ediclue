import os
from lib.EDICommunicator import EDICommunicator
from lib.EDIParser import EDIParser
import lib.cli.tools as tools
from types import SimpleNamespace

def set_args(subparsers):
    parser = subparsers.add_parser('com', description='communication between EDI systems')
    parser.add_argument('--send-to')
    parser.add_argument('--send-from')
    parser.add_argument('--from', dest='from_type', choices=['mail'], default='mail', help='The input content type'),
    parser.add_argument('--username', default=os.environ.get('SL_COM_USERNAME'))
    parser.add_argument('--password', default=os.environ.get('SL_COM_PASSWORD'))
    parser.add_argument('--server', default=os.environ.get('SL_COM_SERVER'))
    parser.add_argument('--outgoing-server', default=os.environ.get('SL_COM_OUTGOING_SERVER'))
    parser.add_argument('--incoming-server', default=os.environ.get('SL_COM_INCOMING_SERVER'))
    parser.add_argument('--dont-store', help='do not store sent email in sent folder')
    parser.add_argument('--verbose', action='store_true')

    parser.add_argument('--send', action='store_true', help='Send mail')

    parser.add_argument('--list-labels', action='store_true')
    parser.add_argument('--imap-search-query')
    parser.add_argument('--imap-store-query', nargs='+', help='two arguments required: command flags')
    parser.add_argument('--set-label', nargs='+')

    parser.add_argument('--input-dir')
    parser.add_argument('--output-dir')

def handle_send(payload, args):
    com = get_com(args)
    mail = None # result email
    if args.from_type == "mail":
        mail = com.mail_from_str(payload)
    if args.send is True:
        com.send_mail(mail)
    return mail

def get_com(args):
    com = EDICommunicator()
    com.server = args.server
    com.username = args.username
    com.password = args.password
    com.init_imap()
    return com

def vprint(args, *margs):
    if args.verbose is True:
        print(*margs)

def handle_store_query(args, mail_ids_str: str):
    mail_ids = mail_ids_str.split(',') # to list
    com = get_com(args)
    query = args.imap_store_query
    if len(query) < 2:  raise ValueError("You need to supply two arguments for imap-store-query, command and flags")
    cmd, flags = query[0], query[1]
    result_email_ids = com.imap_store_query(mail_ids_str, cmd, '({})'.format(flags))
    return result_email_ids

def run(args):
    # dependencies on other arguments
    args.outgoing_server = args.server if args.outgoing_server is None else args.outgoing_server
    args.incoming_server = args.server if args.incoming_server is None else args.incoming_server
    args.send_from = args.username if args.send_from is None else args.send_from

    com = get_com(args)

    # single commands
    if args.list_labels is True:
        exit(com.list_labels())

    # parse inputs
    load = SimpleNamespace()
    load.files = False
    if args.input_dir: # load mails from directory
        load.files = True
        load.filenames, load.paths = tools.get_files(args.input_dir)
        mail_ids = com.str_mail_ids(com.mail_ids_from_filenames(load.filenames))
    else:
        if args.imap_search_query: # fetch from imap server
            mail_ids = com.imap_search_query(args.imap_search_query)
            mail_ids = com.str_mail_ids(com.format_mail_ids(mail_ids))
        else: # read stdin
            mail_ids = args.input.read()
            mail_ids = mail_ids.replace('\n', '')
    
    mail_ids_lst = mail_ids.split(',')
    mail_ids_lst = list(filter(lambda m: m is not '', map(lambda m: m.strip(), mail_ids_lst)))
    n_mail_ids = len(mail_ids_lst)
    if n_mail_ids == 0: raise SystemExit(1)

    # send emails
    if args.send is True:
        if load.files is True:
            for i, path in enumerate(load.paths):
                fh = open(path, 'r')
                content = fh.read()
                mail = handle_send(content, args)
                if args.imap_store_query:
                    mail_id = mail_ids_lst[i]
                    response_id = handle_store_query(args, mail_id)
                fh.close()
    else: # write emails
        if args.output_dir:
            for mail_id in mail_ids_lst:
                mail = com.get_mail_with(mail_id)
                file_name = '{}.eml'.format(mail_id)
                file_path = os.path.join(args.output_dir, file_name)
                fh = open(file_path, 'w')
                fh.write(mail)
                fh.close()
                
    if args.send is False:
        if args.imap_store_query:
            mail_ids = handle_store_query(args, mail_ids)

    print(mail_ids)