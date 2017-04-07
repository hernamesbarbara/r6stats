#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""getplayers.py
"""
import sys
import os
import json
import requests
import collections

def get_url(leaderboard):
    base = "https://api.r6stats.com"
    version = '/api/v1'
    endpoint =  '/leaderboards/{}'.format(leaderboard)
    return "{base}{version}{endpoint}".format(base=base, version=version, endpoint=endpoint)

def get_page(url, page=1):
    return requests.get(url, params={'page': page})

def write_json_to_file(data, outfile):
    print "writing {}".format(outfile)
    with open(outfile, "w") as o:
        json.dump(pages, o, encoding='utf8', indent=2)
    return

def write_text_to_file(data, outfile):
    print "writing {}".format(outfile)
    with open(outfile, "w") as o:
        o.write(os.linesep.join(data))
    return

def append_text_to_file(data, outfile):
    print "writing {}".format(outfile)
    with open(outfile, "a") as o:
        o.write(data)
        o.write(os.linesep)
    return

def get_all_pages(leaderboard):
    pages = []
    errors = []
    url = get_url(leaderboard)
    r = get_page(url)
    page = r.json()
    pages.append(page)
    meta = page['meta']
    next_page = meta['next_page']
    total_pages = meta['total_pages']
    for i in xrange(next_page, total_pages+1):
        if i % 10 == 0 or i == total_pages:
            print "{} => {} of {}".format(leaderboard, i, total_pages)
        try:
            r = get_page(url, page=i)
            page = r.json()
            page['meta'][u'url'] = r.url
            pages.append(page)
        except Exception, err:
            r = requests.Request('GET', url, params={'page':i}).prepare()
            page = None
            errors.append(r.url)
    return pages, errors



for leaderboard in ('casual', 'ranked', 'general'):
    print "*"*80
    print leaderboard.upper()
    print "*"*80
    pages, errors = get_all_pages(leaderboard)

    success_file = "data/{}-success-002.json".format(leaderboard)
    write_json_to_file(pages, success_file)

    error_file = "data/{}-errors-002.txt".format(leaderboard)
    write_text_to_file(errors, error_file)
    
