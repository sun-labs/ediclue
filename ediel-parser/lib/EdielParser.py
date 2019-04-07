from pydifact.message import Message
from pydifact.segments import Segment as PySegment
from lib.Segment import Segment

from lib.segmentDefinitions import definitions

class EdielParser():
    def __init__(self, segments):        
        self.msg = Message.from_str(segments)
        self.parsed = {}

    def toDictEach(self, segment: list):
        tag = segment.tag
        elements = segment.elements
        
        definition = definitions.get(tag)
        if definition is not None:
            return definition.toDictOld(elements, tag=tag)
        else:
            print("[MISSING SEGMENT] https://www.truugo.com/edifact/d96a/{}".format(tag))
            return None


    def toDict(self, segments: list = None):
        segments = segments if segments is not None else self.msg.segments
        result = []
        for s in segments:
            parsed = self.toDictEach(s)
            result.append(parsed)
        return result

    @staticmethod
    def toList(segments: dict):
        result = []
        for s in segments:
            parsed = Segment.toList(s)
            result.append(parsed)
        return result

    @staticmethod
    def toEdifact(segments: list):
        message = Message()
        for s in segments:
            if s is not None and len(s) > 0:
                tag = s.pop(0)
                message.add_segment(PySegment(tag, *s))
        return message

