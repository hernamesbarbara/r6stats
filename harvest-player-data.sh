#!/usr/bin/env bash
# -*- coding: utf-8 -*- 

if [ ! -f "data/leaderboard-pages.jsonl" ]; then
    echo -e "Running getleaderboards.py...this will take a few hours...ZzzZ\n"
    python getleaderboards.py "data/leaderboard-pages.jsonl"
    
else
    echo -e "File Already Exists: data/leaderboard-pages.jsonl\n"
fi

echo -e "Running json2csv.py\n"
python json2csv.py "data/leaderboard-pages.jsonl"

