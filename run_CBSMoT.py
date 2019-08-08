from SegmentationAlgorithms.CBSMoT import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import SegmentationEvaluation
import pandas as pd
from databases import load_datasets
from datetime import datetime


dataset = load_datasets.DataEnum.HURRICANES
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
param_count = len(parameter_grid)
print("Number of Parameter Combinations:",param_count)
for i in range(0,len(dfs)):
    hm_best = 0
    train_dfs = dfs[i]
    test_dfs = []
    start_time = datetime.now()
    for j in range(0, len(dfs)):
        if j!=i:
            test_dfs += dfs[j]
    for p in parameter_grid:
        cov_sum = 0
        pur_sum = 0
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
            cov_sum += SegmentationEvaluation.coverage(ground_truth, predicted)[1]
            pur_sum += SegmentationEvaluation.purity(ground_truth, predicted)[1]
            #hm=SegmentationEvaluation.harmonic_mean(ground_truth,predicted)
            #hm_sum += hm
        cov_avg = cov_sum/len(train_dfs)
        pur_avg = pur_sum/len(train_dfs)
        hm = (2*cov_avg*pur_avg)/(cov_avg+pur_avg)
        print(p, "%.4f" % hm)
        if hm > hm_best:
            best_p = p
            hm_best = hm
    print("*"*50)
    print("Best Parameters")
    print(best_p,"%.4f"%(hm_best/len(train_dfs)))
    print("*"*50)

    hm_sum=0
    cov_sum=0
    pur_sum=0
    error_l1,error_l2=0,0
    for tdf in test_dfs:
        ts_obj = TrajectorySegmentation()
        ts_obj.load_data(lat='latitude', lon='longitude', time_date='time',
                         labels=[label], seperator=';', src=tdf)
        print(len(ts_obj.row_data))

        segment_indexes, segments = ts_obj.segmentByLabel(label=label)
        ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
        segment_indexes, segments = ts_obj.segment_CBSMoT(max_dist=None,
                                                          area=best_p['area'],
                                                          min_time=best_p['min_time'],
                                                          time_tolerance=best_p['time_tolerance'],
                                                          merge_tolerance=best_p['merge_tolerance'])
        predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
        hm = SegmentationEvaluation.harmonic_mean(ground_truth, predicted)
        hm_sum += hm
        cov_sum += SegmentationEvaluation.coverage(ground_truth, predicted)[1]
        pur_sum += SegmentationEvaluation.purity(ground_truth, predicted)[1]
        error_l1 += SegmentationEvaluation.error(ground_truth,predicted,method='l1')[1]
        error_l2 += SegmentationEvaluation.error(ground_truth,predicted,method='l2')[1]
    print("Fold",i,"Results")
    exec_time = datetime.now() - start_time

    avg_cov = cov_sum/len(test_dfs)
    avg_pur = pur_sum/len(test_dfs)
    hm = (2*avg_cov*avg_pur)/(avg_cov+avg_pur)
    error_l1 = error_l1/len(test_dfs)
    error_l2 = error_l2/len(test_dfs)
    print(hm,avg_pur,avg_cov)
    results.append([hm,avg_pur,avg_cov,error_l1,error_l2,exec_time.seconds,param_count])
print(results)
pd.DataFrame(results,columns=['h','p','c','l1','l2','fold_time','param_count']).to_csv(file_name)
