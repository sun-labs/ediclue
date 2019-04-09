from lib.segmentDefinitions import definitions
from lib.Segment import Segment
from copy import deepcopy

def UNSegment(segmentId, **args):
    segment = definitions.get(segmentId)
    segment = deepcopy(segment)
    if segment is None:
        print("https://www.truugo.com/edifact/d96a/{}".format(segmentId))
        return Segment(tag=segmentId) # placeholder segment
    return Segment.create_from(segment, **args)