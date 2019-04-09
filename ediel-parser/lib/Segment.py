class Segment():

    def __init__(self, id=None, *, tag=None, length=(None, None), min=None, max=None, mandatory=False, children=[], value=None):
        self.id = tag or id
        self.tag = tag
        self.length = length
        self.min = min
        self.max = max
        self.mandatory = mandatory
        self.children = children
        self.value = value

    def __getitem__(self, key):
        for child in self.children:
            if child.id == key:
                return child
        raise IndexError('{} does not exist'.format(key))
        
    def __setitem__(self, key, value):
        for child in self.children:
            if child.id == key:
                child.value = value
                return
        raise IndexError('{} does not exist'.format(key))
    
    def __delitem__(self, key):
        children = self.children
        for i in range(0, len(children)):
            child = children[i]
            if child.id == key:
                return self.children.pop(i)
        raise IndexError('{} does not exist'.format(key))

    def __str__(self):
        message = ''
        n_children = len(self.children)
        if self.tag is not None:
            message += '[{}] '.format(self.tag)
        if type(self.children) is list and n_children > 0:
            for child in self.children:
                message += child.__str__()
        else:
            if self.tag is None:
                message += '({}:{}), '.format(self.id, self.value)

        if self.tag is not None:
            message += '\n'
        return message
        

    @classmethod
    def create_template(cls, id=None, **args):
        return cls(id, tag=segment.tag, **args)

    @classmethod
    def create_from(cls, segment, **args):
        args = {
            **args,
            "id": segment.id,
            "tag": segment.tag,
            "max": segment.max,
            "min": segment.min,
            "length": segment.length,
            "mandatory": segment.mandatory,
            "children": segment.children,
        }
        return cls(**args)

    @classmethod
    def create_group(cls, id=None, **args):
        return cls(id, **args)

    def set_elements(self, elements):
        self.elements = elements

    def load(self, segments: list):
        self._load(segments, self.children)

    def _load(self, segments: list, def_segments: list):
        n_segments = len(segments)
        n_def_segments = len(def_segments)
        for i in range(0, n_def_segments):
            if (i < n_segments):
                value = segments[i]
                if type(value) is list:
                    self._load(value, def_segments[i].children)
                else:
                    def_segments[i].value = value

    """
    Add sub elements to the current object
    """
    def structure(self, *children):
        children = list(children)
        self.children = children
        return self

    def validate(self, segment):
        return True # TODO: validate every segment

    """
    Convert dict edifact segment to
    list form
    """
    def toList(self):
        return self._toList(segment=self)

    def _toList(self, segment):
        result = []
        children = segment.children
        n_children = len(children)
        if n_children > 0:
            for i in range(0, n_children):
                cur = children[i]
                value = self._toList(segment=cur)
                if value is not None:
                    result.append(value)
        else:
            if segment.value is not None:
                result = segment.value 
        return result if len(result) > 0 else None

    """
    Create dictionary of segments with explanatory keys
    """
    def toDict(self):
        return self._toDict(segment=self)

    def _toDict(self, segment):
        result = {}
        tag = segment.tag
        if tag is not None:
            result['tag'] = tag
        children = segment.children
        n_children = len(children)
        if n_children > 0: # recursion
            for i in range(0, n_children):
                cur = children[i]
                result[cur.id] = self._toDict(segment=cur)
        else: # base case
            result = segment.value
        return result

Group = Segment.create_group
From = Segment.create_from