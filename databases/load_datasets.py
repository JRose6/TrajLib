import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np
from enum import Enum


class DataEnum(Enum):
    FISHING = 'FISHING'
    HURRICANES = 'HURRICANES'
    GEOLIFE = 'GEOLIFE'


class AlgoEnum(Enum):
    CBSMoT = 'CB-SMoT'
    DBSMoT = 'DB-SMoT'


def get_data(d, algorithm):
    ret = None
    if d == DataEnum.FISHING:
        data = get_fv()
        label = 'label'
    elif d == DataEnum.HURRICANES:
        data = get_hurr()
        label = 'label'
    elif d == DataEnum.GEOLIFE:
        data = get_geolife()
        label = 'transportation_mode'
    if algorithm == AlgoEnum.CBSMoT:
        parms = cbsmot_parms(d)
    elif algorithm == AlgoEnum.DBSMoT:
        parms = dbsmot_parms(d)
    ret = {'data': data,
           'parameter_grid': parms,
           'file_name': str(algorithm.value) + "_" + str(d.value) + "_results.csv",
           'label':label}
    return ret


def get_fv():
    dfs = []
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d1.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d2.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d3.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d4.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d5.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d6.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d7.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d8.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d9.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Fishing Vessels/fv_d10.txt', sep=';')))
    return dfs


def get_hurr():
    dfs = []
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d1.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d2.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d3.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d4.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d5.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d6.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d7.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d8.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d9.txt', sep=';')))
    dfs.append(split_df(pd.read_csv('databases/Hurricanes/h_d10.txt', sep=';')))
    return dfs


def get_geolife():
    dfs = []
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_1.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_2.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_3.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_4.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_5.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_6.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_7.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_8.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_9.csv', sep=',')])
    dfs.append([pd.read_csv('databases/geolife/geolife_w_features_10.csv', sep=',')])
    return dfs


def cbsmot_parms(d):
    ret = None
    if d == DataEnum.HURRICANES:
        ret = ParameterGrid({'area': list(np.arange(0.1, 1, 0.025)),
                             'min_time': np.array(range(0, 24, 6))*3600,
                             'time_tolerance': [0],
                             'merge_tolerance': [0]})
    elif d == DataEnum.FISHING:
        ret = ParameterGrid({'area': list(np.arange(0.1, 1, 0.05)),
                             'min_time': np.array(range(2, 13, 2))*3600,
                             'time_tolerance': [0],
                             'merge_tolerance': [0]})
    elif d == DataEnum.GEOLIFE:
        ret = ParameterGrid({'area': np.arange(0.1, 0.5, 0.05),
                             'min_time': np.arange(0.1, 2, 0.2)*3600,
                             'time_tolerance': [0],
                             'merge_tolerance':[0]})
    return ret


def dbsmot_parms(d):
    ret = None
    if d == DataEnum.HURRICANES:
        ret = ParameterGrid({})
    elif d == DataEnum.FISHING:
        ret = ParameterGrid({})
    elif d == DataEnum.GEOLIFE:
        ret = ParameterGrid({})
    return ret


def split_df(df,label='tid'):
    real_dfs = []
    df.set_index(keys=['tid'],drop=False,inplace=True)
    tids = df['tid'].unique().tolist()
    for tid in tids:
        real_dfs.append(df.loc[df.tid ==tid])
    return real_dfs