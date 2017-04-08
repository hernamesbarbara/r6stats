#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""r6api.py
"""
import sys
import os
import json
import requests
import hammock
import copy



class R6Api(hammock.Hammock):

    ENDPOINTS = ['leaderboards']
    
    def __init__(self, name='https://api.r6stats.com/api/v1', parent=None, **kwargs):
        super(R6Api, self).__init__(name, parent, **kwargs)
    
    def _url(self, *args):
        return super(R6Api, self)._url(*args)

r6 = R6Api()
seen = []

STOP_AFTER = 3

if len(seen) == 0:
    page = r6.leaderboards.casual.GET(params={'page':1}).json()
    total_pages = page['meta']['total_pages']
    for i in xrange(page['meta']['next_page'], total_pages):
        try:
            page = r6.leaderboards.casual.GET(params={'page': i}).json()
            seen.append(page)
        except:
            continue
        
        if i >= STOP_AFTER: 
            break
