#!/usr/bin/env python

l1 = [0] + list(map(int, input().split()))
l2 = [0] + list(map(int, input().split()))
l3 = [0] + list(map(int, input().split()))
l = [l1, l2, l3, [0]*4]

print()
for irow in range(3):
    for ielem in range(1, 4):
        print(l[irow+1][ielem] + l[irow-1][ielem] + l[irow][(ielem+1)&3] + l[irow][(ielem-1)&3], end=' ')

    print()
