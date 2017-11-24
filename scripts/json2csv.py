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

def flatten_page(page):
    meta = page['meta']
    players = page['players']
    for player in players:
        try:
            res = nested_to_record(player)
            for k, v in meta.items():
                res['meta.{}'.format(k)] = v
            yield res
        except Exception as err:
            sys.stderr.write(str(err))
            sys.stderr.flush()
            continue

def jsonl_to_csv(infile, outfile):
    "read line delim json file. flatten each nested record. save data to csv."
    with open(infile, 'r') as infile:
        with open(outfile, 'a') as outfile:
            for i, page in enumerate(read_jsonl_stream(infile)):
                    try:
                        page = flatten_page(page)
                        if i == 0:
                            header = True
                        else:
                            header = False
                        pd.DataFrame(page).to_csv(
                            outfile, 
                            header=header,
                            index=False,
                            encoding='utf-8'
                        )

                    except Exception as err:
                        sys.stderr.write(str(err))
                        sys.stderr.flush()
                        continue

def _parse_args():
    args = docopt.docopt(__doc__, argv=" ".join(sys.argv[1:]), 
                         version="{}=={}".format(NAME, VERSION)) 
    try:
        infile = args["INFILE"]
        dirname = os.path.dirname(infile)
        f_name, _ = os.path.splitext(infile)
        o_jsonl = "{}-flat.jsonl".format(f_name)
        o_csv = "{}.csv".format(f_name)
        return (infile, dirname, f_name, o_csv)
    except Exception as err:
        sys.stderr.write(str(err)+os.linesep)
        sys.stderr.write(__doc__)
        sys.exit(1)

def main():
    (infile, dirname, f_name, o_csv) = _parse_args()
    # CPU times: user 15min 17s, sys: 8.61 s, total: 15min 25s
    # Wall time: 15min 29s
    print("Saving to csv...")
    jsonl_to_csv(infile, o_csv)

if __name__ == '__main__':
    main()
