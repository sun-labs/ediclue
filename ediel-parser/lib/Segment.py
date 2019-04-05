class Segment():

    def __init__(self, id = None, *, length=(None, None), min=None, max=None, mandatory=False):
        self.id = id
        self.length = length
        self.min = min
        self.max = max
        self.mandatory = mandatory
        self.children = []

    def structure(self, children):
        self.children = children
        return self

    def validate(self, segment):
        return True # TODO: validate every segment

    """
    Validate and parse EDIFACT segment
    @return the parsed segment
    @error ValueError
    """
    def parse(self, segment, children = None, tag=None):
        children = self.children if children is None else children
        n_children = len(children)
        n_segments = len(segment)
        parsed = {}
        if tag is not None:
            parsed['segment'] = tag

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
                    parsed[segment_def.id] = self.parse(segment[i], segment_def.children)
        return parsed

    def __str__(self):
        keys = filter(lambda k: "__" not in k, dir(self))
        values = map(lambda k: "{}: {}".format(k, getattr(self, k)), keys)
        return "\n".join(values)