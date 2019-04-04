import importlib

from pydifact.message import Message
from pydifact.segments import Segment

from lib.segmentDefinitions import definitions

class EdielParser():
    def __init__(self, segments):
        self.msg = Message.from_str(segments)
        self.parsed = {}

    def parseSegment(self, segment):
        tag = segment.tag
        elements = segment.elements
        
        definition = definitions.get(tag)
        if definition is not None:
            return definition.parse(elements)


    def parse(self, segments = None):
        segments = segments if segments is not None else self.msg.segments
        result = []
        for s in segments:
            result.append(self.parseSegment(s))
        print(result)

