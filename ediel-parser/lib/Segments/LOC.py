from lib.Segment import Segment
"""
https://www.truugo.com/edifact/d96a/loc/

TODO: Fix sub segment parsing, for example see QTY.
"""
class LOC(Segment):
    def __init__(self, segments):
        for i in range(len(segments)):
            d = segments[i]
            if i == 0: self.location_qualifier = d
            elif i == 1: self.location_identifier = d
            elif i == 2: self.related_location_one_identification = d
            elif i == 3: self.related_location_two_identification = d
            elif i == 4: self.relation_coded = d