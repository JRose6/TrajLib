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
for df in all_dfs:
    ts_obj=TrajectorySegmentation()
    ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                     labels=['label'],seperator=';',src=df)
    segment_indexes,segments = ts_obj.segmentByLabel(label='label')
    ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
    parameters=  {''}
    segment_indexes,segments = ts_obj.segmentByStopMove( max_dist=10000,
                                                         min_time=2,
                                                         time_tolerance=2000,
                                                         merge_tolerance=50)
    print(segment_indexes)
    predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
    print(predicted)
    results.append([SegmentationEvaluation.harmonic_mean(ground_truth,predicted),
               SegmentationEvaluation.purity(ground_truth, predicted)[1],
               SegmentationEvaluation.coverage(ground_truth, predicted)[1]])
results_df = pd.DataFrame(results,columns=list('hpc'))
print(np.mean(results,axis=0))
results_df.to_csv('cbsmot_fv.csv')



