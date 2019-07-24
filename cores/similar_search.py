import pandas as pd
import numpy as np
import textdistance as tdc
from time import time
from multiprocessing import Pool, cpu_count

jaccard = np.vectorize(tdc.jaccard)


def jaccard_block(block):
    df, sample = block
    return jaccard(df, sample)


def similar_search(df, sample, threshold=None, num=None):
    cores = cpu_count()
    sample_keys = ['HO', 'DEM', 'TEN', 'GIOI_TINH', 'NGAY', 'THANG',
                   'NAM', 'MA_TINH_KS', 'MA_HUYEN_KS', 'MA_XA_KS', 'SO_CMTND']

    # Rule-based
    if '-' not in sample['SO_CMTND'] and sample['SO_CMTND'] in set(df.SO_CMTND):
        most_similar = df[df.SO_CMTND == sample['SO_CMTND']]
        most_similar['SCORE'] = 1
        return most_similar
    # Model based
    if df.shape[0] > cores+1:
        df_split = np.array_split(df[sample_keys].values.astype(str), cores)
        samples = [[sample[i] for i in sample_keys]] * cores
        blocks = zip(df_split, samples)
        pool = Pool(cores)
        vectors = np.concatenate(pool.map(jaccard_block, blocks))
        pool.close()
        pool.join()
    else:
        vectors = jaccard(df[sample_keys].values, [sample[i]
                                                   for i in sample_keys])
    # Custom weights
    param1 = np.asarray([7/66, 1/66, 11/66, 5/66, 2/66, 4/66,
                         6/66, 10/66, 9/66, 3/66, 8/66])

    vectors = vectors * param1
    score = np.linalg.norm(vectors, axis=1) / np.linalg.norm(param1)
    most_similar = df.copy()
    most_similar['SCORE'] = score
    if threshold != None:
        most_similar = most_similar[score > threshold].sort_values(
            by='SCORE', ascending=False)
    if num != None:
        most_similar = most_similar.sort_values(
            by="SCORE", ascending=False).iloc[:num]
    return most_similar
