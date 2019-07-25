import numpy as np
import math

class DBSmot:
    def segment(self,traj,min_dir_change,min_time,max_tolerance):
        variation = self.compute_variation(traj)
        print(np.max(variation))

    def compute_variation(self,traj):
        n = len(traj)
        variation = np.zeros(n)
        for i in range(1, n):
            variation[i] = abs(variation[i - 1] - self.calculate_bearing(traj.iloc[i - 1], traj.iloc[i]))
        print(variation[155])

    def calculate_bearing(self,p1,p2):
        lat1 = math.radians(p1['lon'])
        lat2 = math.radians(p2['lon'])
        diffLong = math.radians(p1['lat'] - p2['lat'])
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                               * math.cos(lat2) * math.cos(diffLong))
        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    def find_clusters(self,traj,variation,min_dir_change,min_time,max_tolerance):
        all_clusters = []
        n = len(traj)
        i=0
        cluster_start = 0
        cluster_end = 0
        while(i<n):
            if variation[i] > min_dir_change:
                pass
