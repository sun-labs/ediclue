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
    ]),
    "LOC": Segment().structure([
        Segment("place-location_qualifier", mandatory=True, length=(0,3)),
        Segment("location_identification", min=0, max=1).structure([
            Segment("place-location_identification", length=(0, 25)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("place-location", length=(0,70))
        ]),
        Segment("related_location_one_identification", min=0, max=1).structure([
            Segment("related_place-location_one_identification", length=(0,25)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("related_place-location_one", length=(0, 70))
        ]),
        Segment("related_location_two_identification", min=0, max=1).structure([
            Segment("related_place-location_two_identification", length=(0,25)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("related_place-location_two", length=(0, 70))
        ]),
        Segment("relation-coded", length=(0,3))
    ]),
    "DTM": Segment().structure([
        Segment("date-time-period", min=1, max=1, mandatory=True).structure([
            Segment("date-time-period_qualifier", length=(0,3), mandatory=True),
            Segment("date-time-period", length=(0,35)),
            Segment("date-time-period_format_qualifier", length=(0,3)),
        ])
    ])
}