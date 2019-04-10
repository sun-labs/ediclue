import json
from datetime import datetime
from functools import reduce

from pydifact.message import Message as PMessage
from pydifact.segments import Segment as PSegment

from lib.Segment import Segment, Group
from lib.UNSegment import UNSegment
from lib.UNMessage import UNMessage
import lib.ediTools as edi

class EDIParser():
    def __init__(self, payload: str, format: str):
        self.payload = payload
        self.format = format
        self.segments = self.parse()

    def parse(self):
        if self.format == 'edi':
            return self.parse_edi()
        elif self.format == 'json':
            return self.parse_json()

    def get_props_for(self, segment) -> (str, list):
        if self.format == 'json':
            return segment.pop(0), segment
        elif self.format == 'edi':
            return segment.tag, segment.elements

    def load_segment(self, segment):
        tag, elements = self.get_props_for(segment)
        template = UNSegment(tag)
        template.load(elements)
        return template

    def parse_edi(self):
        message = PMessage.from_str(self.payload)
        segments = Group(self.format).structure(
            *map(self.load_segment, message.segments)
        )
        return segments

    def parse_json(self):
        segments = []
        segment_list = self.flatten_json()
        segments = Group(self.format).structure(
            *map(self.load_segment, segment_list)
        )
        return segments

    def flatten_json(self) -> list:
        message = json.loads(self.payload)
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

        UNIQUE_ID = '1333333777'
        APERAK_PREFIX = 'SLAPE'
        APERAK_START_ID = 1337
        OUR_EDIEL_ID = '27860'
        RECIPIENT_EDIEL_ID = self.segments['UNB']['interchange_sender'][0].value

        aperak_cnt = 0

        partner_identification_code_qualifier = segments['UNB']['interchange_sender']['partner_identification_code_qualifier'].value
        timestamp_now = edi.format_timestamp(datetime.now())
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
        unb['date-time_of_preparation'] = [timestamp_now[:8], timestamp_now[8:]]
        unb['interchange_control_reference'] = UNIQUE_ID
        unb['application_reference'] = application_reference
        aperak.append(unb)
        
        unh = UNSegment('UNH')
        unh[0] = '1'
        unh[1] = ['APERAK', 'D', '96A', 'UN', 'EDIEL2']
        aperak.append(unh)

        bgm = UNSegment('BGM')
        bgm[3] = '27'
        aperak.append(bgm)

        dtm = UNSegment('DTM')
        dtm[0] = ['137', timestamp_now, '203']
        aperak.append(dtm)

        timezone = UNSegment('DTM')
        timezone[0] = ['735', '+0100', '406']
        aperak.append(timezone)

        doc = UNSegment('DOC')
        doc[0] = [doc_message_name_code, '', doc_responsible_agency]
        doc[1] = [doc_message_number]
        aperak.append(doc)

        nad1 = UNSegment('NAD')
        nad1[0] = 'MS' # message sender
        nad1[1] = [OUR_EDIEL_ID, 'SVK', '260']
        nad1['r:3164'] = 'UPPSALA'
        nad1['r:3207'] = 'SE'
        aperak.append(nad1)

        nad2 = UNSegment('NAD')
        nad2[0] = 'MR' # message receiver
        nad2[1] = [RECIPIENT_EDIEL_ID, 'SVK', '260']
        aperak.append(nad2)

        nad3 = UNSegment('NAD')
        nad3[0] = 'DDQ'
        aperak.append(nad3)

        # init loop of transaction
        for s in segments:
            if s.tag == 'IDE': # transaction
                transaction_id = s['identification_number']['identity_number'].value

                erc = UNSegment('ERC') # godkänt
                erc[0] = ['100', None, '260']
                aperak.append(erc)
                
                ftx = UNSegment('FTX') # godkänt
                ftx[0] = 'AAO'
                ftx[3] = 'OK'
                aperak.append(ftx)

                aperak_id = str(APERAK_START_ID + aperak_cnt)
                aperak_cnt += 1
                rff = UNSegment('RFF')
                rff[0] = ['DM', aperak_id]
                aperak.append(rff)

                rff2 = UNSegment('RFF')
                rff2[0] = ['ACW', transaction_id] # refererar till transaktionen som godkäns
                aperak.append(rff2)

        unt = UNSegment('UNT')
        unt[0] = str(reduce(lambda acc, s: acc + 1, aperak, 0) - 2)
        unt[1] = segments['UNH']['r:0062'].value
        aperak.append(unt)

        unz = UNSegment('UNZ')
        unz[0] = '1'
        unz[1] = UNIQUE_ID

        return aperak

    """
    Dictionary out of payload segments
    """
    def toDict(self, segments = None) -> list:
        segments = self.segments if segments is None else segments
        raw_result = map(lambda s: s.toDict(), segments)
        result = filter(lambda s: s is not None, raw_result)
        return list(result)

    """
    List out of payload segments
    """
    def toList(self, segments = None) -> list:
        segments = self.segments if segments is None else segments
        raw_result = map(lambda s: [s.tag, s.toList()], segments)
        result = filter(lambda s: s is not None, raw_result)
        return list(result)

    """
    EDI string out of payload segments
    """
    def toEdi(self, segments=None) -> str:
        segments = self.segments if segments is None else segments
        message = PMessage()
        return self._toEdi(segments, message)

    def _toEdi(self, segments = None, message = None) -> str:
        for s in segments:
            if s.group is True:
                self._toEdi(s, message)
            else:
                elements = s.toList()
                if elements is not None and len(elements) > 0:
                    tag = s.tag
                    segment = PSegment(tag, *elements)
                    message.add_segment(segment)
        return message.serialize()

    

