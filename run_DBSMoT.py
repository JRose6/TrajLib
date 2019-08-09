from SegmentationAlgorithms.CBSMoT import CBSmot
from SegmentationAlgorithms.DBSMoT import DBSMoT
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
for df in all_dfs:
    ts_obj=TrajectorySegmentation()
    ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                     labels=['label'],seperator=';',src=df)
    segment_indexes,segments = ts_obj.segmentByLabel(label='label')
    ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
    #print(len(ground_truth))
    #segment_indexes,segments = ts_obj.segment_DBSMoT()
    dbsmot = DBSMoT()
    print(segment_indexes)
    segment_indexes = dbsmot.segment(ts_obj,90,
    60*60*4,4)
    print(segment_indexes)

    predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
    p = SegmentationEvaluation.purity(ground_truth,predicted)[1]
    c = SegmentationEvaluation.coverage(ground_truth,predicted)[1]
    hm = SegmentationEvaluation.harmonic_mean(ground_truth,predicted)
    print(p, c, hm)
    print("********************")
    results.append([p,c,hm])
df = pd.DataFrame(results,columns=list('pch'))
df2 = df.describe()
df2.to_csv('described.csv')

