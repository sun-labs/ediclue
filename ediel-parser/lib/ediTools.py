from lib.Segment import Segment

def format_timestamp(ts):
    return ts.strftime("%Y%m%d%H%M")

def recurse(func, segments):
    for s in segments:
        if len(s) > 0:
            recurse(func, s)
        else:
            func(s)

def rstrip(segments: [Segment]):
    new_segments = []
    for message in segments:
        new_segments.append(_rstrip(message))
    return new_segments

def _rstrip(segment: Segment):
    decrement_val = 1
    end_index = len(segment)
    for i, seg in enumerate(reversed(segment)):
        if len(seg) > 0:
            stripped = _rstrip(seg)
            # print(i, 'len', len(seg), seg.id, segment.children[i].id, stripped.id)
            segment.children[i] = stripped
            if len(stripped) == 0:
                end_index -= decrement_val
            else:
                decrement_val = 0 # stop decrementing as there's a value
        else:
            if seg.value is None:
                end_index -= decrement_val
                continue
            decrement_val = 0 # stop decrementing, but keep on cleaning rest
    # print(list(map(lambda x: ('old', x.id, x.value), segment.children)))
    segment.children = segment.children[:end_index]
    # print(list(map(lambda x: (x.id, x.value), segment.children)))
    return segment