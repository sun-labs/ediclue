from lib.Segment import Segment

definitions = {
    "SEQ": Segment(length=(0,3)).structure([
        Segment("status_indicator_coded"), 
        Segment("sequence_information", min=0, max=1).structure([
            Segment("sequence_number", mandatory=True, length=(0,6)),
            Segment("sequence_number_source", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency", length=(0,3))
        ])
    ])
}