from lib.messageDefinitions import definitions
from lib.Segment import Segment

from copy import deepcopy

def UNMessage(messageId, **args):
    message = definitions.get(messageId)
    message = deepcopy(message)
    if message is None:
        print("https://www.truugo.com/edifact/d96a/{}".format(segmentId))
        return Segment(messageId) # placeholder segment
    return Segment.create_from(message, **args)