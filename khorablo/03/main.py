#!/usr/bin/env python

l1 = list(map(int, input().split())) + [0]
l2 = list(map(int, input().split())) + [0]
l3 = list(map(int, input().split())) + [0]
l = [l1, l2, l3, [0]*len(l1)]

k = [[], [], []]
for irow in range(len(l)-1):
    for icol in range(len(l[0])-1):
        k[irow].append(l[irow+1][icol] + l[irow-1][icol] + l[irow][icol+1] + l[irow][icol-1])

print()
for row in k:
    print(*row)
