#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""getleaderboards.py
"""
import sys
import os
import requests
import collections
from r6api import R6Api
try:
    import ujson as json
except ImportError:
    import json

from utils import r6io

def get_all_pages(r6, leaderboard, outfile):
    page = r6.leaderboards[leaderboard].GET(params={'page': 1})
    for player in page['players']:
        r6io.dump_jsonl_stream(player, outfile)
    
    total_pages = page['meta']['total_pages']
    next_page = page['meta']['next_page']

    for i in xrange(next_page, total_pages+1):
        if i % 100 == 0 or i == total_pages:
            print "{} => {} of {}".format(leaderboard, i, total_pages)
        try:
            page = r6.leaderboards[leaderboard].GET(params={'page': i})
            for player in page['players']:
                try:
                    r6io.dump_jsonl_stream(player, outfile)
                except Exception, err:
                    print str(err)
                    continue
        except Exception, err:
            print str(err)

def main():
    # Wall time: 6h 50min 25s
    r6 = R6Api()
    outfile_name = sys.argv[1]
    with open(outfile_name, "a") as outfile:
        for leaderboard in ('casual', 'ranked', 'general'):
            print "*"*80
            print leaderboard.upper()
            print "*"*80
            get_all_pages(r6, leaderboard, outfile)
    print "results written to: {}".format(outfile_name)
    sys.exit(0)

if __name__ == '__main__':
    main()
