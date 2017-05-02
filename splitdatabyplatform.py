#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""splitdatabyplatform.py
"""
import sys
import os
import numpy as np
import pandas as pd
from utils import io

pd.options.display.width = 220
pd.options.display.max_colwidth = 80
pd.options.display.max_columns = 40

df = pd.read_csv(sys.argv[1])

df_ps4 = io.read_player_csv(df, platform='ps4', game_mode='')
df_uplay = io.read_player_csv(df, platform='uplay', game_mode='')
df_xone = io.read_player_csv(df, platform='xone', game_mode='')
