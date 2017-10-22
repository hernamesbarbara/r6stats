#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""featuresonly.py
read in the features.csv file and drop everything except a handful of columns
"""
import pandas as pd 

OUTFILE = '../data/features.csv'

df = pd.read_csv('../data/leaderboard-pages-features.csv')

id_cols = ['ubisoft_id', 'platform']
features = [col for col in df.columns if '.normalized.' in col ]

df.loc[:, id_cols+features].to_csv(OUTFILE, index=False, encoding='utf-8')
print('saved features to {}'.format(OUTFILE))
