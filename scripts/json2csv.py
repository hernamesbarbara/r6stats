#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py

* this one reads in the raw data in jsonl (line delim json) and converts it to csv.
* the data is super nested, so it first flattens each line delim document in the 
* input file. so you get 2 new files after you run this one.

"""
import sys
import os
from utils import r6io

if __name__ == '__main__':
    infile = sys.argv[1]
    f_name, _ = os.path.splitext(infile)
    o_jsonl = "{}-flat.jsonl".format(f_name)
    o_csv = "{}.csv".format(f_name)
    if os.path.exists(o_jsonl):
        os.remove(o_jsonl)
    # next line
    # CPU times: user 5min 59s, sys: 2.22 s, total: 6min 2s
    # Wall time: 6min 3s
    print("Flattening json...")
    r6io.read_nested_write_flat(infile, o_jsonl)
    
    # next line
    # CPU times: user 1min 14s, sys: 7.69 s, total: 1min 22s
    # Wall time: 1min 23s
    print("Saving to csv...")
    r6io.jsonl_to_csv(o_jsonl, o_csv)
