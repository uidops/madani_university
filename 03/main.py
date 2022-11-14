#!/usr/bin/env python

import math

def main():
    print('--------------exercises1--------------')
    num = int(input('num: '))
    print(math.trunc(math.sqrt(num)))

    print('--------------exercises2--------------')
    nums = list(map(lambda x: abs(int(x)), input('num1 num2: ').split()))[:2]
    if len(nums) < 2:
        print("Where's the second number?")
        exit(1)

    if not nums[0] or not nums[1]:
        print(max(nums))
        exit(0)

    nums.sort()
    rem = -1
    while rem:
        rem = nums[0]%nums[1]
        nums[0], nums[1] = nums[1], rem

    print(nums[0])

    """
    Another solution:
        import math
        print(math.gcd(*nums))

        import numpy
        print(numpy.gcd(*nums))
    """

if __name__ == '__main__':
    main()
