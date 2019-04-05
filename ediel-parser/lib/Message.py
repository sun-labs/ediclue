class Message():

    def __init__(self, segment = None, *, mandatory=False, max=1):
        self.segment = segment
        self.mandatory = mandatory
        self.children = []

    def structure(self, children):
        self.children = children
        return self