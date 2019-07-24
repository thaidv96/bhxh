import pandas as pd
import numpy as np
from functools import partial
from cores.utils import prep_inp_df1, prep_output_df1, prep_inp_df2, prep_output_df2
from cores.similar_search import similar_search


def get_most_similar(record, df, threshold):
    most_similar = similar_search(df, record, threshold)
    if len(most_similar) == 0:
        return None, None
    else:
        idx = most_similar[most_similar.SCORE ==
                           most_similar.SCORE.max()].index[0]
        score = most_similar.SCORE.max()
        return idx, score


def matching(df1, df2, threshold):
    df1 = df1.astype(str)
    df2 = df2.astype(str)
    # base: df1, candidate: df2
    df1 = prep_inp_df1(df1)
    df2 = prep_inp_df2(df2)
    customize_get_most_similar = partial(
        get_most_similar, df=df1, threshold=threshold)

    df2['matching_idx'], df2['SCORE'] = np.vectorize(
        customize_get_most_similar)(df2.to_dict('records'))

    df1 = prep_output_df1(df1)
    df2 = prep_output_df2(df2)
    res = pd.merge(df2, df1, how='left',
                   left_on='candidate_matching_idx', right_index=True)
    return res
