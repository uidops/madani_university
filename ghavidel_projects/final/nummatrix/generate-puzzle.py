#!/usr/bin/env python


import sys

import numpy as np

n, m = int(sys.argv[1]), int(sys.argv[2])
print('{},{}'.format(n, m))

matrix = np.random.choice(list(range(1, 10)), size=(n, m))
mask = np.random.choice([True, False], size=(n, m))
v = matrix * mask

print(*np.sum(v, axis=1).tolist(), sep=',')
print(*np.sum(v, axis=0).tolist(), sep=',')
for row in matrix:
    print(*row.tolist(), sep=',')

sys.stderr.write('the solutions must be:\n')
sys.stderr.write(str(v))
sys.stderr.write('\n')
