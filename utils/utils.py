#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""utils.py
"""
import r6io
import features

def sample_nrows(frame, pct_of_total=0.1, n=None, replace=False, random_state=42):
    if n is None:
        n = int(len(frame)*pct_of_total)
    return frame.sample(n)
