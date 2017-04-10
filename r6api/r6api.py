#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""r6api.py
"""
import sys
import os
import json
import requests
import copy


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

    def __str__(self):
        return self._base_url

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._base_url)


def GET(url, params={}):
    data = requests.get(url, params).json()
    return DotDict(data)


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

    def __str__(self):
        return self._base_url

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._base_url)


# api = Endpoint()
api = R6Api()

r = api.leaderboards.casual.GET(params={'page':1})
