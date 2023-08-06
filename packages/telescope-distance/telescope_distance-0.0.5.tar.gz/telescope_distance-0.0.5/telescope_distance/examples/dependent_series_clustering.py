import functools

from scipy.spatial.distance import squareform
from sklearn import svm


from telescope_distance.generators import generators
import numpy as np
from scipy import stats
import os.path
from telescope_distance.clustering import agglomerative, kmedoids
from telescope_distance.telescope import TelescopeDistance

import warnings
warnings.filterwarnings("ignore")


def irrational_rotation_dataset(file_name):
    if os.path.exists(f'{file_name}.csv') and os.path.exists(f'{file_name}.shape'):
        return generators.read_from_file(file_name)
    else:
        raise Exception(f"{file_name} dataset doesn't exist")


def irrational_rotation_dataset(class_population, series_length, alphas, dist1, dist2, file_name=None):
    if file_name:
        if os.path.exists(f'{file_name}.csv') and os.path.exists(f'{file_name}.shape'):
            return generators.read_from_file(file_name)

    data = []
    for alpha in alphas:
        data += [generators.generate_irrational_rotation_series(alpha, series_length, dist1, dist2)
                 for i in range(class_population)]
    if file_name:
        generators.write_to_file(file_name, data)

    return data


def markovian_dataset(file_name):
    if os.path.exists(f'{file_name}.csv') and os.path.exists(f'{file_name}.shape'):
        return generators.read_from_file(file_name)
    else:
        raise Exception(f"{file_name} dataset doesn't exist")


def markovian_dataset(class_population, series_length, MCs, hidden=False, distributions=None, file_name=None):

    if file_name:
        if os.path.exists(f'{file_name}.csv') and os.path.exists(f'{file_name}.shape'):
            return generators.read_from_file(file_name)

    data = []
    for i, mc in enumerate(MCs):
        if hidden:
            data += [mc.generate_hidden_markov_sample_path(series_length, distributions[i]) for _ in range(class_population)]
        else:
            data += [mc.generate_sample_path(series_length) for _ in range(class_population)]

    if file_name:
        generators.write_to_file(file_name, data)

    return data


# Weights generator function associated with telescope distance must be written in form of a function not a lambda.
# Because of the multiprocessing used in this implementation, weights_fn should be able to be pickled.
def weights_fn(x):
    return x ** 2


if __name__ == "__main__":
    class_population = 10
    series_length = 2000
    # synthetic dataset used in <https://www.jmlr.org/papers/volume14/ryabko13a/ryabko13a.pdf> experiments.
    dist1 = stats.multivariate_normal(np.zeros(3), np.eye(3) * 0.25)
    dist2 = stats.multivariate_normal(np.ones(3), np.eye(3) * 0.25)
    hir_data = np.array(irrational_rotation_dataset(class_population,
                                                series_length,
                                                [np.pi / 10,(np.pi + 0.4) / 10],
                                                dist1,
                                                dist2))


    svm_kernel = 'rbf'
    max_iter = 500

    clf_constructor = functools.partial(svm.SVC,
                                        kernel=svm_kernel,
                                        max_iter=max_iter)
    TD = TelescopeDistance(clf_constructor, weights_fn)

    distances = TD.pairwise_distance(hir_data, False, 3)

    clusters = agglomerative.agglomerative_clustering(2, distances)
    print(clusters)

    km_clusters = kmedoids.kmedoids_clustering(2, distances)
    print(km_clusters)

    consistent_clustering = kmedoids.consistent_kmedoids(2, distances)
    print(consistent_clustering)