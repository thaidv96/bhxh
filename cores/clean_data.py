import sys
import pandas as pd
from datetime import datetime

from cores.utils import prep_data, pre_output_clean
from cores.similar_search import similar_search

# threshold = 0.9
# path = './data/data_temp_vss.csv'


def clean_data(df, threshold):
    df.to_csv("./data/uncleaned.csv")
    path = "./data/uncleaned.csv"
    df = prep_data(path)
    records = df.to_dict('records')
    print("Number of records:", len(records))
    distinct_records = []
    duplicate_records = []
    for record in records:
        if len(distinct_records) == 0:
            distinct_records.append(record)
        else:
            df = pd.DataFrame(distinct_records)
            most_similar_df = similar_search(df, record, threshold)
            if most_similar_df.shape[0] == 0:
                distinct_records.append(record)
            else:
                duplicate_record = get_duplicate_record(most_similar_df)
                record['duplicate_record'] = duplicate_record
                duplicate_records.append(record)
    result_df = pd.DataFrame(distinct_records)
    result_df = pre_output_clean(result_df)
    if len(duplicate_records) > 0:
        duplicate_df = pd.DataFrame(duplicate_records)
        duplicate_df = pre_output_clean(duplicate_df, duplicate=True)
        duplicate_df = duplicate_df.to_dict('record')
        duplicate_df = sorted(
            duplicate_df, key=lambda x: x['duplicate_record']['SCORE'], reverse=True)
    else:
        duplicate_df = None
    return {'clean': result_df.to_dict('record'),
            'duplicate': duplicate_df
            }


def get_duplicate_record(most_similar_df):
    duplicate_record = sorted(most_similar_df.to_dict(
        "records"), key=lambda x: x['SCORE'], reverse=True)[-1]
    duplicate_record['HO_TEN'] = duplicate_record['HO'] + \
        ' ' + duplicate_record['DEM'] + \
        ' ' + duplicate_record['TEN']
    duplicate_record['NGAY_SINH'] = duplicate_record['NGAY'] + \
        "-" + duplicate_record['THANG'] + \
        "-"+duplicate_record['NAM']
    for ii in ['HO', 'DEM', 'TEN', 'NGAY', 'THANG', 'NAM']:
        del duplicate_record[ii]
    return duplicate_record
