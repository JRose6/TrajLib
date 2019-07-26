import pandas as pd
from sklearn.model_selection import ParameterGrid
import numpy as np
from enum import Enum


class DataEnum(Enum):
    FISHING = 1
    HURRICANES=2
    GEOLIFE=3
class AlgoEnum(Enum):
    CBSMoT = 1
    DBSMoT = 2


def get_data(d,algorithm):
    ret = None
    if d == DataEnum.FISHING:
        data = get_fv()
    elif d==DataEnum.HURRICANES:
        data = get_hurr()
    elif d==DataEnum.GEOLIFE:
        data = get_geolife()
    if algorithm  == AlgoEnum.CBSMoT:
        parms = cbsmot_parms(d)
    elif algorithm == AlgoEnum.DBSMoT:
        parms = dbsmot_parms(d)
    ret = {'data':data,
         'parameter_grid':parms}
    return ret


def get_fv():
    dfs= []
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d1.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d2.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d3.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d4.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d5.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d6.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d7.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d8.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d9.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Fishing Vessels/fv_d10.txt',sep=';'))
    return dfs

def get_hurr():
    dfs=[]
    dfs.append(pd.read_csv('databases/Hurricanes/h_d1.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d2.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d3.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d4.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d5.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d6.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d7.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d8.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d9.txt',sep=';'))
    dfs.append(pd.read_csv('databases/Hurricanes/h_d10.txt',sep=';'))
    return dfs

def get_geolife():
    dfs=[]
    dfs.append(pd.read_csv('Hurricanes/h_d1.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d2.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d3.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d4.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d5.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d6.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d7.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d8.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d9.txt',sep=';'))
    dfs.append(pd.read_csv('Hurricanes/h_d10.txt',sep=';'))
    return dfs

def cbsmot_parms(d):
    ret = None
    if d==DataEnum.HURRICANES:
        ret =  ParameterGrid({'area':list(np.arange(0.1,1,0.05)),
                  'min_time':list(range(1,24,4)),
                  'time_tolerance':[0],
                   'merge_tolerance':[0]})
    elif d == DataEnum.FISHING:
        ret = ParameterGrid({'area':list(np.arange(0.1,1,0.1)),
                  'min_time':list(range(2,12,2)),
                  'time_tolerance':list(range(0,2,1)),
                   'merge_tolerance':list(range(0,1,1))})
    elif d == DataEnum.GEOLIFE:
        ret = ParameterGrid({'area':list(np.arange(0.1,1,0.1)),
                  'min_time':list(range(2,12,2)),
                  'time_tolerance':list(range(0,2,1)),
                   'merge_tolerance':list(range(0,1,1))})
    return ret

def dbsmot_parms(d):
    ret = None
    if d==DataEnum.HURRICANES:
        ret =  ParameterGrid({'area':list(np.arange(0.1,1,0.05)),
                  'min_time':list(range(1,24,4)),
                  'time_tolerance':[0],
                   'merge_tolerance':[0]})
    elif d == DataEnum.FISHING:
        ret = ParameterGrid({'area':list(np.arange(0.1,1,0.1)),
                  'min_time':list(range(2,12,2)),
                  'time_tolerance':list(range(0,2,1)),
                   'merge_tolerance':list(range(0,1,1))})
    elif d == DataEnum.GEOLIFE:
        ret = ParameterGrid({'area':list(np.arange(0.1,1,0.1)),
                  'min_time':list(range(2,12,2)),
                  'time_tolerance':list(range(0,2,1)),
                   'merge_tolerance':list(range(0,1,1))})
    return ret