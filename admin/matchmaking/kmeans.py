from sklearn.cluster import KMeans
import numpy as np
from itertools import cycle
from typing import List, Tuple


def calc_distance(x1: int, y1: int, a: int, b: int, c: int) -> float:
    ''' Calculate straight line distance between point and line to find Elbow Distance'''
    return np.abs((a * x1 + b * y1 + c)) / np.sqrt(a ** 2 + b ** 2)


def random_swap(list: list, indexM: int, indexN: int):
    '''Perform inplace random swap of a certain index between nested list at m and n'''
    randInt1, randInt2 = np.random.randint(0, min(len(list[indexM]), len(list[indexN])), 2)
    temp = list[indexM][randInt1]
    list[indexM][randInt1] = list[indexN][randInt2]
    list[indexN][randInt2] = temp
    return


def random_swaps(groups: list):
    ''' Executes 2 * length randomly selected inplace swaps from left half of
     distributions with right half of distributions'''
    numSwaps = len(groups) * 2
    swaps = 0
    while swaps < numSwaps:
        indexN = np.random.randint(0, len(groups) // 2)
        indexM = np.random.randint(len(groups) // 2, len(groups))
        random_swap(groups, indexM, indexN)
        swaps += 1


def distribute_groups(res: np.array, group_size: int, rem_size: int) -> list:
    '''
    Distribute to group sizes according to a clock cycle using arg value cycles
    '''
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
            myClass = next(clockiterator)
            if len(diction[myClass]) == 0:
                continue
            nextGroup.append(diction[myClass].pop())
            iterations += 1
            currGroup += 1
        groups.append(nextGroup)
    return groups


def find_group_size(n: int, min_groupsize: int, max_groupsize: int) -> Tuple[int, int]:
    '''
    Find the most optimal group size with least number of group members left out
    Uses min_size as minimum acceptable group size for last group
    '''
    group_size = -1  # if is -1, then reject some users
    rem_size = 0  # will be > 0 if not 0
    for i in range(max_groupsize, min_groupsize, -1):
        rem_size = n % i
        print(i, rem_size, min_groupsize)
        if rem_size >= min_groupsize:
            group_size = i
            break
    return group_size, rem_size


def kmeans_elbow(X: np.array) -> np.array:
    '''
    Perform Elbow finding algorithm for Kmeans Clustering Algorithm.
    See more here
    https://www.youtube.com/watch?v=_HiEJ20sQXQ&ab_channel=RANJIRAJ
    '''
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
    point_dist = np.argmax(list(map(lambda x, y: calc_distance(x, y, a, b, c), k, dist_point_from_cluster_centre)))
    km = KMeans(
        n_clusters=point_dist, init="k-means++",
        n_init=10, max_iter=300,
        tol=1e-04, random_state=0
    )
    km.fit(X)
    res = km.predict(X)
    return res


def kMeans(X: np.array, min_groupsize: int, max_groupsize: int) -> List[List[int]]:
    '''
    Overall Execution Algorithm
    1. Finds a balanced group size
    2. Seperate into groups of n clusters that best seperate the dataset of users
    3. Perform Random Swaps on the Dataset
    '''
    n = len(X)
    min_groupsize = 1
    group_size, rem_size = find_group_size(n, min_groupsize, max_groupsize)
    res = kmeans_elbow(X)
    groups = distribute_groups(res, group_size, rem_size)
    random_swaps(groups)
    return groups
