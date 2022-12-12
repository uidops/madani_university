#!/usr/bin/env python

import operator
import re
import secrets
import sys


# sepal_length, sepal_width, petal_length, petal_width, class
eucidistance = lambda x, y: ((y['sepal_length'] - x['sepal_length'])**2 +
                            (y['sepal_width']   - x['sepal_width'])**2 +
                            (y['petal_length']  - x['petal_length'])**2 +
                            (y['petal_width']   - x['petal_width'])**2)**.5


def strtol(s: str) -> float:
    if re.match('^[-+]?\d+(.\d+)?$', s):
        s = float(s)

    return s


def read_csv(pathname: str, sep=',') -> list:
    csv_data = []
    try:
        with open(pathname) as f:
            keys = f.readline().strip().split(sep)
            for row in f:
                csv_data.append(dict(zip(keys, map(strtol, row.strip().split(sep)))))

    except FileNotFoundError as err:
        sys.stderr.write(str(err)+'\n')
        sys.exit(1)

    return csv_data


def means(cluster: list) -> dict:
    data = dict()
    for key in cluster[0]:
        if type(cluster[0][key]) == float:
            data[key] = data.get(key, 0) + sum(map(operator.itemgetter(key), cluster))

    for key in data:
        data[key] = data[key]/len(cluster)

    return data


def eucid_cluster(data: list, k: int) -> tuple:
    clusters = []
    x = []
    for _ in range(k):
        d = secrets.choice(data)
        while d in x:
            d = secrets.choice(data)

        x.append(d)
        clusters.append([])

    for record in data:
        n = (None, sys.maxsize)
        for r in x:
            d = eucidistance(r, record)
            if n[1] > d:
                n = (x.index(r), d)

        clusters[n[0]].append(record)

    return clusters, x


def cluster_correction(data: list, x: list) -> tuple:
    for index, cluster in enumerate(data):
       x[index] = means(cluster)

    for index, cluster in enumerate(data.copy()):
        for record in cluster:
            n = (None, sys.maxsize)
            for r in x:
                d = eucidistance(r, record)
                if n[1] > d:
                    n = (index, d)

            if n[0] != index:
                data[n[0]].append(record)
                data[index].remove(record)
            
    return data, x


if __name__ == '__main__':
    csv_data = read_csv('iris.csv')
    secrets.SystemRandom().shuffle(csv_data)

    data, x = eucid_cluster(csv_data, 3)
    data1, x1 = cluster_correction(data, x)

    n = 0
    while n < 2:
        data, x = data1, x1
        data1, x1 = cluster_correction(data, x)
        if x == x1:
            n += 1

    for index, cluster in enumerate(data1):
        print('\n-- Cluster {}: {}'.format(index, len(cluster)))
        for _ in cluster:
            print(_)
