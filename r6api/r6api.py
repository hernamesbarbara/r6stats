#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""r6api.py
"""
import sys
import os
import json
import requests
import hammock


class R6Api(hammock.Hammock):
    """query rainbow six siege API"""

    ENDPOINTS = [{'leaderboards': ['casual']}]
    
    def __init__(self):
        base_url = "https://api.r6stats.com/api/v1"
        super(R6Api, self).__init__(base_url)

    def leaderboards(self, leaderboard, page):
        method = super(R6Api, r6).__getattr__('leaderboards')
        return method.GET(leaderboard, params={'page': page})


r6 = R6Api()

req = r6.leaderboards('casual', page=1)
print 'url: {}'.format(req.url)
print 'status: {}'.format(req.status_code)

data = req.json()
