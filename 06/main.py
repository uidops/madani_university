#!/usr/bin/env python

import random
import sys

# sepal_length,sepal_width,petal_length,petal_width
eucidistance = lambda x, y: ((y['sepal_length'] - x['sepal_length'])**2 +
                            (y['sepal_width'] - x['sepal_width'])**2 +
                            (y['petal_length'] - x['petal_length'])**2 +
                            (y['petal_width'] - x['petal_width'])**2)**.5

def strtol(s='0'):
    try:
        s = float(s)
    except:
        pass

    return s


def read_csv(fname, sep=','):
    csv_data = []
    with open(fname) as f:
        keys = f.readline().strip().split(sep)
        for row in f:
            csv_data.append(dict(zip(keys, map(strtol, row.strip().split(sep)))))

    return csv_data


def means(cluster):
    data = dict()
    length = len(cluster)
    for record in cluster:
        for key, value in record.items():
            if type(value) == float:
                data[key] = data.get(key, 0) + value/length

    return data


def eucid_cluster(data, k):
    clusters = []
    x = []
    for _ in range(k):
        d = random.choice(data)
        while d in x:
            d = random.choice(data)

        x.append(d)
        clusters.append([])

    for record in data:
        n = (-1, sys.maxsize)
        for r in x:
            d = eucidistance(r, record)
            if n[1] > d:
                n = (x.index(r), d)

        clusters[n[0]].append(record)

    return clusters, x


def cluster_correction(data, x):
    for index, cluster in enumerate(data):
       x[index] = means(cluster)

    for index, cluster in enumerate(data):
        for record in cluster:
            n = (-1, sys.maxsize)
            for r in x:
                d = eucidistance(r, record)
                if n[1] > d:
                    n = (index, d)

            data[n[0]].append(record)
            data[index].remove(record)
            
    return data, x


if __name__ == '__main__':
    csv_data = read_csv('iris.csv')
    while True:
        data, x = eucid_cluster(csv_data, 3)
        data1, x1 = cluster_correction(data, x)
        while data != data1:
            data, x = data1, x1
            data1, x1 = cluster_correction(data, x)

        if len(data1[0]) == len(data1[1]) == len(data1[2]):
            print(f'**Cluster 1 {len(data1[0])}')
            for _ in data1[0]:
                print(_)

            print(f'\n** Cluster 2 {len(data1[1])}')
            for _ in data1[1]:
                print(_)

            print(f'\n** Cluster 3 {len(data1[2])}')
            for _ in data1[2]:
                print(_)

            break
