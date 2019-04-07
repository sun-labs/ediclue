from pydifact.message import Message
from pydifact.segments import Segment as PySegment
from lib.Segment import Segment

class EDIParser():
    def __init__(self, payload: str):
        self.payload = payload
        self.segments = Message.from_str(payload)
        print(self.segments, self.payload)

    @staticmethod
    def toEdifact(segments: list):
        message = Message()
        for s in segments:
            if s is not None and len(s) > 0:
                tag = s.pop(0)
                message.add_segment(PySegment(tag, *s))
        return message

