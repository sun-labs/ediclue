from lib.Segment import Segment

"""
https://www.truugo.com/edifact/d96a/qty/
"""

class QTY(Segment):
    def __init__(self, segments):
        for i in range(0, len(segments)):
            d = segments[i]
            self.quantity_details = Segment()
            for j in range(0, len(d)):
                dd = d[j]
                if i == 0: self.quantity_details.quantity_qualifier = dd
                elif i == 1: self.quantity = dd
                elif i == 2: self.measure_unit_qualifier = dd