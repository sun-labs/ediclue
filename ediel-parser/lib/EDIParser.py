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
        return list(map(lambda s: s.toDict(), self.segments))

    def toList(self):
        return list(map(lambda s: (s.tag, s.toList()), self.segments))

    def toEdifact(self):
        pass
    
    @staticmethod
    def toEdifact(segments: list):
        message = PMessage()
        for s in segments:
            if s is not None and len(s) > 0:
                tag = s.pop(0)
                message.add_segment(PySegment(tag, *s))
        return message

