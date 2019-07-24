import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import textdistance as tdc
from time import time


def load_data(path):
    df = pd.read_csv(path)
    df = df[['HO', 'DEM', 'TEN', 'GIOI_TINH', 'NGAY', 'THANG', 'NAM', 'MA_TINH_KS',
             'MA_HUYEN_KS', 'MA_XA_KS', 'SO_CMTND', 'LABEL']]
#    df.drop_duplicates(inplace=True)
#    df.sort_values('HO', inplace=True)
#    df.reset_index(drop=True, inplace=True)
    
    df['HO'] = df['HO'].astype(str)
    df['DEM'] = df['DEM'].astype(str)
    df['TEN'] = df['TEN'].astype(str)
    df['GIOI_TINH'] = df['GIOI_TINH'].astype(str)
    df['NGAY'] = df['NGAY'].astype(str)
    df['THANG'] = df['THANG'].astype(str)
    df['NAM'] = df['NAM'].astype(str)
    df['MA_TINH_KS'] = df['MA_TINH_KS'].astype(str)
    df['MA_HUYEN_KS'] = df['MA_HUYEN_KS'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].apply(lambda x: '0'*(5-len(str(x))) + str(x))
    df['SO_CMTND'] = df['SO_CMTND'].astype(str)
    df['LABEL'] = df['LABEL'].astype(str)
    df['LABEL'] = df['LABEL'].apply(lambda x: '0'*(11-len(str(x))) + str(x))
    return df

def lcs_euclidean(df, sample, num=15):
    records = []
    for idx, row in df.iterrows():
        ho = SequenceMatcher(None, sample['HO'], row['HO']).get_matching_blocks()
        dem = SequenceMatcher(None, sample['DEM'], row['DEM']).get_matching_blocks()
        ten = SequenceMatcher(None, sample['TEN'], row['TEN']).get_matching_blocks()
        gioi_tinh = SequenceMatcher(None, sample['GIOI_TINH'], row['GIOI_TINH']).get_matching_blocks()
        ngay = SequenceMatcher(None, sample['NGAY'], row['NGAY']).get_matching_blocks()
        thang = SequenceMatcher(None, sample['THANG'], row['THANG']).get_matching_blocks()
        nam = SequenceMatcher(None, sample['NAM'], row['NAM']).get_matching_blocks()
        ma_tinh_ks = SequenceMatcher(None, sample['MA_TINH_KS'], row['MA_TINH_KS']).get_matching_blocks()
        ma_huyen_ks = SequenceMatcher(None, sample['MA_HUYEN_KS'], row['MA_HUYEN_KS']).get_matching_blocks()
        ma_xa_ks = SequenceMatcher(None, sample['MA_XA_KS'], row['MA_XA_KS']).get_matching_blocks()
        so_cmtnd = SequenceMatcher(None, sample['SO_CMTND'], row['SO_CMTND']).get_matching_blocks()
        
        gia_tri = []
        gia_tri.append(np.sum([item.size for item in ho if item.size >= 1]) / len(sample['HO']))
        gia_tri.append(np.sum([item.size for item in dem if item.size >= 2]) / len(sample['DEM']))
        gia_tri.append(np.sum([item.size for item in ten if item.size >= 2]) / len(sample['TEN']))
        gia_tri.append(np.sum([item.size for item in gioi_tinh if item.size >= 1]) / len(sample['GIOI_TINH']))
        gia_tri.append(np.sum([item.size for item in ngay if item.size >= 1]) / len(sample['NGAY']))
        gia_tri.append(np.sum([item.size for item in thang if item.size >= 1]) / len(sample['THANG']))
        gia_tri.append(np.sum([item.size for item in nam if item.size >= 3]) / len(sample['NAM']))
        gia_tri.append(np.sum([item.size for item in ma_tinh_ks if item.size >= 3]) / len(sample['MA_TINH_KS']))
        gia_tri.append(np.sum([item.size for item in ma_huyen_ks if item.size >= 3]) / len(sample['MA_HUYEN_KS']))
        gia_tri.append(np.sum([item.size for item in ma_xa_ks if item.size >= 3]) / len(sample['MA_XA_KS']))
        gia_tri.append(np.sum([item.size for item in so_cmtnd if item.size >= 5]) / len(sample['SO_CMTND']))
        records.append(gia_tri)
    
    vectors = np.asarray(records)
    score = np.linalg.norm(vectors, axis=1)
    score_sorted = np.flip(np.sort(score)[-num:], axis=0)
    indices = np.flip(np.argsort(score)[-num:], axis=0)
    most_similar = df.loc[indices, :]
    most_similar['SCORE'] = score_sorted
    return most_similar

