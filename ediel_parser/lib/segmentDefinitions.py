from ediel_parser.lib.Segment import Segment

definitions = {
    "SEQ": Segment(tag="SEQ").structure(
        Segment("status_indicator_coded"), 
        Segment("sequence_information", min=0, max=1).structure(
            Segment("sequence_number", mandatory=True, length=(0,6)),
            Segment("sequence_number_source", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency", length=(0,3))
        )
    ),
    "QTY": Segment(tag="QTY").structure(
        Segment("quantity_details", mandatory=True, min=1, max=1).structure(
            Segment("quantity_qualifier", length=(0,3), mandatory=True),
            Segment("quantity", length=(0,15), mandatory=True),
            Segment("measure_unit_qualifier", length=(0,3))
        )
    ),
    "LOC": Segment(tag="LOC").structure(
        Segment("place-location_qualifier", mandatory=True, length=(0,3)),
        Segment("location_identification", min=0, max=1).structure(
            Segment("place-location_identification", length=(0, 25)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("place-location", length=(0,70))
        ),
        Segment("related_location_one_identification", min=0, max=1).structure(
            Segment("related_place-location_one_identification", length=(0,25)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("related_place-location_one", length=(0, 70))
        ),
        Segment("related_location_two_identification", min=0, max=1).structure(
            Segment("related_place-location_two_identification", length=(0,25)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("related_place-location_two", length=(0, 70))
        ),
        Segment("relation-coded", length=(0,3))
    ),
    "DTM": Segment(tag="DTM").structure(
        Segment("date-time-period", min=1, max=1, mandatory=True).structure(
            Segment("date-time-period_qualifier", length=(0,3), mandatory=True),
            Segment("date-time-period", length=(0,35)),
            Segment("date-time-period_format_qualifier", length=(0,3)),
        )
    ),
    "CAV": Segment(tag="CAV").structure(
        Segment("characteristic_value", mandatory=True, min=1, max=1).structure(
            Segment("characteristic_value-coded", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("characteristic_value", length=(0,35)),
            Segment("characteristic_value", length=(0,35)),
        )
    ),
    "LIN": Segment(tag="LIN").structure(
        Segment("line_item_number", length=(0,6)),
        Segment("action_request-notification-coded", length=(0,3)),
        Segment("item_number_identification", min=0, max=1).structure(
            Segment("item_number", length=(0,35)),
            Segment("item_number_type-coded", length=(0,3)),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ),
        Segment("sub-line_information", min=0, max=1).structure(
            Segment("sub-line_indicator-coded", length=(0,3)),
            Segment("line_item_number", length=(0,6))
        ),
        Segment("configuration_level", length=(0,2)),
        Segment("configuration-coded", length=(0,3))
    ),
    "MEA": Segment(tag="MEA").structure(
        Segment("measurement_application_qualifier", length=(0,3), mandatory=True),
        Segment("measurement_details", min=0, max=1).structure(
            Segment("measurement_dimension-coded", length=(0,3)),
            Segment("measurement_significance-coded", length=(0,3)),
            Segment("measurement_attribute-coded", length=(0,3)),
            Segment("measurement_attribute", length=(0,70))
        ),
        Segment("value-range", min=0, max=1).structure(
            Segment("measure_unit_qualifier", length=(0,3)),
            Segment("measurement_value", length=(0,18)),
            Segment("range_minimum", length=(0,18)),
            Segment("range_maximum", length=(0,18)),
            Segment("significant_digits", length=(0,2))
        ),
        Segment("surface-layer_indicator-coded", length=(0,3))
    ),
    "IDE": Segment(tag="IDE").structure(
        Segment("identification_qualifier", length=(0,3), mandatory=True, ref='7495'),
        Segment("identification_number", min=1, max=1, mandatory=True, ref='C206').structure(
            Segment("identity_number", length=(0,35), mandatory=True, ref='7402'),
            Segment("identity_number_qualifier", length=(0,3), ref='7405'),
            Segment("status-coded", length=(0,3), ref='4405'),
        ),
        Segment("party_identification_details", min=0, max=1, ref='C082').structure(
            Segment("party_id_identification", length=(0,35), mandatory=True, ref='3039'),
            Segment("code_list_qualifier", length=(0,3), ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055'),
        ),
        Segment("status-coded", length=(0,3), ref='4405'),
        Segment("configuration_level", length=(0,2), ref='1222'),
        Segment("position_identification", min=0, max=1, ref='C778').structure(
            Segment("hierarchical_id_number", length=(0,12), ref='7164'),
            Segment("sequence_number", length=(0,6), ref='1050')
        ),
        Segment("product_characteristic", min=0, max=1, ref='C240').structure(
            Segment("characteristic_identification", length=(0,17), mandatory=True, ref='7037'),
            Segment("code_list_qualifier", length=(0,3), ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055'),
            Segment("characteristic_1", length=(0,35), ref='7036'),
            Segment("characteristic_2", length=(0,35), ref='7036')
        )
    ),
    "CCI": Segment(tag="CCI").structure(
        Segment("property_class-coded", length=(0,3)),
        Segment("measurement_details", min=0, max=1).structure(
            Segment("measurement_dimension-coded", length=(0,3)),
            Segment("measurement_significance-coded", length=(0,3)),
            Segment("measurement_attribute-coded", length=(0,3)),
            Segment("measurement_attribute", length=(0,70))
        ),
        Segment("product_characteristic", min=0, max=1).structure(
            Segment("characteristic_identification", length=(0,17), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("characteristic", length=(0,35)),
            Segment("characteristic", length=(0,35))
        )
    ),
    "STS": Segment(tag="STS").structure(
        Segment("status_type", min=0, max=1).structure(
            Segment("status_type-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ),
        Segment("status_event", min=0, max=1).structure(
            Segment("status_event-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_event", length=(0,35)),
        ),
        Segment("status_reason_1", min=0, max=1).structure(
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ),
        Segment("status_reason_2", min=0, max=1).structure(
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ),
        Segment("status_reason_3", min=0, max=1).structure(
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ),
        Segment("status_reason_4", min=0, max=1).structure(
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ),
        Segment("status_reason_5", min=0, max=1).structure(
            Segment("status_reason-coded", length=(0,3), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
            Segment("status_reason", length=(0,35)),
        ),
    ),
    "NAD": Segment(tag="NAD").structure(
        Segment("party_qualifier", length=(0,3), mandatory=True, ref='3035'),
        Segment("party_identification_details", min=0, max=1, ref='C082').structure(
            Segment("party_id_identification", length=(0,35), ref='3039'),
            Segment("code_list_qualifier", length=(0,3), ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055'),
        ),
        Segment("name_and_address", min=0, max=1, ref='C058').structure(
            Segment("name_and_address_line_1", length=(0,35), mandatory=True, ref='3124'),
            Segment("name_and_address_line_2", length=(0,35), ref='3124'),
            Segment("name_and_address_line_3", length=(0,35), ref='3124'),
            Segment("name_and_address_line_4", length=(0,35), ref='3124'),
            Segment("name_and_address_line_5", length=(0,35), ref='3124'),
        ),
        Segment("party_name", min=0, max=1, ref='C080').structure(
            Segment("party_name_1", length=(0,35), mandatory=True, ref='3036'),
            Segment("party_name_2", length=(0,35), ref='3036'),
            Segment("party_name_3", length=(0,35), ref='3036'),
            Segment("party_name_4", length=(0,35), ref='3036'),
            Segment("party_name_5", length=(0,35), ref='3036'),
            Segment("party_name_format-coded", length=(0,3), ref='3045'),
        ),
        Segment("street", min=0, max=1, ref='C059').structure(
            Segment("street_and_number-po_box_1", length=(0,35), mandatory=True, ref='3042'),
            Segment("street_and_number-po_box_2", length=(0,35), ref='3042'),
            Segment("street_and_number-po_box_3", length=(0,35), ref='3042'),
            Segment("street_and_number-po_box_4", length=(0,35), ref='3042'),
        ),
        Segment("city_name", length=(0,35), ref='3164'),
        Segment("count_sub_entity_identification", length=(0,9), ref='3229'),
        Segment("postcode_identification", length=(0,9), ref='3251'),
        Segment("country-coded", length=(0,3), ref='3207')
    ),
    "BGM": Segment(tag="BGM").structure(
        Segment("document-message_name", min=0, max=1, ref='C002').structure(
            Segment("document-message_name-coded", length=(0,3), ref='1001'),
            Segment("code_list_qualifier", length=(0,3), ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055'),
            Segment("document-message_name", length=(0,35), ref='1000'),
        ),
        Segment("document-message_number", length=(0,35), ref='1004'),
        Segment("message_function-coded", length=(0,3), ref='1225'),
        Segment("response_type-coded", length=(0,3), ref='4343')
    ),
    "MKS": Segment(tag="MKS").structure(
        Segment("sector-subject_identification_qualifier", length=(0,3), mandatory=True),
        Segment("sales_channel_identification", min=1, max=1, mandatory=True).structure(
            Segment("sales_channel_identifier", length=(0,17), mandatory=True),
            Segment("code_list_qualifier", length=(0,3)),
            Segment("code_list_responsible_agency-coded", length=(0,3)),
        ),
        Segment("action_request-notification-coded", length=(0,3))
    ),
    "UNB": Segment(tag="UNB").structure(
        Segment("syntax_identifier", min=1, max=1, mandatory=True, ref='S001').structure(
            Segment("syntax_identifier", length=(4,4), mandatory=True, ref='0001'),
            Segment("syntax_version_number", length=(1,1), mandatory=True, ref='0002'),
        ),
        Segment("interchange_sender", min=1, max=1, mandatory=True, ref='S002').structure(
            Segment("sender_identification", mandatory=True, length=(0,35), ref='0004'),
            Segment("partner_identification_code_qualifier", length=(0,4), ref='0007'),
            Segment("address_for_reverse_routing", length=(0,14), ref='0008')
        ),
        Segment("interchange_recipient", min=1, max=1, mandatory=True, ref='S003').structure(
            Segment("recipient_identification", length=(0,35), mandatory=True, ref='0010'),
            Segment("partner_identification_code_qualifier", length=(0,4), ref='0007'),
            Segment("routing_address", length=(0,14), ref='0014'),
        ),
        Segment("date-time_of_preparation", min=1, max=1, mandatory=True, ref='S004').structure(
            Segment("date_of_preparation", length=(6,6), mandatory=True, ref='0017'),
            Segment("time_of_preparation", length=(4,4), mandatory=True, ref='0019'),
        ),
        Segment("interchange_control_reference", length=(0,14), mandatory=True, ref='0020'),
        Segment("recipients_reference-password", min=0, max=1, ref='S005').structure(
            Segment("recipients_reference-password", length=(0,14), mandatory=True, ref='0022'),
            Segment("recipients_reference-password_qualifier", length=(2,2), ref='0025')
        ),
        Segment("application_reference", length=(0,14), ref='0026'),
        Segment("processing_priority_code", length=(1,1), ref='0029'),
        Segment("acknowledgement_request", length=(1,1), ref='0031'),
        Segment("communications_agreement_id", length=(0,35), ref='0032'),
        Segment("test_indicator", length=(1,1), ref='0035')
    ),
    "UNH": Segment(tag="UNH").structure(
        Segment("message_reference_number", length=(0,14), mandatory=True, ref='0062'),
        Segment("message_identifier", mandatory=True, ref='S009').structure(
            Segment("message_type_identifier", length=(0,6), mandatory=True, ref='0065'),
            Segment("message_type_version_number", length=(0,3), mandatory=True, ref='0052'),
            Segment("message_type_release_number", length=(0,3), mandatory=True, ref='0054'),
            Segment("controlling_agency", length=(0,2), mandatory=True, ref='0051'),
            Segment("association_assigned_code", length=(0,6), ref='0057')
        ),
        Segment("common_access_reference", length=(0,35), ref='0068'),
        Segment("status_of_the_transfer", ref='S010').structure(
            Segment("sequence_message_transfer_number", length=(0,2), mandatory=True, ref='0070'),
            Segment("first-last_sequence_message_transfer_indication", length=(1,1), ref='0073')
        )
    ),
    "UNT": Segment(tag="UNT").structure(
        Segment("number_of_segments_in_a_message", length=(0,6), mandatory=True),
        Segment("message_reference_number", length=(0,14), mandatory=True)
    ),
    "UNZ": Segment(tag="UNZ").structure(
        Segment("interchange_control_count", length=(0,6), mandatory=True, ref='0036'),
        Segment("interchange_control_reference", length=(0,14), mandatory=True, ref='0020'),
    ),
     "UNA": Segment(tag="UNA").structure(
        Segment("service_string_advice", value=":+.? '")
    ),
    "CNT": Segment(tag="CNT").structure(
        Segment("control", max=1, min=1, mandatory=True).structure(
            Segment("control_qualifier", length=(0,3), mandatory=True),
            Segment("control_value", length=(0,18), mandatory=True),
            Segment("measure_unit_qualifier", length=(0,3))
        )
    ),
    "RFF": Segment(tag="RFF").structure(
        Segment("reference", max=1, min=1, mandatory=True, ref='C506').structure(
            Segment("reference_qualifier", length=(0,3), mandatory=True, ref='1153'),
            Segment("reference_number", length=(0,35), ref='1154'),
            Segment("line_number", length=(0,6), ref='1156'),
            Segment("reference_version_number", length=(0,35), ref='4000')
        )
    ),
    "ERC": Segment(tag="ERC").structure(
        Segment("application_error_detail", min=1, max=1, mandatory=True, ref='C901').structure(
            Segment("application_error_identification", mandatory=True, length=(0,8), ref='9321'),
            Segment("code_list_qualifier", length=(0,3), ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055')
        )
    ),
    "FTX": Segment(tag="FTX").structure(
        Segment("text_subject_qualifier", mandatory=True, ref='4451'),
        Segment("text_function-coded", ref='4453'),
        Segment("text_reference", ref='C107').structure(
            Segment("free_text-coded", mandatory=True, ref='4441'),
            Segment("code_list_qualifier", ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055')
        ),
        Segment("text_literal", ref='C108').structure(
            Segment("free_text", mandatory=True, ref='4440'),
            Segment("free_text_2", ref='4440'),
            Segment("free_text_3", ref='4440'),
            Segment("free_text_4", ref='4440'),
            Segment("free_text_5", ref='4440'),
        ),
        Segment("language-coded", ref='3453')
    ),
    "COM": Segment(tag="COM").structure(
        Segment("communication_contact", mandatory=True, ref='C076').structure(
            Segment("communication_number", mandatory=True, ref='3148'),
            Segment("communcation_channel_qualifier", mandatory=True, ref='3155')
        )
    ),
    "CTA": Segment(tag="CTA").structure(
        Segment("contact_function-coded", ref='3139'),
        Segment("department_or_employee_details", ref='C056').structure(
            Segment("department_or_employee_identification", ref='3413'),
            Segment("department_or_employee", ref='3412')
        )
    ),
    "DOC": Segment(tag="DOC").structure(
        Segment("document-message_name", ref='C002', mandatory=True).structure(
            Segment("document-message_name-coded", ref='1001'),
            Segment("code_list_qualifier", ref='1131'),
            Segment("code_list_responsible_agency-coded", length=(0,3), ref='3055'),
            Segment("document-message_name", ref='1000')
        ),
        Segment("document-message_details", ref='C503').structure(
            Segment("document-message_number", ref='1004'),
            Segment("document-message_status-coded", ref='1373'),
            Segment("document-message_source", ref='1366'),
            Segment("language-coded", ref='3453')
        ),
        Segment('communication_channel_identifier-coded', ref='3153'),
        Segment("number_of_copies_of_document_required", ref='1220'),
        Segment("number_of_originals_of_document_required", ref='1218')
    )
}