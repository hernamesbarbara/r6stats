#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""plotting.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def make_figure(figsize):
    return plt.figure(figsize=figsize, dpi=100)

def add_subplot(nrows, ncols, plot_number):
    return plt.subplot(nrows, ncols, plot_number)

def draw_plot(x, y, title=None, xscale=None, yscale=None, legend_loc='upper left', series_label=None):
    if title:
        plt.title(title)
    if yscale:
        plt.yscale(yscale)
    if xscale:
        plt.xscale(xscale)
    plt.plot(x, y, label=series_label)
    if legend_loc:
        plt.legend(loc=legend_loc)

def powerfunc(x):
    return x * x

def expfunc(x):
    return np.exp(x*5)