def jaro_euclidean(df, sample, num=15):
    vectors = np.zeros((len(df), len(sample)))
    for idx, row in df.iterrows():
        vectors[idx] = np.asarray([tdc.jaro(row[key], sample[key]) for key in sample.keys()])
    
    score = np.linalg.norm(vectors, axis=1) / np.sqrt(11)
    score_sorted = np.flip(np.sort(score)[-num:], axis=0)
    indices = np.flip(np.argsort(score)[-num:], axis=0)
    most_similar = df.loc[indices, :]
    most_similar['SCORE'] = score_sorted
    return most_similar

def jaccard_euclidean(df, sample, num=15):
    vectors = np.zeros((len(df), len(sample)))
    start = time()
    checkpoint = time()
    for idx, row in df.iterrows():
        if idx % 10000 == 0:
            print('Extracting sample ' + str(idx) + '/' + str(len(df)))
            print('Time pass: ' + '{:.1f}'.format(time()-start) + '. Time left: ' + 
                  '{:.1f}'.format((time()-checkpoint) * (len(df)-idx) / 10000))
            checkpoint = time()
        vectors[idx] = np.asarray([tdc.jaccard(row[key], sample[key]) for key in sample.keys()])
    
    param1 = np.asarray([7/66, 5/66, 11/66, 1/66, 3/66, 4/66, 
                         6/66, 8/66, 9/66, 10/66, 2/66])
    param2 = np.asarray([10/64, 5/64, 16/64, 1/64, 3/64, 4/64, 
                         6/64, 3/64, 4/64, 10/64, 2/64])
    
    vectors = vectors * param1
    score = np.linalg.norm(vectors, axis=1) / np.linalg.norm(param1)
#    score /= np.max(score)
    score_sorted = np.flip(np.sort(score)[-num:], axis=0)
    indices = np.flip(np.argsort(score)[-num:], axis=0)
    most_similar = df.loc[indices, :]
    most_similar['SCORE'] = score_sorted
    return most_similar

def run_script(df, sample, num=100):
    result = []
#    result.append(lcs_euclidean(df, sample, num))
#    result.append(jaro_euclidean(df, sample, num))
    result.append(jaccard_euclidean(df, sample, num))
#    result.append(tversky_euclidean(df, sample, num))
    return result
    

if __name__ == '__main__':
    start = time()
#    path = './data/data_temp_vss.csv'
#    path = './data/fake_data_temp_vss.csv'
    path = './data/fake_data.csv'
    df = load_data(path)
    
    sample_full = {'HO': 'Dương', 'DEM': 'Thị', 'TEN': 'Thắm', 'GIOI_TINH': '1',
                   'NGAY': '10', 'THANG': '1', 'NAM': '1963',
                   'MA_TINH_KS': '26TTT', 'MA_HUYEN_KS': '251HH',
                   'MA_XA_KS': '09025','SO_CMTND': '026063000011'}
    
    script_full = run_script(df, sample_full, 100)
    script_full[0].to_csv('output/output.csv')
    
    print('Running time: {:.1f} s'.format(time() - start))
    
