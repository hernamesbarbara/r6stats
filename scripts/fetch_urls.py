#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import multiprocessing as mp
import os
import sys
import requests
try:
    import ujson as json
except:
    import json

####
####
from queue import Queue
from threading import Thread
import logging 
from time import time
import shutil
import glob

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
####
####

def read_lines(filename):
    with open(filename, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if line:
                yield (i, line)
            else:
                continue

def make_request(url):
    try:
        return requests.get(url).json()
    except Exception as err:
        print(str(err))
        return {}

def dump_jsonl(data, outstream):
    try:
        json.dump(data, outstream)
        outstream.write(os.linesep)
    except:
        pass

########
####

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        out_fmt = 'data/page-{:07d}.jsonl'
        while True:
            # Get the work from the queue and expand the tuple
            directory, (i, url) = self.queue.get()
            data = make_request(url)
            if data:
                with open(out_fmt.format(i+1), 'w') as o:
                    dump_jsonl(data, o)
            self.queue.task_done()

def purge_files(list_of_files):
    for f in list_of_files:
        os.remove(f)

def combine_all_files(list_of_files, combined_filename):
    with open(combined_filename, 'wb') as outfile:
        for filename in list_of_files:
            if filename == combined_filename:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)

    purge_files(list_of_files)


if __name__ == '__main__':

    ts = time()

    infile = sys.argv[1]
    download_dir = sys.argv[2]

    urls = list(read_lines(infile))

    # Create a queue to communicate with the worker threads
    queue = Queue()

    # Create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

        # Put the tasks into the queue as a tuple
    for (i, url) in urls:
        logger.info('Queueing {}'.format(url))
        queue.put((download_dir, (i, url)))

        # Causes main thread to wait for the queue to finish processing all tasks
        queue.join()
        logger.info('Took {}'.format(time() - ts))

    outfile_names = glob.glob(download_dir+"*.jsonl")

    combine_all_files(outfile_names, download_dir+"/pages.jsonl")

