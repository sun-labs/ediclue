from lib.Segment import Segment

"""
https://www.truugo.com/edifact/d96a/unh/
"""

class UNH(Segment):
    def __init__(self, segments):
        for i in range(0, len(segments)):
            d = segments[i]
            if i == 0: self.message_reference_number = d
            elif i == 1: self.message_identifier = d
            elif i == 2: self.common_access_reference = d
            elif i == 3: self.status_of_the_transfer = d