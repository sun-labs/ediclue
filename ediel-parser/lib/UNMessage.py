from lib.messageDefinitions import definitions
from lib.Segment import Segment

def UNMessage(messageId, **args):
    message = definitions.get(messageId)
    if message is None:
        print("https://www.truugo.com/edifact/d96a/{}".format(segmentId))
        return Segment(messageId) # placeholder segment
    return Segment.create_from(message, **args)