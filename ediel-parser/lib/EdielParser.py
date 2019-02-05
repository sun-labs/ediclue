import importlib

from pydifact.message import Message
from pydifact.segments import Segment

from lib.Segments.LOC import LOC

class EdielParser():
    def __init__(self, segments):
        self.msg = Message.from_str(segments)
        self.parsed = {}

    def filterServiceSegments(self, segment):
        return "UN" in segment.tag

    def parseSegment(self, segment):
        tag = segment.tag
        elements = segment.elements

        # dynamically loading classes from Segments
        ClassId = "lib.Segments.{}".format(tag)
        Module = None
        try:
            Module = importlib.import_module(ClassId)
        except ModuleNotFoundError:
            print("[{}] Unsupported tag".format(tag))
            return None

        Segment = getattr(Module, tag)
        if Segment is not None:
            structured = Segment(elements)
            print(structured)

    def parse(self, segments = None):
        segments = segments if segments is not None else self.msg.segments
        # messages = filter(lambda s: not self.filterServiceSegments(s), segments)
        for s in segments:
            self.parseSegment(s)

