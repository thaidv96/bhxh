import pandas as pd
# General Utils


def load_data(path):
    df = pd.read_csv(path)
    df = df[['HO_TEN', 'GIOI_TINH', 'NGAY_SINH', 'MA_TINH_KS',
             'MA_HUYEN_KS', 'MA_XA_KS', 'SO_CMTND']]
    df.drop_duplicates(inplace=True)
    df.sort_values('HO_TEN', inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['GIOI_TINH'] = df['GIOI_TINH'].astype(str)
    df['NGAY_SINH'] = df['NGAY_SINH'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].apply(
        lambda x: '0'*(5-len(str(x))) + str(x))
    df['MA_XA_KS'] = df['MA_XA_KS'].astype(str)
    df['SO_CMTND'].fillna('------------', inplace=True)
    df['SO_CMTND'] = df['SO_CMTND'].astype(str)
    return df


def prep_data(path):
    df = load_data(path)
    df = split_name(df)
    df = split_db(df)
    return df


def split_name(df):
    name = [item.split() for item in df['HO_TEN']]
    df.drop(columns=['HO_TEN'], inplace=True)
    last_name = [item.pop(0) for item in name]
    first_name = [item.pop() for item in name]
    middle_name = [' '.join(item) for item in name]
    df['HO'] = last_name
    df['DEM'] = middle_name
    df['TEN'] = first_name
    return df


def split_db(df):
    db = df['NGAY_SINH']
    df.drop(columns=['NGAY_SINH'], inplace=True)
    df['NGAY'] = [item[6:] for item in db]
    df['THANG'] = [item[4:6] for item in db]
    df['NAM'] = [item[:4] for item in db]
    return df

# Utils for search feature:


def parse_search_request_data(data):
    res = {}
    name_parts = data['full_name'].strip().split()
    res['HO'] = name_parts[0]
    res['TEN'] = name_parts[-1]
    res['DEM'] = ' '.join(name_parts[1:-1])
    res['GIOI_TINH'] = data['gender']
    try:
        dob = data['dob'].split('-')
        res['NGAY'] = dob[0]
        res['THANG'] = str(int(dob[1]))
        res['NAM'] = dob[2]
    except:
        res['NGAY'] = None
        res['THANG'] = None
        res['NAM'] = None
    res['MA_TINH_KS'] = data['registration_province']
    res['MA_HUYEN_KS'] = data['registration_district']
    res['MA_XA_KS'] = data['registration_commute']
    res['SO_CMTND'] = data['id_number']
    return res


def pre_output_search_api(result):
    columns = ['full_name', 'gender', 'dob', 'registration_province',
               'registration_district', 'registration_commute', 'id_number']
    data = pd.DataFrame(columns=columns)
    data['full_name'] = result.HO + ' ' + result.DEM + ' ' + result.TEN
    data['gender'] = result['GIOI_TINH']
    data['id_number'] = result['SO_CMTND']
    data['registration_province'] = result['MA_TINH_KS']
    data['registration_district'] = result['MA_HUYEN_KS']
    data['registration_commute'] = result['MA_XA_KS']
    data['dob'] = result.NGAY + "-" + result.THANG + '-' + result.NAM
    data['score'] = result['SCORE']
    return data

# Utils for clean feature


def pre_output_clean(df, duplicate=False):
    df['HO_TEN'] = df.HO + ' ' + df.DEM + ' ' + df.TEN
    df['NGAY_SINH'] = df.NGAY + '-' + df.THANG + '-' + df.NAM
    col_name = ['HO_TEN', 'GIOI_TINH', 'NGAY_SINH', 'MA_XA_KS',
                'MA_HUYEN_KS', 'MA_TINH_KS', "SO_CMTND"]
    if duplicate:
        col_name.append('duplicate_record')
    df = df[col_name]
    return df


# Utils for Merge feature
# Utils for merge function
def prep_inp_df1(df):
    df = df[['HO_TEN', 'GIOI_TINH', 'NGAY_SINH', 'MA_TINH_KS',
             'MA_HUYEN_KS', 'MA_XA_KS', 'SO_CMTND', 'MA_BHYT']]
    df.drop_duplicates(inplace=True)
    df['GIOI_TINH'] = df['GIOI_TINH'].astype(str)
    df['NGAY_SINH'] = df['NGAY_SINH'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].apply(
        lambda x: '0'*(5-len(str(x))) + str(x))
    df['MA_XA_KS'] = df['MA_XA_KS'].astype(str)
    df['SO_CMTND'].fillna('------------', inplace=True)
    df['SO_CMTND'] = df['SO_CMTND'].astype(str)
    df = split_name(df)
    df = split_db(df)
    return df


def prep_output_df1(df):
    df['HO_TEN'] = df.HO + ' ' + df.DEM + ' ' + df.TEN
    df['NGAY_SINH'] = df.NGAY + '-' + df.THANG + '-' + df.NAM
    df = df[['HO_TEN', 'GIOI_TINH', 'NGAY_SINH', 'MA_XA_KS',
             'MA_HUYEN_KS', 'MA_TINH_KS', "SO_CMTND", 'MA_BHYT']]
    df.columns = [f'base_{i}' for i in df.columns]
    return df


def prep_inp_df2(df):
    df = df[['HO', 'DEM', 'TEN', 'GIOI_TINH', 'NGAY_SINH',
             'NOI_KHAI_SINH', 'SO_CMTND', 'MA_CD']]
    df['MA_XA_KS'] = df['NOI_KHAI_SINH'].str.split("-").str[0]
    df['MA_HUYEN_KS'] = df['NOI_KHAI_SINH'].str.split("-").str[1]
    df['MA_TINH_KS'] = df['NOI_KHAI_SINH'].str.split("-").str[2]
    df.drop_duplicates(inplace=True)
    df['GIOI_TINH'] = df['GIOI_TINH'].astype(str)
    df['NGAY_SINH'] = df['NGAY_SINH'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].apply(
        lambda x: '0'*(5-len(str(x))) + str(x))
    df['MA_XA_KS'] = df['MA_XA_KS'].astype(str)
    df['SO_CMTND'].fillna('------------', inplace=True)
    df['SO_CMTND'] = df['SO_CMTND'].astype(str)
    df = split_db(df)
    return df


def prep_output_df2(df):
    df['NGAY_SINH'] = df.NGAY + '-' + df.THANG + '-' + df.NAM
    df = df[['HO', 'DEM', 'TEN', 'GIOI_TINH', 'NGAY_SINH',
             'NOI_KHAI_SINH', 'SO_CMTND', 'MA_CD', 'matching_idx', 'SCORE']]
    df.columns = [f'candidate_{i}' for i in df.columns]
    return df
