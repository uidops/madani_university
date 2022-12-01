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

matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
print(matrix)

for col in range(len(matrix[0])):
    print(matrix[0][col], end=' ')

for row in range(1, len(matrix)):
    print(matrix[row][col], end=' ')

for col in range(len(matrix[row])-2, -1, -1):
    print(matrix[row][col], end=' ')

for row in range(len(matrix)-2, 0, -1):
    print(matrix[row][col], end=' ')

for col in range(1, len(matrix[row])-1):
    print(matrix[row][col], end=' ')

for row in range(2, len(matrix)-1):
    print(matrix[row][col], end=' ')

for col in range(1, len(matrix[row])-2):
    print(matrix[row][col], end=' ')

print()
