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
from r6api.r6api import R6Api

NAME = os.path.basename(__file__)
VERSION = "0.0.1"

def main():
    args = docopt.docopt(__doc__, argv=" ".join(sys.argv[1:]), 
                         version="{}=={}".format(NAME, VERSION))
    try:
        output = args["--output"]
    except Exception as err:
        sys.stderr.write(str(err)+os.linesep)
        sys.stderr.write(__doc__)
        sys.exit(1)
    r6 = R6Api()
    with open(output, 'w') as output:
        for leaderboard in ('casual', 'ranked', 'general'):
            start_page = 1
            end_page = int(r6.leaderboards[leaderboard].GET(params={'page': start_page})['meta']['total_pages'])
            fmt = 'https://api.r6stats.com/api/v1/leaderboards/{}?page={}'
            for i in range(start_page, end_page+1):
                url = fmt.format(leaderboard, i)
                output.write(url)
                output.write(os.linesep)
            sys.stdout.write('done with {}'.format(leaderboard))
            sys.stdout.write(os.linesep)
            sys.stdout.flush()

if __name__ == '__main__':
    main()
