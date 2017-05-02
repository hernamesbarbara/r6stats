#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""analyse_players.py
"""
import os
import sys
import numpy as np
import pandas as pd
from utils import io

pd.options.display.width = 220
pd.options.display.max_colwidth = 80
pd.options.display.max_columns = 40



df = pd.read_csv(sys.argv[1]).head(1000)

df_ps4 = io.read_player_csv(df, platform='ps4', game_mode='')
df_uplay = io.read_player_csv(df, platform='uplay', game_mode='')
df_xone = io.read_player_csv(df, platform='xone', game_mode='')


print "df_ps4: {} rows".format(df_ps4.shape[0])
print "df_uplay: {} rows".format(df_uplay.shape[0])
print "df_xone: {} rows".format(df_xone.shape[0])



###############
###############

df_stats = io.select_stats_columns_by_game_mode(df_ps4, '')
target = 'stats.ranked.wlr'
features = [col for col in df_stats.columns if col != target]


from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesRegressor


forest = ExtraTreesRegressor(n_estimators=250, random_state=0)

X, y = df_stats[features], df_stats[target]
forest.fit(X, y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
fig = plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), [features[i] for i in indices])
fig.autofmt_xdate()
plt.xlim([-1, X.shape[1]])
plt.show()


features = [
    'stats.ranked.kd'
]

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


