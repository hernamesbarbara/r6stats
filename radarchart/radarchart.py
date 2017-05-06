#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""radarchart.py
"""
import numpy as np
import matplotlib.pyplot as plt

class Radar(object):
    def __init__(self, fig, titles, labels, rotation=0, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.95, 0.95]

        self.n = len(titles)
        self.angles = np.arange(0, 360, 360.0/self.n)
        self.axes = [fig.add_axes(rect, projection="polar", label="axes{}".format(i)) 
                         for i in range(self.n)]
        if not len(labels):
            labels = [ [""]*self.n for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=10)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, self.n+1), angle=angle, labels=label)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, self.n)
            ax.set_theta_offset(np.deg2rad(rotation))

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)
