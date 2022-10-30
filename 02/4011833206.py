#!/usr/bin/python3.11

# Javad Bajelan - 4011833206

import cmath

print("-------------------------exercises1-------------------------")

print('ax² + bx + c = 0')
a, b, c = map(float, input('a b c: ').split(' '))
delta = (b**2) - (4*a*c)

x1 = (-b + cmath.sqrt(delta))/(2*a)
x2 = (-b - cmath.sqrt(delta))/(2*a)

if not x1.imag:
    x1 = x1.real

if not x2.imag:
    x2 = x2.real

print('x1 = {}\nx2 = {}'.format(x1, x2))

print("-------------------------exercises2-------------------------")

number = int(input('number: '))
answer = 0

while number:
    answer += number%10
    number //= 10

print(answer)

print("-------------------------exercises3-------------------------")

number = int(input('number: '))
answer = 0
n = 1

while n <= number:
    answer += n*n
    n += 1

print(answer)

"""
# Another solution:
# Time complexity: O(1)

number = int(input('number: '))
answer = number*(number+1)*(2 * number + 1)//6

print(answer)
"""

print("-------------------------exercises4-------------------------")

number = int(input('number: '))
answer = 0

for i in range(1, number+1):
    answer += i*i

print(answer)

print("-------------------------exercises5-------------------------")

number = int(input('number: '))
answer = 0

while number:
    answer *= 10
    answer += number%10
    number //= 10

print(answer)

"""
# Another solution:

number = input('number: ')
print(number[::-1])
"""
