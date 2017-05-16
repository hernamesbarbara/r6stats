#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""getleaderboards.py
"""
import sys
import os
import requests
import arrow
import collections
from r6api import R6Api
try:
    import ujson as json
except ImportError:
    import json
from utils import r6io

SEEN = "seen.txt"
SEEN_PAGES = "seen_pages.json"

def _localtime():
    utc = arrow.utcnow()
    return utc.to('US/Eastern').format('YYYY-MM-DD HH:mm:ss ZZ')

def get_all_pages(r6, leaderboard, outfile):
    try:
        seen = set(line.strip() for line in open(SEEN, 'r').readline())
    except:
        seen = set()

    try:
        seen_pages = json.load(open(SEEN_PAGES, "r"))
    except:
        seen_pages = {"ranked": 1, "casual": 1, "general":1}
    
    with open(SEEN, 'a') as seen_file:
        first_page = seen_pages[leaderboard]
        print "starting on page {}".format(first_page)
        page = r6.leaderboards[leaderboard].GET(params={'page': first_page})
        for player in page['players']:
            if player['ubisoft_id'] not in seen:
                r6io.dump_jsonl_stream(player, outfile)
                seen.add(player['ubisoft_id'])
                seen_file.write(player['ubisoft_id']+os.linesep)
        total_pages = page['meta']['total_pages']
        next_page = page['meta']['next_page']
        for i in xrange(next_page, total_pages+1):
            if i % 100 == 0 or i == total_pages:
                print "[{}]    {} => {} of {}".format(_localtime(), leaderboard, i, total_pages)
            try:
                page = r6.leaderboards[leaderboard].GET(params={'page': i})
                seen_pages[leaderboard] = i
                json.dump(seen_pages, open(SEEN_PAGES, "w"))
                for player in page['players']:
                    try:
                        if player['ubisoft_id'] not in seen:
                            r6io.dump_jsonl_stream(player, outfile)
                            seen.add(player['ubisoft_id'])
                            seen_file.write(player['ubisoft_id']+os.linesep)
                    except Exception, err:
                        print str(err)
                        continue
            except Exception, err:
                print str(err)


def main():
    outfile_name = sys.argv[1]
    # Wall time: 6h 50min 25s
    r6 = R6Api()
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
