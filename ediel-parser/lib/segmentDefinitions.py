from lib.Segment import Segment

definitions = {
    "SEQ": Segment().structure([
        Segment("status_indicator_coded"), 
        Segment("sequence_information", min=0, max=1).structure([
            Segment("sequence_number", mandatory=True, length=(0,6)),
            Segment("sequence_number_source", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency", length=(0,3))
        ])
    ]),
    "QTY": Segment().structure([
        Segment("quantity_details", mandatory=True, min=1, max=1).structure([
            Segment("quantity_qualifier", length=(0,3), mandatory=True),
            Segment("quantity", length=(0,15), mandatory=True),
            Segment("measure_unit_qualifier", length=(0,3))
        ])
    ])
}