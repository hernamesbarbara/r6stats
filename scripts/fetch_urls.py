#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
import requests
try:
    import ujson as json
except:
    import json

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import glob
import shutil

import logging
import pygogo as gogo



logger = gogo.Gogo(os.path.basename(__file__),
    low_formatter=gogo.formatters.fixed_formatter,
    high_formatter=gogo.formatters.fixed_formatter
).logger

def read_lines(filename):
    with open(filename, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if line:
                yield (i, line)
            else:
                continue

 
def get_request(url, params={}):
    """
    Downloads the specified URL and saves it to disk
    """
    try:
        r = requests.Request('GET', url, params=params)
        s = requests.Session()
        return s.send(r.prepare())
    except Exception as err:
        logger.error(str(err))
        return None

def dump_jsonl(data, outfile_name):
    with open(outfile_name, 'w') as outstream:
        try:
            json.dump(data, outstream)
            outstream.write(os.linesep)
            return outfile_name
        except Exception as err:
            logger.error(str(err))
            return None

def purge_files(list_of_files):
    for f in list_of_files:
        os.remove(f)

def combine_all_files(list_of_files, combined_filename, cleanup=True):
    with open(combined_filename, 'w') as outfile:
        for filename in list_of_files:
            if filename == combined_filename:
                # don't want to copy the output into the output
                continue
            with open(filename, 'r') as readfile:
                shutil.copyfileobj(readfile, outfile)

    if cleanup:
        purge_files([f for f in list_of_files if f != combined_filename])

def job(url, outdir):
        outdir = outdir.strip('/')
        url_parts = requests.packages.urllib3.util.parse_url(url)
        leaderboard_name = url_parts.path.split('/')[-1]
        page_number = int(url_parts.query.split('=')[-1])
        outfile_name = '{}/page-{:07d}.jsonl'.format(outdir, page_number)
        r = get_request(url)
        if r is None:
            res = (None, url)
        else:
            data = r.json()
            meta = data.get('meta', {})
            meta['url'] = r.url
            data['meta'] = meta
            outfile_name = dump_jsonl(data, outfile_name)
            res = (outfile_name, url)
        return res

def main():
    """
    Create a thread pool and download specified urls
    """
    url_file = sys.argv[1]
    outdir   = sys.argv[2].strip('/')+'/'

    url_tups = list(read_lines(url_file))
    urls     = [tup[1] for tup in url_tups]
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(job, url, outdir) for url in urls]
        for i, future in enumerate(as_completed(futures)):
            (outfile_name, url) = res = future.result()
            if i % 100 == 0:
                msg = "GET '{}' => '{}'".format(url, outfile_name)
                logger.debug(msg)

    page_files = glob.glob(outdir+'*.jsonl')
    combined_filename = outdir+'combined-pages.jsonl'
    combine_all_files(page_files, combined_filename, cleanup=True)

    msg = 'merging {} files => {}'.format(len(page_files), combined_filename)
    logger.info(msg)
 
if __name__ == '__main__':
    main()
