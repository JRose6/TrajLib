from SegmentationAlgorithms.CBSMoT import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import SegmentationEvaluation
import pandas as pd
import time
import numpy as np

dfs = []
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

ts_obj=TrajectorySegmentation()
ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                 labels=['label'],seperator=';',src=all_dfs[0])
segment_indexes,segments = ts_obj.segmentByLabel(label='label')
ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
segment_indexes,segments = ts_obj.segment_DBSMoT()
predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)



