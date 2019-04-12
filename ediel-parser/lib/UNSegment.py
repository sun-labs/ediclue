from lib.segmentDefinitions import definitions
from lib.Segment import Segment
from copy import deepcopy

def UNSegment(segmentId, **args):
    segment = definitions.get(segmentId)
    if segment is None:
        print("https://www.truugo.com/edifact/d96a/{}".format(segmentId))
        return Segment(tag=segmentId) # placeholder segment
    else:
        segment = deepcopy(segment)
        return segment