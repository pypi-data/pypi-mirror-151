from multiprocessing import Pool

import numpy as np
from scipy.spatial.distance import squareform

from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment as linear_assignment



def pairwise_distance(series_list, distance_fn, condensed_form=True, pool_size=1):
    n = len(series_list)
    distance_vec = np.zeros(n * (n - 1) // 2)

    if pool_size > 1:
        args = []
        idx_mapping = {}
        idx_counter = 0
        for i in range(n):
            for j in range(i + 1, n):
                args.append((series_list[i], series_list[j],))
                idx_mapping[idx_counter] = n * i + j - ((i + 2) * (i + 1)) // 2
                idx_counter += 1
        pool = Pool(pool_size)
        distance_arr = pool.starmap(distance_fn, args)
        for i, val in enumerate(distance_arr):
            distance_vec[idx_mapping[i]] = val

    else:
        for i in range(n):
            for j in range(i + 1, n):
                idx = n * i + j - ((i + 2) * (i + 1)) // 2
                distance_vec[idx] = distance_fn(series_list[i], series_list[j])

    if condensed_form:
        return distance_vec
    return squareform(distance_vec, 'tomatrix')


def clustering_accuracy(cluster_assignments, labels):
    cm = confusion_matrix(labels, cluster_assignments)

    def _convert_to_cost_form(_cm):
        s = np.max(_cm)
        return s - _cm
    row_ind, col_ind = linear_assignment(_convert_to_cost_form(cm))
    return cm[row_ind, col_ind].sum() / cm.sum()

