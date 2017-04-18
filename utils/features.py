#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""features.py
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn import preprocessing

def normalize_dataframe(frame, drop_non_numeric=True, sep="."):
    """
    Rescale all real numbers in dataframe between range 0..1
    Takes and returns pandas.DataFrame
    """
    numeric = frame.select_dtypes(include=[np.number]).columns
    non_numeric = frame.columns[frame.columns.isin(numeric)==False]
    colnames = numeric + sep + "norm"
    values = preprocessing.normalize(frame[numeric].fillna(0), axis=0)
    df_numbers = pd.DataFrame(values, columns=colnames)
    if drop_non_numeric:
        return df_numbers
    else:
        return frame[non_numeric].join(df_numbers)

