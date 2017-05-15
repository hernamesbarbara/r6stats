#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""json2csv.py
"""
import sys
import os
from utils import r6io

if __name__ == '__main__':
    infile = sys.argv[1]
    f_name, _ = os.path.splitext(infile)
    o_jsonl = "{}-flat.jsonl".format(f_name)
    o_csv = "{}.csv".format(f_name)

    # next line
    # CPU times: user 5min 59s, sys: 2.22 s, total: 6min 2s
    # Wall time: 6min 3s
    r6io.read_nested_write_flat(infile, o_jsonl)
    
    # next line
    # CPU times: user 1min 14s, sys: 7.69 s, total: 1min 22s
    # Wall time: 1min 23s
    r6io.jsonl_to_csv(o_jsonl, o_csv)

