#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""generateurls.py - generate API endpoints to call

Usage:
    generateurls --output OUTPUT

Arguments:
    -o --output OUTPUT    filename where you want to save urls

Options:
    -h --help           Show this message
    -v --version        Version number

"""

import sys
import os
import docopt
import requests

try:
    import ujson as json
except ImportError:
    import json


NAME = os.path.basename(__file__)
VERSION = "0.0.1"

def get_url(base_url, leaderboard, page_num):
    url = base_url.format(leaderboard, page_num)
    try:
        req = requests.get(url)
    except Exception as err:
        sys.stderr.write(str(err))
        req = None
    return url, req


def main():
    args = docopt.docopt(__doc__, argv=" ".join(sys.argv[1:]), 
                         version="{}=={}".format(NAME, VERSION))
    try:
        output = args["--output"]
    except Exception as err:
        sys.stderr.write(str(err)+os.linesep)
        sys.stderr.write(__doc__)
        sys.exit(1)
    base_url = 'https://api.r6stats.com/api/v1/leaderboards/{}?page={}'
    with open(output, 'w') as output:
        for leaderboard in ('casual', 'ranked', 'general'):
            start_page = 1
            url, req = get_url(base_url, leaderboard, start_page)
            page = req.json()
            end_page = int(page['meta']['total_pages'])
            for i in range(start_page, end_page+1):
                url = base_url.format(leaderboard, i)
                output.write(url)
                output.write(os.linesep)
            sys.stdout.write('done with {}'.format(leaderboard))
            sys.stdout.write(os.linesep)
            sys.stdout.flush()

if __name__ == '__main__':
    main()
