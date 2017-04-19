#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""analyse_players.py
"""
import numpy as np
import pandas as pd

pd.options.display.width = 200
pd.options.display.max_colwidth = 75

def select_stats_for(frame, platform, game_mode):
    stats_columns = frame.columns[
        (frame.columns.str.startswith("stats.{}".format(game_mode))) &
        (frame.columns != "stats.{}.playtime".format(game_mode)) &
        (frame.columns != "stats.{}.has_played".format(game_mode))
    ]
    return frame.ix[frame['platform'] == platform, stats_columns]

df = pd.read_csv('tmp/sample.csv')

df.indexed_at = pd.to_datetime(df.indexed_at)
df.updated_at = pd.to_datetime(df.updated_at)
df = df.sort_values(['username', 'updated_at'], ascending=[True, False])

df_stats = select_stats_for(df, 'ps4', 'ranked')

target = 'stats.ranked.wlr'
features = [col for col in df_stats.columns if col != target]


from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

for feature in features:
    X = df_stats[[feature]]
    y = df_stats[[target]]

    X = pd.DataFrame(preprocessing.scale(X), columns=X.columns)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.40, random_state=42)


    model = LinearRegression()
    model = model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mean_sq_error = np.mean((y_pred - y_test)**2)[0]
    print "{}: Mean squared error: {:.2f}".format(feature, mean_sq_error)

    print "{}: Variance score: {:.2f}".format(feature, model.score(X_test, y_test))

    # Plot outputs
    plt.scatter(X_test, y_test,  color='black')
    plt.plot(X_test, y_pred, color='blue',linewidth=1)
    plt.xticks(())
    plt.yticks(())
    plt.show()


