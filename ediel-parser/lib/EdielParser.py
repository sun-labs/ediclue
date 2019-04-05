import importlib

from pydifact.message import Message
from pydifact.segments import Segment

from lib.segmentDefinitions import definitions

class EdielParser():
    def __init__(self, segments):
        self.msg = Message.from_str(segments)
        self.parsed = {}

    def toDictEach(self, segment):
        tag = segment.tag
        elements = segment.elements
        
        definition = definitions.get(tag)
        if definition is not None:
            return definition.toDict(elements, tag=tag)
        else:
            if tag != "UNA":
                print("[MISSING SEGMENT] https://www.truugo.com/edifact/d96a/{}".format(tag))
                return None


    def toDict(self, segments = None):
        segments = segments if segments is not None else self.msg.segments
        result = []
        for s in segments:
            parsed = self.toDictEach(s)
            result.append(parsed)
        return result

    @staticmethod
    def toList(self, segments):
        result = []
        
        return Segment.flatten(segmentDict)

