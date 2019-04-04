from lib.Segment import Segment

"""
https://www.truugo.com/edifact/d96a/seq/
"""

class SEQ(Segment):
    def __init__(self, segments):
        for i in range(0, len(segments)):
            d = segments[i]
            if i == 0: self.status_indicator = d
            elif i == 1: 
                self.sequence_information = Segment()
                for j in range(0, len(d)):
                    dd = d[j]
                    if i == 0: self.sequence_information.sequence_number = dd
                    elif i == 1: self.sequence_information.sequence_number_source = dd
                    elif i == 2: self.sequence_information.code_list_qualifier = dd
                    elif i == 3: self.sequence_information.code_list_responsible_agency = dd