from flask import Flask, request, jsonify
import json
from cores.utils import parse_search_request_data, pre_output_search_api, prep_data
from cores.exactly_search import exactly_search
from cores.similar_search import similar_search
from cores.merge_file import matching
from cores.clean_data import clean_data


import pandas as pd
import numpy as np
from time import time
from multiprocessing import Pool, cpu_count


app = Flask(__name__)


@app.route("/search", methods=['POST'])
def search():
    # load data from request's body
    data = request.data
    data = json.loads(data)
    exactly = request.args.get('exactly')
    print(data)
    print('EXACTLY', exactly)
    _sample = parse_search_request_data(data)
    print(_sample)

    if exactly.lower() == "true":
        result = exactly_search(df, _sample)
    else:
        result = similar_search(df, _sample, num=100)
        result = pre_output_search_api(result)
        result = result.to_dict("records")
    return jsonify(result)


@app.route("/clean", methods=['POST'])
def clean():
    print("Getting request")
    data = request.data
    data = json.loads(data)

    df = pd.DataFrame(data['data'])
    threshold = float(data['threshold'])
    res = clean_data(df, threshold)
    resp = jsonify(res)
    return resp


@app.route('/merge', methods=['POST'])
def merge():
    data = request.data
    data = json.loads(data)
    base_df = pd.DataFrame(data['base'])
    candidate_df = pd.DataFrame(data['candidate'])
    print("BASE", base_df.head())
    print("CANDIDATE", candidate_df.head())

    threshold = float(data['threshold'])
    res = matching(base_df, candidate_df, threshold)
    return jsonify(res.to_dict('records'))


if __name__ == '__main__':
    start = time()
    # df = load_data('./data/fake_data.csv')
    df = prep_data('./data/fake_data_1e5.csv')
    print('Loaded {} samples in {:.1f}s'.format(len(df), time() - start))

    app.run(host='0.0.0.0', port=8002, debug=True)
