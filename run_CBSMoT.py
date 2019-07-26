from SegmentationAlgorithms.CBSMoT import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import SegmentationEvaluation
import pandas as pd
from databases import load_datasets

def split_df(df,label='tid'):
    real_dfs = []
    df.set_index(keys=['tid'],drop=False,inplace=True)
    tids = df['tid'].unique().tolist()
    for tid in tids:
        real_dfs.append(df.loc[df.tid ==tid])
    return real_dfs

dataset = load_datasets.DataEnum.HURRICANES
algorithm = load_datasets.AlgoEnum.CBSMoT

data = load_datasets.get_data(dataset,algorithm)
dfs = data['data']
parameter_grid = data['parameter_grid']
all_dfs = []


results = []
best_p = {}
for i in range(0,len(dfs)):
    hm_best = 0
    train_dfs = split_df(dfs[i])
    test_dfs = []
    for j in range(0, len(dfs)):
        if j!=i:
            test_dfs += split_df(dfs[j])
    for p in parameter_grid:
        hm_sum = 0
        for tdf in train_dfs:
            N = len(train_dfs)
            ts_obj=TrajectorySegmentation()
            ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                             labels=['label'],seperator=';',src=tdf)
            segment_indexes,segments = ts_obj.segmentByLabel(label='label')
            ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
            segment_indexes,segments = ts_obj.segment_CBSMoT(max_dist=None,
                                                             area=p['area'],
                                                             min_time=p['min_time']*3600,
                                                             time_tolerance=p['time_tolerance']*3600,
                                                             merge_tolerance=p['merge_tolerance'])
            predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
            hm=SegmentationEvaluation.harmonic_mean(ground_truth,predicted)
            hm_sum += hm
        print(p, "%.4f" % (hm_sum/len(train_dfs)))

        if hm_sum > hm_best:
            best_p = p
            hm_best = hm_sum
    print("*"*50)
    print("Best Parameters")
    print(best_p,"%.4f"%(hm_best/len(train_dfs)))
    print("*"*50)

    hm_sum=0
    cov_sum=0
    pur_sum=0
    for tdf in test_dfs:
        N = len(train_dfs)
        ts_obj = TrajectorySegmentation()
        ts_obj.load_data(lat='latitude', lon='longitude', time_date='time',
                         labels=['label'], seperator=';', src=tdf)
        segment_indexes, segments = ts_obj.segmentByLabel(label='label')
        ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
        segment_indexes, segments = ts_obj.segment_CBSMoT(max_dist=None,
                                                          area=p['area'],
                                                          min_time=p['min_time'] * 3600,
                                                          time_tolerance=p['time_tolerance'] * 3600,
                                                          merge_tolerance=p['merge_tolerance'])
        predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
        hm = SegmentationEvaluation.harmonic_mean(ground_truth, predicted)
        hm_sum += hm
        cov_sum += SegmentationEvaluation.coverage(ground_truth, predicted)[1]
        pur_sum += SegmentationEvaluation.purity(ground_truth, predicted)[1]
    results.append([hm_sum/len(test_dfs),pur_sum/len(test_dfs),cov_sum/len(test_dfs)])
print(results)
pd.DataFrame(results,columns=list('hpc')).to_csv('cbsmot_hurr.csv')
