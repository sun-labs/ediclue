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
    ]),
    "CAV": Segment().structure([
        Segment("characteristic_value", mandatory=True, min=1, max=1).structure([
            Segment("characteristic_value-coded", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("characteristic_value", length=(0,35)),
            Segment("characteristic_value", length=(0,35)),
        ])
    ]),
    "LIN": Segment().structure([
        Segment("line_item_number", length=(0,6)),
        Segment("action_request-notification-coded", length=(0,3)),
        Segment("item_number_identification", min=0, max=1).structure([
            Segment("item_number", length=(0,35)),
            Segment("item_number_type-coded", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ]),
        Segment("sub-line_information", min=0, max=1).structure([
            Segment("sub-line_indicator-coded", length=(0,3)),
            Segment("line_item_number", length=(0,6))
        ]),
        Segment("configuration_level", length=(0,2)),
        Segment("configuration-coded", length=(0,3))
    ]),
    "MEA": Segment().structure([
        Segment("measurement_application_qualifier", length=(0,3), mandatory=True),
        Segment("measurement_details", min=0, max=1).structure([
            Segment("measurement_dimension-coded", length=(0,3)),
            Segment("measurement_significance-coded", length=(0,3)),
            Segment("measurement_attribute-coded", length=(0,3)),
            Segment("measurement_attribute", length=(0,70))
        ]),
        Segment("value-range", min=0, max=1).structure([
            Segment("measure_unit_qualifier", length=(0,3)),
            Segment("measurement_value", length=(0,18)),
            Segment("range_minimum", length=(0,18)),
            Segment("range_maximum", length=(0,18)),
            Segment("significant_digits", length=(0,2))
        ]),
        Segment("surface-layer_indicator-coded", length=(0,3))
    ]),
    "IDE": Segment().structure([
        Segment("identification_qualifier", length=(0,3), mandatory=True),
        Segment("identification_number", min=1, max=1, mandatory=True).structure([
            Segment("identity_number", length=(0,35)),
            Segment("identity_number_qualifier", length=(0,3)),
            Segment("status-coded", length=(0,3)),
        ]),
        Segment("party_identification_details", min=0, max=1).structure([
            Segment("party_id_identification", length=(0,35), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ]),
        Segment("status-coded", length=(0,3)),
        Segment("configuration_level", length=(0,2)),
        Segment("position_identification", min=0, max=1).structure([
            Segment("hierarchical_id_number", length=(0,12)),
            Segment("sequence_number", length=(0,6))
        ]),
        Segment("product_characteristic", min=0, max=1).structure([
            Segment("characteristic_identification", length=(0,17), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("characteristic", length=(0,35)),
            Segment("characteristic", length=(0,35))
        ])
    ]),
    "CCI": Segment().structure([
        Segment("property_class-coded", length=(0,3)),
        Segment("measurement_details", min=0, max=1).structure([
            Segment("measurement_dimension-coded", length=(0,3)),
            Segment("measurement_significance-coded", length=(0,3)),
            Segment("measurement_attribute-coded", length=(0,3)),
            Segment("measurement_attribute", length=(0,70))
        ]),
        Segment("product_characteristic", min=0, max=1).structure([
            Segment("characteristic_identification", length=(0,17), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("characteristic", length=(0,35)),
            Segment("characteristic", length=(0,35))
        ])
    ]),
    "STS": Segment().structure([
        Segment("status_type", min=0, max=1).structure([
            Segment("status_type-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ]),
        Segment("status_event", min=0, max=1).structure([
            Segment("status_event-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_event", length=(0,35)),
        ]),
        Segment("status_reason_1", min=0, max=1).structure([
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ]),
        Segment("status_reason_2", min=0, max=1).structure([
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ]),
        Segment("status_reason_3", min=0, max=1).structure([
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ]),
        Segment("status_reason_4", min=0, max=1).structure([
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ]),
        Segment("status_reason_5", min=0, max=1).structure([
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ]),
    ]),
    "NAD": Segment().structure([
        Segment("party_qualifier", length=(0,3), mandatory=True),
        Segment("party_identification_details", min=0, max=1).structure([
            Segment("party_id_identification", length=(0,35)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ]),
        Segment("name_and_address", min=0, max=1).structure([
            Segment("name_and_address_line_1", length=(0,35), mandatory=True),
            Segment("name_and_address_line_2", length=(0,35)),
            Segment("name_and_address_line_3", length=(0,35)),
            Segment("name_and_address_line_4", length=(0,35)),
            Segment("name_and_address_line_5", length=(0,35)),
        ]),
        Segment("party_name", min=0, max=1).structure([
            Segment("party_name_1", length=(0,35), mandatory=True),
            Segment("party_name_2", length=(0,35)),
            Segment("party_name_3", length=(0,35)),
            Segment("party_name_4", length=(0,35)),
            Segment("party_name_5", length=(0,35)),
            Segment("party_name_format-coded", length=(0,3)),
        ]),
        Segment("street", min=0, max=1).structure([
            Segment("street_and_number-po_box_1", length=(0,35), mandatory=True),
            Segment("street_and_number-po_box_2", length=(0,35)),
            Segment("street_and_number-po_box_3", length=(0,35)),
            Segment("street_and_number-po_box_4", length=(0,35)),
        ]),
        Segment("city_name", length=(0,35)),
        Segment("count_sub_entity_identification", length=(0,9)),
        Segment("postcode_identification", length=(0,9)),
        Segment("county-coded", length=(0,3))
    ]),
    "BGM": Segment().structure([
        Segment("document-message_name", min=0, max=1).structure([
            Segment("document-message_name-coded", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("document-message_name", length=(0,35)),
        ]),
        Segment("document-message_number", length=(0,35)),
        Segment("message_function-coded", length=(0,3)),
        Segment("response_type-coded", length=(0,3))
    ]),
    "MKS": Segment().structure([
        Segment("sector-subject_identification_qualifier", length=(0,3), mandatory=True),
        Segment("sales_channel_identification", min=1, max=1, mandatory=True).structure([
            Segment("sales_channel_identifier", length=(0,17), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ]),
        Segment("action_request-notification-coded", length=(0,3))
    ]),
    "UNB": Segment().structure([
        Segment("syntax_identifier", min=1, max=1, mandatory=True).structure([
            Segment("syntax_identifier", length=(4,4), mandatory=True),
            Segment("syntax_version_number", length=(1,1), mandatory=True),
        ]),
        Segment("interchange_sender", min=1, max=1, mandatory=True).structure([
            Segment("sender_identification", mandatory=True, length=(0,35)),
            Segment("partner_identification_code_qualifier", length=(0,4)),
            Segment("address_for_reverse_routing", length=(0,14))
        ]),
        Segment("interchange_recipient", min=1, max=1, mandatory=True).structure([
            Segment("recipient_identification", length=(0,35), mandatory=True),
            Segment("partner_identification_code_qualifier", length=(0,4)),
            Segment("routing_address", length=(0,14)),
        ]),
        Segment("date-time_of_preparation", min=1, max=1, mandatory=True).structure([
            Segment("date_of_preparation", length=(6,6), mandatory=True),
            Segment("time_of_preparation", length=(4,4), mandatory=True),
        ]),
        Segment("interchange_control_reference", length=(0,14), mandatory=True),
        Segment("recipients_reference-password", min=0, max=1).structure([
            Segment("recipients_reference-password", length=(0,14), mandatory=True),
            Segment("recipients_reference-password_qualifier", length=(2,2))
        ]),
        Segment("application_reference", length=(0,14)),
        Segment("processing_priority_code", length=(1,1)),
        Segment("acknowledgement_request", length=(1,1)),
        Segment("communications_agreement_id", length=(0,35)),
        Segment("test_indicator", length=(1,1))
    ])
}