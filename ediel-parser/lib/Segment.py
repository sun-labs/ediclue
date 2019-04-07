class Segment():

    def __init__(self, id=None, *, tag=None, length=(None, None), min=None, max=None, mandatory=False, children=[], elements=[], value=None):
        self.id = id or tag
        self.length = length
        self.min = min
        self.max = max
        self.mandatory = mandatory
        self.children = children
        self.elements = elements
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
    list form
    """
    def toList(self):
        return self._toList(segment=self)

    def _toList(self, segment):
        result = []
        for k in segments.keys():
            segment = segments.get(k)
            if type(segment) is not dict: # base case
                result.append(segment)
            else: # recursion
                rec = self._toList(segment)
                result.append(rec)
        return result
    
    """
    Create dictionary of segments with explanatory keys
    """
    def toDict(self):
        return self._toDict(segment=self)

    def _toDict(self, segment):
        result = {}
        children = segment.children
        if len(children) > 0: # recursion
            for i in range(0, len(children)):
                cur = children[i]
                result[cur.id] = self._toDict(segment=cur)
        else: # base case
            result = segment.value
        return result

Group = Segment.create_group
From = Segment.create_from