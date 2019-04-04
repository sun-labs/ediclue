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

    def __str__(self):
        keys = filter(lambda k: "__" not in k, dir(self))
        values = map(lambda k: "{}: {}".format(k, getattr(self, k)), keys)
        return "\n".join(values)