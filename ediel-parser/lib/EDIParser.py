from pydifact.message import Message as PMessage
from pydifact.segments import Segment as PSegment

from lib.Segment import Segment

class EDIParser():
    def __init__(self, payload: str):
        self.payload = payload
        self.message = PMessage.from_str(payload)

    def toDict(self):
        pass

    def toList(self):
        pass

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

