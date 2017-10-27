#!/usr/bin/env bash
# -*- coding: utf-8 -*- 

START_TIME=$SECONDS

# helper script to run the full data cleaning process all at the same time

# INFILE => line delim json (.jsonl) file. Output of getleaderboards.py
INFILE="data/leaderboard-pages.jsonl"

# convert dataset from .jsonl to .csv. 
# output of next line will be data/leaderboard-pages.csv
echo -e "running scripts/json2csv.py\n"
ipython3 -c "%time %run scripts/json2csv.py $(readlink -f $INFILE)"

# read the csv data. do some cleaning. save normalize columns to features.csv.
echo -e "running scripts/features.py\n"
ipython3 -c "%time %run scripts/features.py $(readlink -f data/leaderboard-pages.csv)"

echo -e "cleaning up...\n"
# rm intermediary files. we don't need 'em.
rm "$(readlink -f data/leaderboard-pages-flat.jsonl)"
rm "$(readlink -f data/leaderboard-pages.csv)"

echo -e "done. completed in $(( SECONDS - START_TIME )) seconds.\n"

