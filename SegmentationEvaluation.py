import numpy as np

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
