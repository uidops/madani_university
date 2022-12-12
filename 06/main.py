#!/usr/bin/env python

import math
import operator
import re
import secrets


def strtol(s: str) -> float:
    if re.match('^[-+]?\d+(.\d+)?$', s):
        s = float(s)

    return s


def read_csv(pathname: str, sep=',') -> list:
    csv_data = list()
    with open(pathname, 'r') as f:
        keys = f.readline().strip().split(sep)
        for row in f:
            csv_data.append(dict(zip(keys, map(strtol, row.strip().split(sep)))))

    return csv_data


def eucidistance(x: dict, y: dict) -> float:
    distance = 0
    for key in x.keys():
        if type(x[key]) == float:
            distance += math.pow(y[key] - x[key], 2)

    return math.sqrt(distance)


def means(cluster: list) -> dict:
    data = dict()
    for key in cluster[0]:
        if type(cluster[0][key]) == float:
            data[key] = data.get(key, 0) + sum(map(operator.itemgetter(key), cluster))

    for key in data:
        data[key] = data[key]/len(cluster)

    return data


def cluster_correction(clusters: list, x: list) -> tuple:
    for index, cluster in enumerate(clusters):
       x[index] = means(cluster)

    for index, cluster in enumerate(clusters.copy()):
        for record in cluster:
            n = (None, math.inf)
            for i, r in enumerate(x):
                d = eucidistance(r, record)
                if d < n[1]:
                    n = (i, d)

            clusters[n[0]].append(record)
            clusters[index].remove(record)

    return clusters, x


def k_means(data: list, k: int) -> tuple:
    clusters = [list() for _ in range(k)]
    x = secrets.SystemRandom().sample(data, k)

    for record in data:
        n = (None, math.inf)
        for i, r in enumerate(x):
            d = eucidistance(r, record)
            if d < n[1]:
                n = (i, d)

        clusters[n[0]].append(record)

    clusters1, x1 = cluster_correction(clusters, x)
    n = 0
    while n < 2:
        clusters, x = clusters1, x1
        clusters1, x1 = cluster_correction(clusters, x)
        if x == x1:
            n += 1

    return clusters1


if __name__ == '__main__':
    csv_data = read_csv('iris.csv')
    secrets.SystemRandom().shuffle(csv_data)

    clusters = k_means(csv_data, 3)
    for index, cluster in enumerate(clusters):
        print('\n-- Cluster {}: {}'.format(index, len(cluster)))
        for _ in cluster:
            print(_)
