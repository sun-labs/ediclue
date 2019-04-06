class Segment():

    def __init__(self, id = None, *, tag=None, length=(None, None), min=None, max=None, mandatory=False, children = []):
        self.id = id
        self.tag = tag
        self.length = length
        self.min = min
        self.max = max
        self.mandatory = mandatory
        self.children = children

    @classmethod
    def From(cls, segment, **args):
        return cls(segment.id, tag=segment.tag, **args)

    @classmethod
    def Group(cls, id, **args):
        return cls(id, **args)

    """
    Add sub elements to the current object
    """
    def add(self, *children):
        children = list(children)
        self.children = children
        return self

    def validate(self, segment):
        return True # TODO: validate every segment

    """
    Convert dict edifact segment to
    list form (for pydifact)
    """
    @staticmethod
    def toList(segments):
        if segments is None: return None
        result = []
        for k in segments.keys():
            segment = segments.get(k)
            if type(segment) is not dict:
                result.append(segment)
            else:
                rec_result = Segment.toList(segment)
                if rec_result is not None:
                    result.append(rec_result)
        return result


    """
    Validate and parse EDIFACT segment
    @return the parsed segment
    @error ValueError
    """
    def toDict(self, segment, children = None, tag=None):
        children = self.children if children is None else children
        n_children = len(children)
        n_segments = len(segment)
        parsed = {}
        if tag is not None:
            parsed['tag'] = tag

        if type(segment) is not list:
            if self.id is None:
                return segment
            else:
                parsed[self.id] = segment
        else:
            for i in range(0, n_children):
                segment_def = children[i]
                is_mandatory = segment_def.mandatory 
                out_of_bounds = (i >= n_segments)
                if out_of_bounds and is_mandatory:
                    parsed[segment_def.id] = {
                        'type': 'error',
                        'message': 'mandatory field [{}] not supplied'.format(segment_def.id),
                        'structure': segment_def
                    }
                if not out_of_bounds:
                    parsed[segment_def.id] = self.toDict(segment[i], segment_def.children)
        return parsed

    def __str__(self):
        keys = filter(lambda k: "__" not in k, dir(self))
        values = map(lambda k: "{}: {}".format(k, getattr(self, k)), keys)
        return "\n".join(values)

# Alias
Group = Segment