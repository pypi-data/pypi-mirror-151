import numpy as np
from telescope_distance.utils import utils


def consistent_kmedoids(n_clusters, metric, series_list=None, pool_size=1):
    """ Clusters time-series with the consistent clustering algorithm presented in [1].


    Parameters
    ----------
    n_clusters : int
        number of clusters to find

    metric: callable, ndarray
        distance function to compute the pairwise distance between timeseries.
        Or a square ndarray of dissimilarities

    series_list : list, ndarray, None
        list of ndarray of shape=(sz, d)
        ndarray of shape=(n_ts, sz, d)
        Time series dataset.
        If metric is given in the form of a distance matrix, series_list is no longer required

    pool_size: int
        The size of multiprocessing pool to run distance matrix computations in parallel.

    Returns
    -------
    ndarray of shape (n_ts,)
        Cluster assignment

    Notes
    -----
    [1] Khaleghi, Azedeh, et al. "Consistent algorithms for clustering time series." Journal of Machine Learning Research 17.3 (2016): 1-32.
    """

    assert callable(metric) or isinstance(metric, np.ndarray), 'metric should be ndarray or a callable'
    if isinstance(metric, np.ndarray):
        assert metric.shape[0] == metric.shape[1], 'metric as a dissimilarity matrix should be squared'

    distance_mat = utils.pairwise_distance(series_list, metric, False, pool_size) if callable(metric) else metric

    centroids = [0]
    for k in range(1, n_clusters):
        min_dist_centroids = np.array([min([distance_mat[i, centroids[j]] for j in range(k)])
                                       for i in range(distance_mat.shape[0])])
        centroids.append(np.argmax(min_dist_centroids, keepdims=True)[0])

    labels = []
    for i in range(distance_mat.shape[0]):
        dist2centeroids = np.array([distance_mat[i, centroid] for centroid in centroids])
        labels.append(np.argmin(dist2centeroids, keepdims=True)[0])

    return np.array(labels)
