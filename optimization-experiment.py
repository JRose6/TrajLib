from SegmentationAlgorithms.CBSMoT import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import SegmentationEvaluation
import pandas as pd
from databases import load_datasets
from bayes_opt.bayesian_optimization import BayesianOptimization


dataset = load_datasets.DataEnum.FISHING
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

def optimze_test(area, min_time):
    hm = 0
    for tdf in train_dfs:
        ts_obj = TrajectorySegmentation()
        ts_obj.load_data(lat='latitude', lon='longitude', time_date='time',
                         labels=[label], seperator=';', src=tdf)
        segment_indexes, segments = ts_obj.segmentByLabel(label=label)
        ground_truth = TrajectorySegmentation.get_segment_labels(segment_indexes)
        segment_indexes, segments = ts_obj.segment_CBSMoT(max_dist=None,
                                                          area=area,
                                                          min_time=min_time*3600,
                                                          time_tolerance=0,
                                                          merge_tolerance=0)

        predicted = TrajectorySegmentation.get_segment_labels(segment_indexes)
        hm += SegmentationEvaluation.harmonic_mean(ground_truth, predicted)
    return hm


pbounds = {
    'area': (0.01, 1),
    'min_time': (0.1, 24),
}

optimizer = BayesianOptimization(
    f=optimze_test,
    pbounds=pbounds,
    random_state=1,
)
for t in dfs:
    train_dfs = t
    print(len(train_dfs))
    optimizer = BayesianOptimization(
        f=optimze_test,
        pbounds=pbounds,
        random_state=1,
    )
    optimizer.maximize(init_points=5, n_iter=20)
    print(optimizer.max)

