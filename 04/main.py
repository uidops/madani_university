#!/usr/bin/env python

print('---------------exercises1---------------')

array = list(map(int, input('array: ').split()))

for index in range(len(array)-1):
    array[index] = max(array[index+1:])

array[-1] = -1
print(array)


print('---------------exercises2---------------')

array = list(map(int, input('array: ').split()))

for index in range(len(array)):
    n = 0
    for jndex in range(index+1, len(array)):
        if array[index] > array[jndex]:
            n += 1

    array[index] = n

print(array)


print('---------------exercises3---------------')

matrix = []
n = int(input('the number of rows: '))
for _ in range(n):
    matrix.append(list(map(int, input(f'row {_}: ').split())))

for row in range(len(matrix)):
    for col in range(len(matrix[row])):
        if matrix[row][col] != matrix[col][row]:
            print(False)
            break

    else:
        continue

    break

else:
    print(True)


print('---------------exercises4---------------')

matrix = []
n = int(input('the number of rows: '))
for _ in range(n):
    matrix.append(list(map(int, input(f'row {_}: ').split())))

zero = sum(_.count(0) for _ in matrix)
if zero >= (len(matrix)*len(matrix[0]))/2:
    print(True)
else:
    print(False)


print('---------------exercises5---------------')

matrix = []
n = int(input('the number of rows: '))
for _ in range(n):
    matrix.append(list(map(int, input(f'row {_}: ').split())))

t, b, r, l = 0, len(matrix)-1, len(matrix[0])-1, 0

while t <= b and l <= r:
    for i in range(l, r+1):
        print(matrix[t][i], end=' ')

    for i in range(t+1, b+1):
        print(matrix[i][r], end=' ')

    if l < r and t < b:
        for i in range(r-1, l, -1):
            print(matrix[b][i], end=' ')

        for i in range(b, t, -1):
            print(matrix[i][l], end=' ')

    t, b, r, l = t+1, b-1, r-1, l+1

print()
