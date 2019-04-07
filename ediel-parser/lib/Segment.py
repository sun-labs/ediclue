class Segment():

    def __init__(self, id=None, *, tag=None, length=(None, None), min=None, max=None, mandatory=False, children=[], elements=[]):
        self.id = id or tag
        self.length = length
        self.min = min
        self.max = max
        self.mandatory = mandatory
        self.children = children
        self.elements = elements

    @classmethod
    def create_template(cls, id=None, **args):
        return cls(id, tag=segment.tag, **args)

    @classmethod
    def create_from(cls, segment, **args):
        if segment is None: return
        args = {
            **args,
            "id": segment.id,
            "children": segment.children,
            "max": segment.max,
            "min": segment.min,
            "length": segment.length,
            "mandatory": segment.mandatory
        }
        print(args)
        return cls(**args)

    @classmethod
    def create_group(cls, id, **args):
        return cls(id, **args)

    def set_elements(self, elements):
        self.elements = elements

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
    

    def toDict(self):
        return self._toDict(segment=self)

    def _toDict(self, segment):
        parsed = {}
        children = segment.children
        if len(children) > 0: # recursion
            for i in range(0, len(children)):
                cur = children[i]
                parsed[cur.id] = self._toDict(segment=cur)
        else: # base case
            parsed = None
        return parsed

    """
    Validate and parse EDIFACT segment
    @return the parsed segment
    @error ValueError
    """
    def toDictOld(self, segment=None, children=None, tag=None):
        children = self.children if children is None else children
        n_children = len(children) if children is not None else 0
        n_segments = len(segment) if segment is not None else 0
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
                out_of_bounds = (i >= n_segments) and segment is not None
                if out_of_bounds and is_mandatory:
                    parsed[segment_def.id] = {
                        'type': 'error',
                        'message': 'mandatory field [{}] not supplied'.format(segment_def.id),
                        'structure': segment_def
                    }
                if not out_of_bounds:
                    value = segment[i] if segment is not None else None
                    parsed[segment_def.id] = self.toDictOld(value, segment_def.children)
        return parsed

Group = Segment.create_group
From = Segment.create_from