#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""analyse_players.py
"""
import numpy as np
import pandas as pd

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

df = pd.read_csv('data/players.csv')

df.indexed_at = pd.to_datetime(df.indexed_at)
df.updated_at = pd.to_datetime(df.updated_at)
df = df.sort_values(['username', 'updated_at'], ascending=[True, False])



