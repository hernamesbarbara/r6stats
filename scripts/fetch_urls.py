#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import sys
import time
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
        for line in f.readlines():
            line = line.strip()
            if line:
                yield line
            else:
                continue

def get_unseen_urls(url_file, seen_file):
    "get urls from url_file if they dont appear in seen_file"
    urls = read_lines(url_file)
    seen = read_lines(seen_file)
    return sorted(set(urls).difference(set(seen)))

 
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
        outfile_name = '{}/{}-page-{:07d}.jsonl'.format(outdir, leaderboard_name, page_number)
        r = get_request(url)
        if r is None:
            res = (None, url)
        else:
            data = r.json()
            meta = data.get('meta', {})
            meta['url'] = r.url
            data['meta'] = meta
            outfile_name = dump_jsonl(data, outfile_name)
            res = outfile_name, url
        return res

def main():
    """
    Create thread pool w/ ThreadPoolExecutor & download urls in parallel.
    """
    url_file = sys.argv[1]
    outdir   = sys.argv[2].strip('/')+'/'
    seen_file = outdir+"seen.txt"
    if not (os.path.exists(seen_file) and os.path.isfile(seen_file)):
        with open(seen_file, 'w+') as f:
            pass
    urls = get_unseen_urls(url_file, seen_file)
    # Schedules the callable, fn, to be executed as fn(*args **kwargs) 
    # and return a Future object representing the execution of the callable.
    # If max_workers is None or not given, it will default to the number of 
    # processors on the machine, multiplied by 5, assuming that ThreadPoolExecutor 
    # is often used to overlap I/O instead of CPU work and the number of workers 
    # should be higher than the number of workers for ProcessPoolExecutor.

    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(job, url, outdir) for url in urls]
        loop_time = time.time()
        for i, future in enumerate(as_completed(futures)):
            try:
                outfile_name, url = future.result()
                if url and url.strip():
                    msg = "GET '{}' => '{}'".format(url, outfile_name)
                    logger.debug(msg)
                    with open(seen_file, 'a') as f:
                        f.write(url.strip())
                        f.write(os.linesep)
                else:
                    continue
            except Exception as err:
                logger.error(str(err))
            if i % 10 == 0:
                logger.debug("Loop Completd in: {:10.10f}".format(time.time()-loop_time))
                loop_time = time.time()
    page_files = glob.glob(outdir+'*.jsonl')
    combined_filename = outdir+'combined-pages.jsonl'
    combine_all_files(page_files, combined_filename, cleanup=True)

    msg = 'merging {} files => {}'.format(len(page_files), combined_filename)
    logger.info(msg)
 
if __name__ == '__main__':
    main()
