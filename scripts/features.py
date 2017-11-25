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

def try_cast_int(num):
    if not num:
        return -999
    try:
        return np.int64(np.float64(num))
    except Exception as err:
        sys.stderr.write(u" ".join([str(err), str(num)]))
        sys.stderr.flush()
        try:
            return np.float64(num)
        except Exception as err:
            sys.stderr.write(u" ".join([str(err), str(num)]))
            sys.stderr.flush()
            raise

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

DATA_TYPES = {
    "meta.current_page": (try_cast_int, 0),
    "meta.next_page": (try_cast_int, 0),
    "meta.prev_page": (try_cast_int, 0),
    "meta.total_count": (try_cast_int, 0),
    "meta.total_pages": (try_cast_int, 0),
    "meta.url": (np.unicode,""),
    "ubisoft_id": (np.unicode,""),
    "stats.overall.bullets_hit": (try_cast_int, 0),
    "stats.ranked.deaths": (try_cast_int, 0),
    "stats.progression.level": (try_cast_int, 0),
    "stats.casual.wlr": (np.float64,np.nan),
    "stats.overall.penetration_kills": (try_cast_int, 0),
    "updated_at": (pd.to_datetime,pd.NaT),
    "stats.ranked.losses": (try_cast_int, 0),
    "stats.overall.melee_kills": (try_cast_int, 0),
    "stats.casual.has_played": (np.bool, False),
    "stats.overall.bullets_fired": (try_cast_int, 0),
    "stats.ranked.wins": (try_cast_int, 0),
    "stats.overall.headshots": (try_cast_int, 0),
    "indexed_at": (pd.to_datetime,pd.NaT),
    "stats.ranked.kd": (np.float64,np.nan),
    "platform": (np.unicode,""),
    "stats.ranked.wlr": (np.float64,np.nan),
    "username": (np.unicode,""),
    "stats.overall.revives": (try_cast_int, 0),
    "stats.casual.playtime": (try_cast_int, 0),
    "stats.casual.wins": (np.float64,np.nan),
    "stats.progression.xp": (try_cast_int, 0),
    "stats.ranked.playtime": (try_cast_int, 0),
    "stats.overall.assists": (try_cast_int, 0),
    "stats.overall.barricades_built": (try_cast_int, 0),
    "stats.casual.losses": (try_cast_int, 0),
    "stats.casual.kills": (try_cast_int, 0),
    "stats.casual.deaths": (try_cast_int, 0),
    "stats.overall.suicides": (try_cast_int, 0),
    "stats.overall.reinforcements_deployed": (try_cast_int, 0),
    "stats.casual.kd": (np.float64,np.nan),
    "stats.overall.steps_moved": (try_cast_int, 0),
    "stats.ranked.kills": (try_cast_int, 0),
    "stats.ranked.has_played": (np.bool, False)
}

CONVERTERS = {k: v[0] for k, v in DATA_TYPES.items()}

def fillna_and_apply(series, func, na_value):
    series = series.fillna(na_value)
    return series.apply(func)

