#!/usr/bin/python

import cmath
import sys

__all__ = ['roots']

def roots(a, b, c):
    delta = (b**2) - (4*a*c)

    x1 = (-b + cmath.sqrt(delta))/(2*a)
    x2 = (-b - cmath.sqrt(delta))/(2*a)

    if not x1.imag: x1 = x1.real
    if not x2.imag: x2 = x2.real

    return x1, x2


def main():
    print('ax² + bx + c = 0')
    try:
        a, b, c = map(float, input('a b c: ').split(' '))
    except ValueError:
        print('Inputs are not numbers')
        sys.exit(1)

    if not a:
        print('Can you divide a number by zero?')
        sys.exit(1)

    result = roots(a, b, c)
    print('', result[0], result[1], sep='\n')


if __name__ == '__main__':
    main()
