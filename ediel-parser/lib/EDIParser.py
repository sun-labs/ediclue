from pydifact.message import Message as PMessage
from pydifact.segments import Segment as PSegment

from lib.Segment import Segment, Group
from lib.UNSegment import UNSegment

class EDIParser():
    def __init__(self, payload: str):
        self.payload = payload
        self.message = PMessage.from_str(payload)
        self.segments = self.parse()

    def parse(self):
        segments = []
        for s in self.message.segments:
            tag, elements = s.tag, s.elements
            template = UNSegment(tag)
            template.load(elements)
            segments.append(template)
        return segments

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

