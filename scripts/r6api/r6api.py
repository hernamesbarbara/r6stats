#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""r6api.py
"""
import sys
import os
import json
import requests

class DotDict(dict):
    """
    dict that supports both dot.notation and sub['notation']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value

def GET(url, params={}):
    try:
        data = requests.get(url, params=params).json()
        return DotDict(data)
    except Exception as err:
        r = requests.Request('GET', url, params=params).prepare()
        raise Exception("GET exception", r.url)

class Endpoint(object):
    def __init__(self, base_url, child_endpoints):
        self._base_url = base_url
        self._endpoints = child_endpoints
        for endpoint, children in child_endpoints.items():
            if endpoint=='methods':
                for method, function in children.items():
                    def wrapper(params={}):
                        return function(self._base_url, params)
                    setattr(self, method, wrapper)
                continue
            setattr(self, endpoint, Endpoint(os.path.join(base_url, endpoint), children))

    def __getattr__(self, attr):
        return self.__dict__[attr]

    def __getitem__(self, attr):
        return self.__dict__[attr]

    def __str__(self):
        return self._base_url

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._base_url)

class R6Api(Endpoint):
    BASE_URL = 'https://api.r6stats.com/api/v1'
    ENDPOINTS = {
        'leaderboards': {
            'casual': {'methods': {'GET': GET}},
            'general': {'methods': {'GET': GET}},
            'ranked': {'methods': {'GET': GET}}
        }
    }
    
    def __init__(self):
        super(R6Api, self).__init__(self.BASE_URL, self.ENDPOINTS)


