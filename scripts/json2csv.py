#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""json2csv.py - convert line delim json file to csv

Usage:
    json2csv INFILE

Arguments:
    INFILE    Line delim json file you want to convert to csv

Options:
    -h --help           Show this message
    -v --version        Version number

"""
import sys
import os
import pandas as pd
from pandas.io.json.normalize import nested_to_record
import docopt

try:
    import ujson as json
except ImportError:
    import json

NAME = os.path.basename(__file__)
VERSION = "0.0.1"

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

def jsonl_to_csv(infile_jsonl, outfile_csv):
    pd.read_json(infile_jsonl, lines=True)\
        .to_csv(outfile_csv, index=False, encoding='utf-8')
    print("saved records to {}".format(outfile_csv))

def _parse_args():
    args = docopt.docopt(__doc__, argv=" ".join(sys.argv[1:]), 
                         version="{}=={}".format(NAME, VERSION)) 
    try:
        infile = args["INFILE"]
        dirname = os.path.dirname(infile)
        f_name, _ = os.path.splitext(infile)
        o_jsonl = "{}-flat.jsonl".format(f_name)
        o_csv = "{}.csv".format(f_name)
        return (infile, dirname, f_name, o_jsonl, o_csv)
    except Exception as err:
        sys.stderr.write(str(err)+os.linesep)
        sys.stderr.write(__doc__)
        sys.exit(1)

def main():
    (infile, dirname, f_name, o_jsonl, o_csv) = _parse_args()
    if os.path.exists(o_jsonl):
        os.remove(o_jsonl)
    # next line
    # CPU times: user 5min 59s, sys: 2.22 s, total: 6min 2s
    # Wall time: 6min 3s
    print("Flattening json...")
    read_nested_write_flat(infile, o_jsonl)
    
    # next line
    # CPU times: user 1min 14s, sys: 7.69 s, total: 1min 22s
    # Wall time: 1min 23s
    print("Saving to csv...")
    jsonl_to_csv(o_jsonl, o_csv)

if __name__ == '__main__':
    main()
