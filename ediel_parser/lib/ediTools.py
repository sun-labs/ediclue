from ediel_parser.lib.Segment import Segment

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
    new_segment = Segment.create_from(segment)
    new_children = []
    decrement_val = 1
    end_index = len(segment)
    for i, seg in enumerate(reversed(segment)):
        if len(seg) > 0:
            stripped = _rstrip(seg)
            # print(i, 'len', len(seg), seg.id, segment.children[i].id, stripped.id)
            # segment.children[i] = stripped
            new_children.append(stripped)
            if len(stripped) == 0:
                end_index -= decrement_val
            else:
                decrement_val = 0 # stop decrementing as there's a value
        else:
            new_children.append(seg)
            if seg.value is None:
                end_index -= decrement_val
                continue
            decrement_val = 0 # stop decrementing, but keep on cleaning rest
    # print(list(map(lambda x: ('old', x.id, x.value), segment.children)))
    new_children = list(reversed(new_children)) # reverse back
    new_segment.children = new_children[:end_index]
    # print(list(map(lambda x: (x.id, x.value), segment.children)))
    return new_segment