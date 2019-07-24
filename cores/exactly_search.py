from cores.utils import pre_output_search_api


def exactly_search(df, filter):
    result = df.copy()
    result['SCORE'] = 1
    for k, v in filter.items():
        if v != None:
            result = result[result[k] == v]

    if len(result) == 0:
        res = [{
            "full_name": "",
            "gender": "",
            "id_number": "",
            "registration_province": "",
            "registration_district": "",
            "registration_commute": "",
            "dob": "",
            'SCORE': ""
        }]
    else:
        res = pre_output_search_api(result)
        res = res.to_dict('records')
    return res
