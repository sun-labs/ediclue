def get_tag(ediel_result_list, tag):
    for ediel_result in ediel_result_list:
        if ediel_result.tag == tag:
            return ediel_result