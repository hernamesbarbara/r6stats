#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py
"""
import sys
import os
import numpy as np
import pandas as pd
from pandas.io.json import nested_to_record
from bandit import Bandit
try:
    import ujson as json
except ImportError:
    import json

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

def read_jsonl_stream(stream):
    for line in stream:
        try:
            yield json.loads(line)
        except:
            continue

def dump_jsonl_stream(data, stream):
    try:
        json.dump(data, stream)
        stream.write(os.linesep)
    except:
        pass

def read_nested_write_flat(infile, outfile):
    with open(infile, 'r') as infile:
        with open(outfile, 'a') as outfile:
            for record in read_jsonl_stream(infile):
                dump_jsonl_stream(nested_to_record(record), outfile)
    print "saved records to {}".format(outfile)

def jsonl_to_csv(infile_jsonl, outfile_csv):
    pd.read_json(infile_jsonl, lines=True).to_csv(outfile_csv, index=False, encoding='utf-8')
    print "saved records to {}".format(outfile_csv)

if __name__ == '__main__':
    infile = sys.argv[1]
    f_name, _ = os.path.splitext(infile)
    o_jsonl = "{}-flat.jsonl".format(f_name)
    o_csv = "{}.csv".format(f_name)

    # next line
    # CPU times: user 5min 59s, sys: 2.22 s, total: 6min 2s
    # Wall time: 6min 3s
    read_nested_write_flat(infile, o_jsonl)
    
    # next line
    # CPU times: user 1min 14s, sys: 7.69 s, total: 1min 22s
    # Wall time: 1min 23s
    jsonl_to_csv(o_jsonl, o_csv)

