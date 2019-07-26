from SegmentationAlgorithms.CBSMoT import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import SegmentationEvaluation
import pandas as pd
from databases import load_datasets



dataset = load_datasets.DataEnum.GEOLIFE
algorithm = load_datasets.AlgoEnum.CBSMoT

data = load_datasets.get_data(dataset,algorithm)

dfs = data['data']
parameter_grid = data['parameter_grid']
file_name = data['file_name']
label = data['label']


print(file_name)

all_dfs = []


results = []
best_p = {}
for i in range(0,len(dfs)):
    hm_best = 0
    train_dfs = dfs[i]
    test_dfs = []
    for j in range(0, len(dfs)):
        if j!=i:
            test_dfs += dfs[j]
    for p in parameter_grid:
        hm_sum = 0
        for tdf in train_dfs:
            N = len(train_dfs)
            ts_obj=TrajectorySegmentation()
            ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                             labels=[label],seperator=';',src=tdf)
            segment_indexes,segments = ts_obj.segmentByLabel(label=label)
            ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
            segment_indexes,segments = ts_obj.segment_CBSMoT(max_dist=None,
                                                             area=p['area'],
                                                             min_time=p['min_time'],
                                                             time_tolerance=p['time_tolerance'],
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
                         labels=[label], seperator=';', src=tdf)
        segment_indexes, segments = ts_obj.segmentByLabel(label=label)
        ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
        segment_indexes, segments = ts_obj.segment_CBSMoT(max_dist=None,
                                                          area=p['area'],
                                                          min_time=p['min_time'],
                                                          time_tolerance=p['time_tolerance'],
                                                          merge_tolerance=p['merge_tolerance'])
        predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
        hm = SegmentationEvaluation.harmonic_mean(ground_truth, predicted)
        hm_sum += hm
        cov_sum += SegmentationEvaluation.coverage(ground_truth, predicted)[1]
        pur_sum += SegmentationEvaluation.purity(ground_truth, predicted)[1]
    results.append([hm_sum/len(test_dfs),pur_sum/len(test_dfs),cov_sum/len(test_dfs)])
print(results)
pd.DataFrame(results,columns=list('hpc')).to_csv(file_name)
