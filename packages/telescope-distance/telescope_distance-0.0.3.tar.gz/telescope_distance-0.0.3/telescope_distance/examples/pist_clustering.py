import functools
from multiprocessing import Pool

import PyChest
from scipy.spatial.distance import squareform
from sklearn import svm
from telescope_distance.utils import utils

from telescope_distance.clustering.pist_clustering import piecewise_stationary_clustering
from telescope_distance.generators import generators
import numpy as np
from scipy import stats
import os.path
from telescope_distance.clustering import agglomerative, kmedoids
from telescope_distance.telescope import TelescopeDistance
from telescope_distance.utils.utils import clustering_accuracy

from scipy import stats

import warnings
warnings.filterwarnings("ignore")

def weights_fn(x):
    return x ** 2

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


def piecewise_stationary_dataset(class_population, series_length, all_dists, file_name=None):

    if file_name:
        if os.path.exists(f'{file_name}.csv') and os.path.exists(f'{file_name}.shape'):
            return generators.read_from_file(file_name)

    data = []
    alpha = 1
    for dists in all_dists:
        for _ in range(class_population):
            min_dist, _data = generators.generate_piecewise_stationary_series(series_length, dists)
            alpha = min(alpha, min_dist)
            data += [_data]

    if file_name:
        generators.write_to_file(file_name, data)

    return alpha, data

class_population = 10
series_length = 2000
n_change_point = 1
all_dists = [[generators.MarkovChain(2, 5).generate_sample_path for _ in range(n_change_point+1)],
             [generators.MarkovChain(2, 4).generate_sample_path for _ in range(n_change_point+1)]]
alpha, data = piecewise_stationary_dataset(class_population, series_length, all_dists)

change_param = alpha * 0.75

svm_kernel = 'rbf'
max_iter = 300
clf_constructor = functools.partial(svm.SVC,
                                    kernel=svm_kernel,
                                    max_iter=max_iter)
TD = TelescopeDistance(clf_constructor, weights_fn)

core_distance_fn = TD.distance

distance_fn = functools.partial(_empirical_dist,
                                change_point_param=change_param,
                                n_change_point=n_change_point,
                                distance_fn=core_distance_fn,
                                pool_size=3)
print(distance_fn(data[0], data[1]))

distance_mat = utils.pairwise_distance(data, distance_fn, False, 1)
print(distance_mat)
#
# print(piecewise_stationary_clustering(2, data, change_param, 1, core_distance_fn, pool_size=3))
#
#
#
#
