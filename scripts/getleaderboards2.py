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
import glob
try:
    import ujson as json
except ImportError:
    import json

def get_page(i):
    try: 
        players = r6.leaderboards[leaderboard].GET(params={'page': i})['players']
        outfile = f'/tmp/{leaderboard}-page-{i:03}.jsonl'
        with open(outfile, 'a') as o:
            for player in players:
                r6io.dump_jsonl_stream(player, o)
        return outfile
    except:
        return ''

def coalesce_pages(infiles_list, outfile):
    for infile in infiles_list:
        try:
            r6io.read_nested_write_flat(infile, outfile)
            print(f'{infile}: success')
        except:
            print(f'{infile}: error')
            continue

if __name__ == '__main__':
    r6 = R6Api()
    for leaderboard in ('casual', 'ranked', 'general'):
        start_page = 1
        end_page = r6.leaderboards[leaderboard].GET(params={'page': 1})['meta']['total_pages']

        pool = multiprocessing.Pool()
        res = pool.map_async(get_page, range(start_page,end_page+1))
        pool.close()
        pool.join()

        coalesce_pages(res.get(), "data/players.jsonl")


