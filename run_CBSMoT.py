from SegmentationAlgorithms.CBSMoT import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import SegmentationEvaluation
import pandas as pd
import time
import numpy as np

dfs = []
def get_fv():
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
def get_hurr_parms():
    return ParameterGrid({'max_dist':list(range(15000,100000,5000)),
                  'min_time':list(range(2,24,2)),
                  'time_tolerance':list(range(2,12,4)),
                   'merge_tolerance':list(range(0,1002,500))})
def get_fv_parms():
    pass

dfs = get_hurr()
parameter_grid = get_hurr_parms()

all_dfs = []
def split_df(df,label='tid'):
    real_dfs = []
    df.set_index(keys=['tid'],drop=False,inplace=True)
    tids = df['tid'].unique().tolist()
    for tid in tids:
        real_dfs.append(df.loc[df.tid ==tid])
    return real_dfs
for df in dfs:
    all_dfs+=split_df(df)
results = []
hm_best = 0
N=5
for p in parameter_grid:
    hm_sum=0
    for df in all_dfs[:N]:
        ts_obj=TrajectorySegmentation()
        ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                         labels=['label'],seperator=';',src=df)
        segment_indexes,segments = ts_obj.segmentByLabel(label='label')
        ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
        segment_indexes,segments = ts_obj.segment_CBSMoT(max_dist=p['max_dist'],
                                                         min_time=p['min_time']*3600,
                                                         time_tolerance=p['time_tolerance']*3600,
                                                         merge_tolerance=p['merge_tolerance'])
        predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
        hm=SegmentationEvaluation.harmonic_mean(ground_truth,predicted)
        hm_sum += hm
    print(p,"%.4f"%(hm_sum/N))
    if hm_sum>hm_best:
        print("Best Parameters",p)
        print("Harmonic Mean",(hm_sum/N))
        hm_best = hm_sum

