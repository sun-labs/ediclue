import json
from datetime import datetime
from functools import reduce
from hashlib import md5
import time
import email
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders

from pydifact.message import Message as PMessage

from ediel_parser.lib.Segment import Segment, Group
from ediel_parser.lib.UNSegment import UNSegment
import ediel_parser.lib.ediTools as edi

EDI_FILENAME = 'edifact.edi'

class EDIParser():
    def __init__(self, payload: str, format: str):
        self.payload = payload # raw input
        self.format = format
        self.segments = self.parse()

    def __getitem__(self, key):
        if type(key) is str:
            for segment in self.segments:
                if segment.tag == key:
                    return segment

    def parse(self):
        if self.format == 'edi':
            return self.parse_edi()
        elif self.format == 'json':
            return self.parse_json()
        elif self.format == 'mail':
            return self.parse_email()

    def get_props_for(self, segment) -> (str, list):
        if self.format == 'json':
            return segment.pop(0), segment
        elif self.format == 'edi' or self.format == 'mail':
            return segment.tag, segment.elements

    def get_attachment_from_mail(self, mail_str=None):
        mail_str = self.payload if mail_str is None else mail_str
        mail = email.message_from_string(mail_str)
        for i, part in enumerate(mail.walk()):
            if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                return part.get_payload(decode=True)
        return mail

    def parse_email(self):
        content = self.get_attachment_from_mail()
        content = content.decode('utf-8')
        segments = self.parse_edi(content)
        return segments
        

    def load_segment(self, segment):
        tag, elements = self.get_props_for(segment)
        template = UNSegment(tag)
        template.load(elements)
        return template

    def parse_edi(self, payload=None):
        payload = self.payload if payload is None else payload
        message = PMessage.from_str(payload)
        segments = Group(self.format).structure(
            *map(self.load_segment, message.segments)
        )
        return segments

    def parse_json(self, payload=None):
        payload = self.payload if payload is None else payload
        segments = []
        segment_list = self.flatten_json(payload)
        segments = Group(self.format).structure(
            *map(self.load_segment, segment_list)
        )
        return segments

    def flatten_json(self, payload=None) -> list:
        payload = self.payload if payload is None else payload
        message = json.loads(payload)
        result = []
        for segment in message:
            result.append(self._flatten_json(segment))
        return result

    def _flatten_json(self, segment) -> list:
        # flatten the segments to arrays
        # load as edi message
        segments = []
        if type(segment) is dict:
            for k in segment.keys():
                cur = segment[k]
                segments.append(self._flatten_json(cur))
            return segments
        else:
            return segment

    """
    Generate aperak based on payload information
    """
    def create_aperak(self, segments = None) -> [Segment]:

        segments = self.segments if segments is None else segments

        unix_timestamp = time.time()
        segment_hash = segments.__str__()
        hash_string = '{}:{}'.format(segment_hash, unix_timestamp).encode('utf-8')
        UNIQUE_ID = str(md5(hash_string).hexdigest())[:14]

        APERAK_PREFIX = 'SLAPE'
        APERAK_START_ID = 1337
        OUR_EDIEL_ID = '27860'
        RECIPIENT_EDIEL_ID = self.segments['UNB']['interchange_sender'][0].value

        aperak_cnt = 0

        timestamp_now = edi.format_timestamp(datetime.now())
        partner_identification_code_qualifier = segments['UNB']['interchange_sender']['partner_identification_code_qualifier'].value
        reference_no = segments['BGM']['r:1004'].value

        doc_name = segments['BGM']['document-message_name']
        doc_message_name_code = doc_name['document-message_name-coded'].value
        doc_responsible_agency = doc_name['code_list_responsible_agency-coded'].value
        doc_message_number = segments['BGM']['document-message_number'].value
        application_reference = segments['UNB']['application_reference'].value

        aperak = []
        aperak.append(UNSegment('UNA'))

        unb = UNSegment('UNB')
        unb['syntax_identifier']['syntax_identifier'] = 'UNOB'
        unb['syntax_identifier']['syntax_version_number'] = '3'
        unb['interchange_sender'] = [OUR_EDIEL_ID, partner_identification_code_qualifier]
        unb['interchange_recipient'] = [RECIPIENT_EDIEL_ID, partner_identification_code_qualifier]
        unb['date-time_of_preparation'] = [timestamp_now[2:8], timestamp_now[8:]]
        unb['interchange_control_reference'] = UNIQUE_ID
        unb['application_reference'] = application_reference
        aperak.append(unb)
        
        unh = UNSegment('UNH')
        unh['r:0062'] = UNIQUE_ID # UNIQUE_ID
        unh[1] = ['APERAK', 'D', '96A', 'UN', 'EDIEL2']
        aperak.append(unh)

        bgm = UNSegment('BGM')
        bgm['response_type-coded'] = '29'
        aperak.append(bgm)

        dtm = UNSegment('DTM')
        dtm[0] = ['137', timestamp_now, '203']
        aperak.append(dtm)

        # timezone = UNSegment('DTM')
        # timezone[0] = ['735', '+0100', '406']
        # aperak.append(timezone)

        ftx_uts = UNSegment('FTX') # unix timestamp sparad
        ftx_uts[0] = 'ZZZ'
        ftx_uts[3] = str(unix_timestamp)
        aperak.append(ftx_uts)

        # doc = UNSegment('DOC')
        # doc[0] = [doc_message_name_code, '', doc_responsible_agency]
        # doc[1] = [doc_message_number]
        # print(doc)
        # aperak.append(doc)

        # group1
        rff =  UNSegment('RFF')
        rff[0] = ['ACW', doc_message_number]
        aperak.append(rff)

        # group 2
        nad1 = UNSegment('NAD')
        nad1['party_qualifier'] = 'MS' # message sender
        nad1['party_identification_details'] = [OUR_EDIEL_ID, 'SVK', '260']
        nad1['city_name'] = 'UPPSALA'
        nad1['country-coded'] = 'SE'
        aperak.append(nad1)

        nad2 = UNSegment('NAD')
        nad2[0] = 'MR' # message receiver
        nad2[1] = [RECIPIENT_EDIEL_ID, 'SVK', '260']
        aperak.append(nad2)

        # nad3 = UNSegment('NAD')
        # nad3[0] = 'DDQ'
        # aperak.append(nad3)

        # init loop of transaction
        # for s in segments:
        #     if s.tag == 'IDE': # transaction
        #         transaction_id = s['identification_number']['identity_number'].value

        #         # group 3
        #         erc = UNSegment('ERC') # godkänt
        #         erc[0] = ['100', None, '260']
        #         aperak.append(erc)
                
        #         ftx = UNSegment('FTX') # godkänt
        #         ftx[0] = 'AAO'
        #         ftx[3] = 'OK'
        #         aperak.append(ftx)

        #         aperak_id = str(APERAK_START_ID + aperak_cnt)
        #         aperak_cnt += 1
        #         rff = UNSegment('RFF')
        #         rff[0] = ['DM', aperak_id]
        #         aperak.append(rff)

        #         rff2 = UNSegment('RFF')
        #         rff2[0] = ['ACW', transaction_id] # refererar till transaktionen som godkäns
        #         aperak.append(rff2)

        unt = UNSegment('UNT')
        unt[0] = str(reduce(lambda acc, s: acc + 1, aperak, 0) - 1)
        unt[1] = UNIQUE_ID # segments['UNH']['r:0062'].value
        aperak.append(unt)

        unz = UNSegment('UNZ')
        unz[0] = '1'
        unz[1] = UNIQUE_ID
        aperak.append(unz)
        
        return edi.rstrip(aperak)

    """
    Dictionary out of payload segments
    """
    def toDict(self, segments = None) -> list:
        segments = self.segments if segments is None else segments
        # segments = edi.rstrip(segments)
        raw_result = map(lambda s: s.toDict(), segments)
        result = filter(lambda s: s is not None, raw_result)
        return list(result)

    """
    List out of payload segments
    """
    def toList(self, segments = None) -> list:
        segments = self.segments if segments is None else segments
        # segments = edi.rstrip(segments)
        raw_result = map(lambda s: [s.tag, s.toList()], segments)
        result = filter(lambda s: s is not None, raw_result)
        return list(result)

    """
    EDI string out of payload segments
    """
    def toEdi(self, segments=None) -> str:
        segments = self.segments if segments is None else segments
        # segments = edi.rstrip(segments)
        raw_result = map(lambda s: s.toEdi(), segments)
        return ''.join(raw_result)

    def current_mail(self):
        return email.message_from_string(self.payload)

    def toMail(self, segments=None, send_from=None, send_to=None, subject=None, filename=None):
        cur = self.current_mail()
        mail = MIMEBase('application', "EDIFACT")
        mail['From'] = cur['To'] if send_from is None else send_from
        mail['To'] = cur['From']
        mail['Date'] = formatdate(localtime=True)
        unb = list(filter(lambda s: s.tag == 'UNB', segments))[0]
        mail['Subject'] = unb.toEdi()

        file_content = self.toEdi(segments)
        mail.set_payload(file_content)
        encoders.encode_base64(mail)
        mail.add_header('Content-Disposition', 'attachment; filename="{}"'.format(EDI_FILENAME))

        return mail