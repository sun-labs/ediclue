import json
from pydifact.message import Message as PMessage
from pydifact.segments import Segment as PSegment

from lib.Segment import Segment, Group
from lib.UNSegment import UNSegment

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

    def parse_edi(self):
        message = PMessage.from_str(self.payload)
        segments = []
        for s in message.segments:
            tag, elements = s.tag, s.elements
            template = UNSegment(tag)
            template.load(elements)
            segments.append(template)
        return segments

    def parse_json(self):
        segments = []
        segment_list = self.flatten_json()
        for segment in segment_list:
            tag = segment.pop(0)
            elements = segment
            template = UNSegment(tag)
            template.load(elements)
            segments.append(template)
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


    def toDict(self):
        raw_result = map(lambda s: s.toDict(), self.segments)
        result = filter(lambda s: s is not None, raw_result)
        return list(result)

    def toList(self):
        raw_result = map(lambda s: [s.tag, s.toList()], self.segments)
        result = filter(lambda s: s is not None, raw_result)
        return list(result)

    def toEdi(self):
        message = PMessage()
        for s in self.segments:
            elements = s.toList()
            if elements is not None and len(elements) > 0:
                tag = s.tag
                segment = PSegment(tag, *elements)
                message.add_segment(segment)
        return message.serialize()

