class Segment():
    def __str__(self):
        keys = filter(lambda k: "__" not in k, dir(self))
        values = map(lambda k: "{}: {}".format(k, getattr(self, k)), keys)
        return "\n".join(values)