#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""newgetleaderboards.py
"""
import sys
import os
import json
import requests
import collections
from r6api import R6Api
from bandit import Bandit

def dump_jsonl(data, outfile):
    with open(outfile, 'a') as outfile:
        json.dump(data, outfile)
        outfile.write(os.linesep)

def get_all_pages(leaderboard, outfile):
    page = r6.leaderboards[leaderboard].GET(params={'page': 1})
    for player in page['players']:
        dump_jsonl(player, outfile)
    
    total_pages = page['meta']['total_pages']
    next_page = page['meta']['next_page']

    for i in xrange(next_page, total_pages+1):
        if i % 100 == 0 or i == total_pages:
            print "{} => {} of {}".format(leaderboard, i, total_pages)
        try:
            page = r6.leaderboards[leaderboard].GET(params={'page': i})
            for player in page['players']:
                try:
                    dump_jsonl(player, outfile)
                except Exception, err:
                    print str(err)
                    continue
        except Exception, err:
            print str(err)

def main():
    for leaderboard in ('casual', 'ranked', 'general'):
        print "*"*80
        print leaderboard.upper()
        print "*"*80
        get_all_pages(leaderboard, bandit.output_dir+'leaderboard-pages.jsonl')
    sys.exit(0)

if __name__ == '__main__':
    r6 = R6Api()
    bandit = Bandit()
    main()
