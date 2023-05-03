#!/usr/bin/env python

import math
import sys

def main():
    print('--------------exercises1--------------')
    num = int(input('num: '))
    print(math.trunc(math.sqrt(num)))

    print('--------------exercises2--------------')
    nums = list(map(lambda x: abs(int(x)), input('num1 num2: ').split()))[:2]
    if len(nums) < 2:
        print("Where's the second number?")
        sys.exit(1)

    nums.sort(reverse=True)
    while nums[1]:
        nums[0], nums[1] = nums[1], nums[0]%nums[1]

    print(nums[0])

# Another solution:

#    import math
#    print(math.gcd(*nums))

#    import numpy
#    print(numpy.gcd(*nums))


if __name__ == '__main__':
    main()
