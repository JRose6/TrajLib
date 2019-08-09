import numpy as np
import math

class DBSMoT:

    def segment(self,traj,min_dir_change,min_time,max_tolerance):
        variation = self.compute_variation(traj.row_data)
        stops = self.find_stops(traj.row_data,variation,min_dir_change,min_time,max_tolerance)
        moves = []
        moves = self.find_moves(stops,len(variation))
        clusters = stops+moves
        clusters.sort(key=lambda x: x[0])
        return clusters


    def compute_variation(self,traj):
        n = len(traj)
        bearing,variation = np.zeros(n),np.zeros(n)
        for i in range(1, n):
            bearing[i] = self.calculate_bearing(traj.iloc[i-1], traj.iloc[i])
            variation[i] = abs(bearing[i]-bearing[i-1])
        variation[0] = variation[1]
        return variation

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

    def find_stops(self,traj,variation,min_dir_change,min_time,max_tolerance):
        all_clusters = []
        n = len(variation)
        i=0
        cluster = []
        opened = False
        while(i<n):
            if variation[i] > min_dir_change:
                cluster.append(i)
                opened=True
            elif opened:
                end = self.look_ahead(i,variation,min_dir_change,max_tolerance)
                if end < i+max_tolerance:
                    cluster += list(range(i,end+1))
                    i = end
                else:
                    start_time = traj.iloc[cluster[0]]['time_date']
                    end_time = traj.iloc[cluster[len(cluster)-1]]['time_date']
                    delta = end_time-start_time
                    if (delta.seconds>min_time):
                        all_clusters.append((cluster[0],cluster[len(cluster)-1]))
                    cluster=[]
                    opened=False
            i+=1
        return all_clusters

    def look_ahead(self,current_index,variation,
                   min_dir_change,max_tolerance):
        i=current_index
        while(i<current_index+max_tolerance and i<len(variation)):
            if variation[i] > min_dir_change:
                break
            i+=1
        return i


    def find_moves(self,stops,size):
        moves = []
        start = 0

        for i in range(len(stops)):
            end = stops[i][0]-1
            if start < end:
                moves.append((start,end))
            start = stops[i][1]+1
        end = size
        if start<end:
            moves.append((start, end))
        return moves