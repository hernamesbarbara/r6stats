#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""getplayers.py
"""
import sys
import os
import json
import requests


base = "https://api.r6stats.com"
version = '/api/v1'
endpoint =  '/leaderboards/casual'
url = "{base}{version}{endpoint}".format(base=base, version=version, endpoint=endpoint)

def get_page(url=url, page=1):
    return requests.get(url, params={'page': page})

n_pages = 7615
n_players = 190359

pages = []
page_errors = []

n = n_pages

for i in range(1, n+1):
    if i % 10 == 0:
        print "{} of {}".format(i, n)
    try:
        r = get_page(url, i)
        page = r.json()
        pages.append(page)
    except Exception, err:
        r = requests.Request('GET', url, params={'page':i}).prepare()
        page = None
        page_errors.append(r.url)

print "{} succuessful".format(len(pages))
print "{} errors".format(len(page_errors))

json.dump(pages, open("pages.json", "w"), encoding='utf8', indent=2)

with open("page_errors.txt", "w") as e:
    e.write(os.linesep.join(page_errors))