def add_overall_totals(frame):
    frame = frame.fillna(0)
    frame = frame.replace(np.inf, 0)
    frame['stats.overall.playtime.hours'] = (frame[['stats.casual.playtime', 'stats.ranked.playtime']].sum(1)) / 60. / 60.
    frame['stats.overall.steps_moved'] = frame['stats.overall.steps_moved'].abs()
    frame['stats.overall.kills'] = frame[['stats.ranked.kills', 'stats.casual.kills']].sum(1).astype(np.int64)
    frame['stats.overall.deaths'] = frame[['stats.ranked.deaths', 'stats.casual.deaths']].sum(1).astype(np.int64)
    frame['stats.overall.wins'] = frame[['stats.ranked.wins', 'stats.casual.wins']].sum(1).astype(np.int64)
    frame['stats.overall.losses'] = frame[['stats.ranked.losses', 'stats.casual.losses']].sum(1).astype(np.int64)
    frame['stats.overall.points'] = frame[['stats.overall.assists', 'stats.overall.kills']].sum(1).astype(np.int64)
    defensive_actions = ['stats.overall.reinforcements_deployed', 'stats.overall.revives', 'stats.overall.barricades_built']
    frame['stats.overall.defensive_actions'] = frame[defensive_actions].sum(1).astype(np.int64)

    frame['stats.overall.engagements'] = frame[['stats.overall.kills', 'stats.overall.deaths']].sum(1)

    frame['stats.normalized.accuracy'] = frame['stats.overall.bullets_hit'] / frame['stats.overall.bullets_fired']
    frame['stats.normalized.points.perhour'] = frame['stats.overall.points'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.deaths.perhour'] = frame['stats.overall.deaths'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.kills.perhour'] = frame['stats.overall.kills'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.wins.perhour'] = frame['stats.overall.wins'] / frame['stats.overall.playtime.hours']
    frame['stats.normalized.losses.perhour'] = frame['stats.overall.losses'] / frame['stats.overall.playtime.hours']

    mask = (frame['stats.overall.kills']>0) & (frame['stats.overall.deaths']==0)
    frame['stats.normalized.kd'] = np.where(mask, 1.0, frame['stats.overall.kills'] / frame['stats.overall.deaths'])

    mask = (frame['stats.overall.wins']>0) & (frame['stats.overall.losses']==0)
    frame['stats.normalized.wlr'] = np.where(mask, 1.0, frame['stats.overall.wins'] / frame['stats.overall.losses'])

    frame['stats.normalized.defensive_actions.perhour'] = \
        frame['stats.overall.defensive_actions'] / frame['stats.overall.playtime.hours']

    frame['stats.normalized.points.perbullet_fired'] = \
        frame['stats.overall.points'] / frame['stats.overall.bullets_fired']

    frame['stats.normalized.aggression'] = \
        frame['stats.overall.points'] / frame['stats.overall.engagements']
    
    frame['stats.normalized.mobility'] = \
        frame['stats.overall.engagements'] / (frame['stats.overall.steps_moved'].abs() / frame['stats.overall.playtime.hours'])

    xp_scaled = scale_series(frame['stats.progression.xp'])
    frame[xp_scaled.name] = xp_scaled

    pt_scaled = scale_series(frame['stats.overall.playtime.hours'])
    frame[pt_scaled.name] = pt_scaled

    level_scaled = scale_series(frame['stats.progression.level'])
    frame[level_scaled.name] = level_scaled
    frame = frame.loc[:,frame.columns.sort_values()]
    return frame

def drop_players_with_low_playtime(frame, min_hours=24.0, copy=True):
    if copy:
        frame = frame.copy()
        return frame[frame['stats.overall.playtime.hours']>=min_hours]
    else:
        frame = frame[frame['stats.overall.playtime.hours']>=min_hours]
        return frame

def get_features_dataframe(frame):
    nrow = len(frame)
    for col in frame.columns:
        func, fill_value = DATA_TYPES[col]
        frame[col] = fillna_and_apply(frame[col], func, na_value=fill_value)
    return frame


def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]

    f_name, _ = os.path.splitext(infile)

    print("Reading {}".format(infile))
    df = pd.read_csv(infile, converters=CONVERTERS)
    print("nrow: {}".format(len(df)))
    print("ncol: {}".format(len(df.columns)))

    print("dropping duplicates")
    df = df.sort_values(by=['ubisoft_id', 'stats.casual.playtime'], ascending=[1,0])
    df = df.drop_duplicates('ubisoft_id')

    print("getting features")
    df = get_features_dataframe(df)

    print("adding totals")
    df = add_overall_totals(df)

    print("dropping players with low playtime")
    df = drop_players_with_low_playtime(df)
    print("nrow: {}".format(len(df)))
    print("ncol: {}".format(len(df.columns)))

    dims = ['username', 'updated_at', 'indexed_at', 'ubisoft_id', 'stats.casual.deaths']
    meta = df.columns[df.columns.str.startswith('meta.')].tolist()
    measures = df.columns[df.columns.isin(dims+meta)==False].tolist()
    col_order = dims+meta+measures

    assert len(df.columns) == len(col_order)
    df = df.loc[:, col_order]
    df.to_csv(outfile, index=False, encoding='utf-8')
    print("saved to {}".format(outfile))

if __name__ == '__main__':
    main()
