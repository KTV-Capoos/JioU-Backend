from sklearn.cluster import KMeans
import numpy as np
from itertools import cycle

import django
import matplotlib.pyplot as plt
import time


def calc_distance(x1, y1, a, b, c):
    return np.abs((a * x1 + b * y1 + c )) / np.sqrt(a**2 + b ** 2)

def random_swap(list: list,m :int , n:int):
    a, b =np.random.randint(0, min(len(list[m]), len(list[n])), 2)
    temp = list[m][a]
    list[m][a] = list[n][b]
    list[n][b] = temp
    return

def random_swaps(groups):
    numSwaps = len(groups) * 2
    swaps = 0
    while swaps < numSwaps:
        n = np.random.randint(0, len(groups) // 2)
        m = np.random.randint(len(groups) // 2, len(groups))
        random_swap(groups, m, n)
        swaps += 1

def distribute_groups(res, group_size, rem_size):
    n = len(res)
    diction = {}
    for i in range(len(set(res))):
        diction[i] = list(np.argwhere(res == i).T.flatten())
    clockiterator = cycle(set(res))
    iterations = 0
    groups = []
    numGroups = n // group_size + (1 if rem_size > 0 else 0)
    while len(groups) < numGroups:
        nextGroup = []
        currGroup = 0
        while currGroup < group_size and iterations < n:
            myClass = clockiterator.__next__()
            if len(diction[myClass]) == 0:
                continue
            nextGroup.append(diction[myClass].pop())
            iterations += 1
            currGroup += 1
            # print(iterations, currGroup)
        groups.append(nextGroup)
    return groups

def find_group_size(n, min_groupsize, max_groupsize):
    group_size = -1  # if is -1, then reject some users
    rem_size = 0  # will be > 0 if not 0
    for i in range(max_groupsize, min_groupsize, -1):
        rem_size = n % i
        print(i, rem_size, min_groupsize)
        if rem_size >= min_groupsize:
            group_size = i
            break
    return group_size, rem_size

def kNN_with_elbow(X, min_groupsize, max_groupsize):

    n = len(X)
    min_groupsize = 1
    group_size, rem_size = find_group_size(n, min_groupsize, max_groupsize)
    dist_point_from_cluster_centre = []
    k = list(range(1, 11))
    for i in k:
        km = KMeans(
            n_clusters=i, init="k-means++",
            n_init=10, max_iter=300,
            tol=1e-04, random_state=0
        )
        km.fit(X)
        dist_point_from_cluster_centre.append(km.inertia_)
    a = dist_point_from_cluster_centre[0] - dist_point_from_cluster_centre[-1]
    b = k[-1] - k[0]
    c = (k[0] * dist_point_from_cluster_centre[-1]) - (k[8] * dist_point_from_cluster_centre[0])
    point_dist = np.argmax(list(map(lambda x, y: calc_distance(x, y, a, b, c), k, dist_point_from_cluster_centre )))
    km = KMeans(
            n_clusters=point_dist, init="k-means++",
            n_init=10, max_iter=300,
            tol=1e-04, random_state=0
        )
    km.fit(X)
    res = km.predict(X)
    groups = distribute_groups(res, group_size, rem_size)
    final_grouping = random_swaps(groups)
    return final_grouping
    # make json with

