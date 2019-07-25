from CBSmot import CBSmot
from sklearn.model_selection import ParameterGrid
from TrajectorySegmentation import TrajectorySegmentation
import pandas as pd
import time

dfs = []
dfs.append(pd.read_csv('databases/Hurricanes/h_d1.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d2.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d3.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d4.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d5.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d6.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d7.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d8.txt',sep=';'))
dfs.append(pd.read_csv('databases/Hurricanes/h_d9.txt',sep=';'))
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


ts_obj=TrajectorySegmentation()
ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                 labels=['label'],seperator=';',src='databases/Hurricanes/h_d1.txt')
ts_obj=TrajectorySegmentation()
ts_obj.load_data(lat='latitude',lon='longitude',time_date='time',
                 labels=['label'],seperator=';',src=all_dfs[0])
a,b = ts_obj.segmentByStopMove(max_dist=100000, min_time=5, time_tolerance=100000, merge_tolerance=5)
print("Here we go")
print(type(a[0][0]))
print(type(b[0]))
print("Done")
exit()
cbsmot = CBSmot()
for i in range(0,len(dfs)):
    dataframes = split_df(dfs[i])
    lowest_cost = float('inf')
    for p in parm_grid:
        for df in dataframes:
            continue
    test_dfs = []
    for j in range(0, len(dfs)):
        if j != i:
            test_dfs+=split_df(dfs[j])
    #print("--- %s seconds ---" % (time.time() - start_time))

########################################################################################################################


