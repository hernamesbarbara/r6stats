#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""getleaderboards.py
"""
import sys
import os
import requests
import arrow
import numpy as np
import pandas as pd
from r6api import R6Api
from utils import r6io
try:
    import ujson as json
except ImportError:
    import json


SEEN = "seen.txt"
SEEN_PAGES = "seen_pages.json"

def _seen_set():
    try:
        seen = pd.read_csv(SEEN, usecols=['ubisoft_id'], names=['ubisoft_id'], squeeze=True)
        seen = seen.sort_values().drop_duplicates()
    except:
        seen = pd.Series([], name='ubisoft_id')
        seen.to_csv(SEEN, index=False, header=False, encoding='utf-8')
    return set(seen)

def _seen_pages():
    try:
        seen_pages = json.load(open(SEEN_PAGES, "r"))
    except:
        seen_pages = {"ranked": 0, "casual": 0, "general":0}
    return seen_pages

def _localtime():
    utc = arrow.utcnow()
    return utc.to('US/Eastern').format('YYYY-MM-DD HH:mm:ss ZZ')

def get_all_pages(r6, leaderboard, outfile):
    seen = _seen_set()
    seen_pages = _seen_pages()
    first_page = seen_pages[leaderboard]+1
    with open(SEEN, 'a') as seen_file:
        print "[{}]    Starting on page {}".format(_localtime(), first_page)    
        page = r6.leaderboards[leaderboard].GET(params={'page': first_page})
        for player in page['players']:
            if player['ubisoft_id'] not in seen:
                r6io.dump_jsonl_stream(player, outfile)
                seen.add(player['ubisoft_id'])
                seen_file.write(player['ubisoft_id']+os.linesep)
        json.dump(seen_pages, open(SEEN_PAGES, "w"))
        total_pages = page['meta']['total_pages']
        next_page = page['meta']['next_page']
        for i in xrange(next_page, total_pages+1):
            if i % 100 == 0 or i == total_pages:
                print "[{}]    {} => {} of {}".format(_localtime(), leaderboard, i, total_pages)
            try:
                page = r6.leaderboards[leaderboard].GET(params={'page': i})
                seen_pages[leaderboard] = i
                for player in page['players']:
                    try:
                        if player['ubisoft_id'] not in seen:
                            r6io.dump_jsonl_stream(player, outfile)
                            seen.add(player['ubisoft_id'])
                            seen_file.write(player['ubisoft_id']+os.linesep)
                    except Exception, err:
                        print "[{}]    {}".format(_localtime(), str(err))
                        continue
                json.dump(seen_pages, open(SEEN_PAGES, "w"))
            except Exception, err:
                print "[{}]    {}".format(_localtime(), str(err))


def main():
    outfile_name = sys.argv[1]
    r6 = R6Api()
    with open(outfile_name, "a") as outfile:
        for leaderboard in ('casual', 'ranked', 'general'):
            print "*"*80
            print leaderboard.upper()
            print "*"*80
            get_all_pages(r6, leaderboard, outfile)
    print "[{}]    Results saved to: {}".format(_localtime(), outfile_name)
    sys.exit(0)

if __name__ == '__main__':
    main()
