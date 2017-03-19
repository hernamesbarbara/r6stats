#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""playerapi.py
"""
import sys
import os
import json
import requests
import pandas as pd


def get_url(platform, username):
    base = "https://api.r6stats.com"
    version = '/api/v1'
    endpoint = '/players/{username}/?platform={platform}'.format(platform=platform, username=username)
    return "{base}{version}{endpoint}".format(base=base, version=version, endpoint=endpoint)


df = pd.read_csv('data/players.csv')

# for player in players:
#     get the data goes here..
#     url = get_url(platform, username)
#     r = requests.get(url)
#     data = r.json()
