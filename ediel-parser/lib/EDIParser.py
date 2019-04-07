from pydifact.message import Message as PMessage
from pydifact.segments import Segment as PSegment

from lib.UNMessage import UNMessage
from lib.UNSegment import UNSegment

class EDIParser():
    def __init__(self, payload: str):
        self.payload = payload
        self.message = PMessage.from_str(payload)

    @staticmethod
    def toEdifact(segments: list):
        message = PMessage()
        for s in segments:
            if s is not None and len(s) > 0:
                tag = s.pop(0)
                message.add_segment(PySegment(tag, *s))
        return message

