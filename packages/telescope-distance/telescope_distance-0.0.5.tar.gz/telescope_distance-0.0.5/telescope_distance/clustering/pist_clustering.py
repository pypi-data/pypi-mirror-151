import functools
from multiprocessing import Pool

import PyChest
import numpy as np
from sklearn import svm

from .kmedoids import consistent_kmedoids
from ..telescope import TelescopeDistance


def weights_fn(x):
    return x ** 2


def piecewise_stationary_clustering(n_clusters, series_list, change_point_param, n_change_point, core_distance_fn=None,
                                    pool_size=1):

    if not core_distance_fn:
        svm_kernel = 'rbf'
        max_iter = 500

        clf_constructor = functools.partial(svm.SVC,
                                            kernel=svm_kernel,
                                            max_iter=max_iter)

        core_distance_fn = TelescopeDistance(clf_constructor, weights_fn).distance

    distance_fn = functools.partial(_empirical_dist,
                                    change_point_param=change_point_param,
                                    n_change_point=n_change_point,
                                    distance_fn=core_distance_fn,
                                    pool_size=pool_size)

    return consistent_kmedoids(n_clusters, distance_fn, series_list)


def _empirical_dist(x, y, change_point_param, n_change_point, distance_fn, pool_size):

    x_estimates = sorted(PyChest.list_estimator(x, change_point_param)[:n_change_point])
    y_estimates = sorted(PyChest.list_estimator(y, change_point_param)[:n_change_point])

    def get_subseqs(_x, _x_estimates):
        return [_x[:_x_estimates[0]]] + \
                [_x[_x_estimates[i-1]: _x_estimates[i]] for i in range(1, len(_x_estimates))] + \
                [_x[_x_estimates[-1]:]]

    x_subseqs = get_subseqs(x, x_estimates)
    y_subseqs = get_subseqs(y, y_estimates)

    pdists = _pairwise_distance(x_subseqs, y_subseqs, distance_fn, pool_size)

    return pdists.min(axis=1).max() + pdists.min(axis=0).max()

def _pairwise_distance(x, y, distance_fn, pool_size):
    n = len(x)
    m = len(y)
    args = []
    for i in range(n):
        for j in range(m):
            args.append((x[i], y[j],))
    pool = Pool(pool_size)
    distance_arr = pool.starmap(distance_fn, args)
    return np.array(distance_arr).reshape((n, m))


