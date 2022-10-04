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
    def __init__(self,
                 payload: str,
                 format: str,
                 our_ediel: str,
                 our_city: str):
        self.payload = payload # raw input
        self.format = format
        self.segments = self.parse()
        self.our_ediel_id = our_ediel
        self.our_city = our_city

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

    def create_contrl(self, segments=None) -> [Segment]:
        segments = self.segments if segments is None else segments
        unix_timestamp = time.time()
        segment_hash = segments.__str__()
        hash_string = '{}:{}'.format(segment_hash, unix_timestamp).encode('utf-8')
        UNIQUE_ID = str(md5(hash_string).hexdigest())[:14]
        RECIPIENT_EDIEL_ID = self.segments['UNB']['interchange_sender'][0].value

        timestamp_now = edi.format_timestamp(datetime.now())
        partner_identification_code_qualifier = segments['UNB']['interchange_sender'][
            'partner_identification_code_qualifier'].value

        application_reference = segments['UNB']['application_reference'].value

        contrl = []
        contrl.append(UNSegment('UNA'))

        unb = UNSegment('UNB')
        unb['syntax_identifier']['syntax_identifier'] = 'UNOB'
        unb['syntax_identifier']['syntax_version_number'] = '3'
        unb['interchange_sender'] = [self.our_ediel_id, partner_identification_code_qualifier]
        unb['interchange_recipient'] = [RECIPIENT_EDIEL_ID, partner_identification_code_qualifier]
        unb['date-time_of_preparation'] = [timestamp_now[2:8], timestamp_now[8:]]
        unb['interchange_control_reference'] = UNIQUE_ID
        unb['application_reference'] = application_reference
        contrl.append(unb)

        unh = UNSegment('UNH')
        unh['r:0062'] = UNIQUE_ID  # UNIQUE_ID
        unh[1] = ['CONTRL', '2', '2', 'UN', 'EDIEL2']
        contrl.append(unh)

        interchange_reference = segments['UNB']['interchange_control_reference'].value
        sender_identification = segments['UNB']['interchange_sender']['sender_identification'].value
        recepient_identification = segments['UNB']['interchange_recipient']['recipient_identification'].value
        action_coded = '1'

        uci = UNSegment('UCI')
        uci['interchange_control_reference'] = interchange_reference
        uci['interchange_sender']['sender_identification'] = sender_identification
        uci['interchange_recipient']['recipient_identification'] = recepient_identification
        uci['action_coded'] = action_coded
        contrl.append(uci)

        unt = UNSegment('UNT')
        unt[0] = str(reduce(lambda acc, s: acc + 1, contrl, 0) - 1)
        unt[1] = UNIQUE_ID  # segments['UNH']['r:0062'].value
        contrl.append(unt)

        unz = UNSegment('UNZ')
        unz[0] = '1'
        unz[1] = UNIQUE_ID
        contrl.append(unz)

        return edi.rstrip(contrl)

    """
    Generate aperak based on payload information
    """
    def create_aperak(self, segments = None) -> [Segment]:

        segments = self.segments if segments is None else segments

        unix_timestamp = time.time()
        segment_hash = segments.__str__()
        hash_string = '{}:{}'.format(segment_hash, unix_timestamp).encode('utf-8')
        UNIQUE_ID = str(md5(hash_string).hexdigest())[:14]
        RECIPIENT_EDIEL_ID = self.segments['UNB']['interchange_sender'][0].value

        timestamp_now = edi.format_timestamp(datetime.now())
        partner_identification_code_qualifier = segments['UNB']['interchange_sender']['partner_identification_code_qualifier'].value
        doc_message_number = segments['BGM']['document-message_number'].value
        application_reference = segments['UNB']['application_reference'].value

        aperak = [UNSegment('UNA')]

        unb = UNSegment('UNB')
        unb['syntax_identifier']['syntax_identifier'] = 'UNOB'
        unb['syntax_identifier']['syntax_version_number'] = '3'
        unb['interchange_sender'] = [self.our_ediel_id, partner_identification_code_qualifier]
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

        ftx_uts = UNSegment('FTX')
        ftx_uts[0] = 'ZZZ'
        ftx_uts[3] = str(unix_timestamp)
        aperak.append(ftx_uts)

        # group1
        rff =  UNSegment('RFF')
        rff[0] = ['ACW', doc_message_number]
        aperak.append(rff)

        # group 2
        nad1 = UNSegment('NAD')
        nad1['party_qualifier'] = 'MS'
        nad1['party_identification_details'] = [self.our_ediel_id, 'SVK', '260']
        nad1['city_name'] = self.our_city
        nad1['country-coded'] = 'SE'
        aperak.append(nad1)

        nad2 = UNSegment('NAD')
        nad2[0] = 'MR' # message receiver
        nad2[1] = [RECIPIENT_EDIEL_ID, 'SVK', '260']
        aperak.append(nad2)

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