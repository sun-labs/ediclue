from lib.Segment import Segment

"""
https://www.truugo.com/edifact/d96a/qty/
"""

class QTY(Segment):
    def __init__(self, segments):
        for i in range(0, len(segments)):
            d = segments[i]
            if i == 0: self.quantity_identifier = {
                "quantity_qualifier": d[0],
                "quantity": d[1],
                "measure_unit_qualifier": d[2] if len(d) > 2 else None
            }