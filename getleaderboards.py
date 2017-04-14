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
        if isinstance(data, dict):
            json.dump(data, outfile)
            outfile.write(os.linesep)
            return
        else:
            for doc in data:
                json.dump(doc, outfile)
                outfile.write(os.linesep)
    return True

def get_all_pages(leaderboard, outfile):

    page = r6.leaderboards[leaderboard].GET(params={'page': 1})
    dump_jsonl(page, outfile)
    
    total_pages = page['meta']['total_pages']
    next_page = page['meta']['next_page']

    for i in xrange(next_page, total_pages+1):
        if i % 10 == 0 or i == total_pages:
            print "{} => {} of {}".format(leaderboard, i, total_pages)
        try:
            try:
                page = r6.leaderboards[leaderboard].GET(params={'page': i})
            except Exception, err:
                print str(err)
            dump_jsonl(page, outfile)
        except Exception, err:
            page = None
    return True

def main():
    for leaderboard in ('casual', 'ranked', 'general'):
        print "*"*80
        print leaderboard.upper()
        print "*"*80
        get_all_pages(leaderboard, bandit.output_dir+'-{}-pages.jsonl')
    sys.exit(0)

if __name__ == '__main__':
    r6 = R6Api()
    bandit = Bandit()
    main()
