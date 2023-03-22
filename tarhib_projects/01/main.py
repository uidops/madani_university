#!/usr/bin/env python

a = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

b = [[10, 11, 12],
     [13, 14, 15],
     [16, 17, 18]]

c = []
for row in a:
    c.append([])
    for icol in range(len(b[0])):
        c[-1].append(sum(map(lambda x, y: x*y, row, tuple(e[icol] for e in b))))

print(c)


print('\n-------------------------------\n')


rainfall = [('Mapaloa', [87, 88, 89]),
            ('Matale' , [135, 139, 61])]

res = []
for x, y in rainfall:
    res.append((x, sum(y)/len(y)))

print(res)


print('\n-------------------------------\n')


my_array = (9, 6, 7, 4, 3, 18, 9, 10)
my_array = my_array[:3] + my_array[4:]
print(my_array)

# my_array = (9, 6, 7, 4, 3, 18, 9, 10)
# my_array = list(my_array)
# my_array.remove(4)
# my_array = tuple(my_array)
# print(my_array)

# my_array = (9, 6, 7, 4, 3, 18, 9, 10)
# my_array = tuple(filter((4).__ne__, my_array))
# print(my_array)
