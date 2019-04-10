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
    for segment in segments:
        end_index, new_segment = _rstrip(segment)
        new_segments.append(new_segment)
    return new_segments

def _rstrip(segment: Segment):
    new_children = []
    end_index = len(segment)
    for child in reversed(segment):
        if len(child) > 0:
            end_index, new_segment = _rstrip(child)
            new_children.append(new_segment.children[:end_index]) # skip null children
        else:
            if child.value is None:
                end_index -= 1
                continue
            break
    segment.children = new_children
    return end_index, segment