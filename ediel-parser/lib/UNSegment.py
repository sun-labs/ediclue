from lib.segmentDefinitions import definitions
from lib.Segment import Segment
from copy import deepcopy

def UNSegment(segmentId, **args):
    segment = definitions.get(segmentId)
    if segment is None:
        return Segment(tag=segmentId) # placeholder segment
    else:
        segment = deepcopy(segment)
        return Segment.create_from(segment, **args)