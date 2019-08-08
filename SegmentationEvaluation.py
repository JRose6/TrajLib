import numpy as np
import math


def purity( ground_truth, labels):
    avg = []
    ground_truth = np.array(ground_truth)
    labels = np.array(labels)
    for ts in set(labels):
        ma = 0
        g = ground_truth[(np.where(labels == ts)[0])]
        for tp in set(g):
            _ = len(np.where(g == tp)[0])
            if _ > ma:
                ma = _
        if ts != -1:
            avg.append(ma * 1.0 / len(g))
    return avg, np.mean(np.array(avg))


def coverage(ground_truth, labels):
    cov = []
    labels = np.array(labels)
    ground_truth = np.array(ground_truth)
    for ts in set(ground_truth):
        mx = 0
        g = labels[(np.where(ground_truth == ts)[0])]
        for l in set(g):
            _ = len(np.where(g == l)[0])
            if mx <= _:
                mx = _
        cov.append(mx * 1.0 / len(g))
    return cov, np.mean(np.array(cov))

def harmonic_mean(ground_truth,prediction):
    cov = coverage(ground_truth, prediction)[1]
    pur = purity(ground_truth, prediction)[1]
    return (2*cov*pur)/(cov+pur)


def error(truth,predicted,method='l2'):
    f = abs if method=='l1' else lambda x: math.pow(x,2)
    start_truth = 0
    start_pred = 0
    truth_tuples, pred_tuples =[],[]
    for i in range(len(truth)-1):
        if truth[i]!=truth[i+1]:
            truth_tuples.append((start_truth,i))
            start_truth=i+1
        if predicted[i]!=predicted[i+1]:
            pred_tuples.append((start_pred,i))
            start_pred = i+1
    truth_tuples.append((start_truth,i))
    pred_tuples.append((start_pred,i))
    error = 0
    errors = []
    for t in truth_tuples:
        distances = []
        for p in pred_tuples:
            distances.append(abs(t[0]-p[0])+abs(t[1]-p[1]))
        m = np.min(distances)
        errors.append(f(m))
        error+=f(m)
    return errors,error/len(truth_tuples)