#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""getleaderboards2.py
"""
import sys
import os
import multiprocessing
import requests
import arrow
import numpy as np
import pandas as pd
from r6api.r6api import R6Api
from utils import r6io
try:
    import ujson as json
except ImportError:
    import json

def get_page(i):
    try: 
        return r6.leaderboards['casual'].GET(params={'page': i})['players']
    except:
        return []

if __name__ == '__main__':
    r6 = R6Api()
    
    start_page = 1
    end_page = 5
    leaderboard = 'casual'

    pool = multiprocessing.Pool()
    res = pool.map_async(get_page, range(start_page,end_page+1))
    pool.close()
    pool.join()

    with open('data/leaderboard-pages2.jsonl', 'a') as outfile:
        for i, record in enumerate(sum(res.get(), [])):
            if i % 100 == 0:
                print('saved record: {}'.format(i))
            try:
                json.dump(record, outfile)
                outfile.write(os.linesep)
            except:
                pass
