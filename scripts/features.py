#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""clean_raw_csv.py - read raw csv data and cast columns to the right types
and save the output to another csv file.
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

pd.options.display.width = 180
pd.options.display.max_colwidth = 80
pd.options.display.max_columns = 60
pd.options.display.max_rows = 200

def scale_series(series):
    series = series.copy().astype(float).fillna(series.mean())
    values_scaled = StandardScaler().fit_transform(series.values.reshape(-1,1))
    name = series.name
    return pd.Series(values_scaled[:,0], name=name+'.scaled')

def normalize_series(series):
    name = series.name
    series = series.copy().astype(float).fillna(series.mean())
    series = preprocessing.normalize(series.values.reshape(1,-1))[0,:]
    return pd.Series(series, name=name+'.normed')


infile = sys.argv[1]
outfile = sys.argv[2]

f_name, _ = os.path.splitext(infile)

print("Reading {}".format(infile))
df = pd.read_csv(infile, parse_dates=['meta.indexed_at', 'meta.updated_at'], nrows=20000)
print("nrow: {}".format(len(df)))
print("ncol: {}".format(len(df.columns)))

