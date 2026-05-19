#!/usr/bin/env python
# source : https://numpy.org/doc/stable

import numpy

a = numpy.array([8, 5, 0, 4, 9, 6, 0, 0], dtype='<u1')  # 1-Byte little-endian unsigned integer linear array
# <                            : little-endian byteorder
# >                            : big-endian byteorder
# b, byte                      : signed byte
# B, ubyte                     : unsigned byte
# int                          : signed integer (8-Byte by default)
# i                            : signed integer (4-Byte by default)
# i1, int8                     : 1-Byte (08-Bit) signed integer
# i2, int16                    : 2-Byte (16-Bit) signed integer
# i4, int32                    : 4-Byte (32-Bit) signed integer
# i8, int64                    : 8-Byte (64-Bit) signed integer
# uint                         : unsigned integer (8-Byte by default)
# u1, uint8                    : 1-Byte (08-Bit) unsigned integer
# u2, uint16                   : 2-Byte (16-Bit) unsigned integer
# u4, uint32                   : 4-Byte (32-Bit) unsigned integer
# u8, uint64                   : 8-Byte (64-Bit) unsigned integer
# ?, bool                      : boolean (True or False)
# float                        : IEEE-754 floating-point number (8-Byte by default)
# f2, float16, half            : half precision IEEE-754 floating-point number
# f4, float32, single          : single precision IEEE-754 floating-point number
# f8, float64, double          : double precision IEEE-754 floating-point number
# f16, float128, longdouble    : long double precision IEEE-754 floating-point number
# complex                      : complex number (16-Byte by default)
# c8, complex64, csingle       : 08-Byte complex number
# c16, complex128, cdouble     : 16-Byte complex number
# c32, complex256, clongdouble : 32-Byte complex number
# U, unicode                   : unicode
# O                            : python objcet
# S, a                         : zero-terminated byte
# V                            : raw data


print(a)
print(a[0])
print(a * a)        # multiplication
print(a + a)        # addition
print(a ^ (2 * a))  # exclusive Or
print(a > 3)        # compare

print(a.dtype)  # data type
print(a.ndim)   # number of dimensions
print(a.shape)  # number of elements

print(a.newbyteorder('big'))  # big-endian byte order

print(a.max())  # maximum of the array
print(a.min())  # minimum of the array
print(a.sum())  # sum of the array
print(a.mean())  # mean of the array

print(numpy.where(a == a.min())[0][0])  # index of the minimum of the array

print(numpy.split(a, 2))                      # split an array into multiple sub-arrays as views into ary
print(numpy.array_split(a, 2))                # split an array into multiple sub-array
print(numpy.partition(a, 1))                  # partition the array by the element at index 1
print(numpy.sort(a))                          # sort the array (quicksort, smallest to largest)
print(numpy.sort(a, kind='mergesort')[::-1])  # sort the array (mergesort, largest to smallest)
print(numpy.unique(a))                        # find the unique elements of an array

print(numpy.count_nonzero(a))      # number of elements that are nonzero
print(numpy.count_nonzero(a > 5))  # number of elements that are greater than 5
print(numpy.nonzero(a))            # index of elements that aree nonzero
print(numpy.nonzero(a > 5))        # index of elements that are greater than 5
print(a[numpy.nonzero(a)])         # only non-zero elements

print(numpy.pad(a, (0, 5), 'constant', constant_values=(0xff)))  # padding
print(numpy.pad(a, (3, 2), 'constant', constant_values=(0x1f, 0xff)))
print(numpy.pad(a, (5, 5), 'edge'))
print(numpy.pad(a, (1, 0), 'maximum'))
print(numpy.pad(a, (4, 1), 'median'))
print(numpy.pad(a, (4, 5), 'symmetric'))
print(numpy.pad(a, (5, 4), 'wrap'))

# modes:
#   constant    : pads with a constant value (default)
#   edge        : pads with the edge values of array
#   linear_ramp : pads with the linear ramp between 'end_value' and the array edge value
#   maximum     : pads with the maximum value
#   minimum     : padd with the minimum value
#   mean        : pads with the mean value
#   median      : pads with the median value
#   reflect     : pads with the reflection of the vector mirrored on the first and last values
#   symmetric   : pads with the reflection of the vector mirrored along the edge of the array
#   wrap        : pads with the wrap of the vector along the axis
#                 the first values are used to pad the end and the end values are used to pad the beginning
#   empty       : pads with undefined values
# also can be a function:


def pad_func(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('pad_value', 0xff)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value


print(numpy.pad(a, (0, 10), pad_func, pad_value=0xff))


print(numpy.arange(10))  # array from a range
print(numpy.arange(5, 10))
print(numpy.arange(0, 1, 0.1))

print(numpy.linspace(0, 1, num=5))           # return evenly spaced numbers over a specified interval
print(numpy.logspace(1, 2, num=3, base=10))  # return numbers spaced evenly on a log scale
#                                              base ** start -> base ** end
#                                              base is 10 by default

print(numpy.empty(20))      # create an empty array of given shape (values are undefined behavior)
print(numpy.empty(30, dtype='u2'))
print(numpy.empty_like(a))  # create an empty array from a given array

print(numpy.zeros(30, dtype='f'))  # create a zero array of given shape
print(numpy.zeros_like(a))         # create a zero array from a given array

print(numpy.ones(30))      # create an empty array of given shape with one
print(numpy.ones_like(a))  # create an empty array from a given array with one

print(numpy.full(5, 0xff))       # create a new array and filled with a given value
print(numpy.full_like(a, 0x1f))  # create a new array and filled with a given value from a given array

print(numpy.repeat(0, 5))  # repeat elements of an array
print(numpy.repeat(a, 5))

print(numpy.invert(numpy.zeros(10, dtype='u2')))               # one’s complement of the elements
print(numpy.left_shift(numpy.ones(10, dtype='u2'), 4))         # perform left shift on elements of the array
print(numpy.right_shift(numpy.full(10, 0x10, dtype='u2'), 2))  # perform right shift on elements of the array


# -------------------------------------------------


a = numpy.array([
    [0x01, 0x02, 0x03, 0x04],
    [0x05, 0x06, 0x07, 0x08],
    [0x09, 0x0a, 0x0b, 0x0c],
    [0x0d, 0x0e, 0x0f, 0x10],
])

print(a)
print(a[0])
print(a[0][0])
print(a[1, 2])  # same as a[1][2]
print(a[:, ::2])
print(a[0:2, 2:])

print(a.ndim)
print(a.shape)

print(a.T)  # view of the transposed array

b = numpy.mat([
    [0x01, 0x02, 0x03, 0x04],
    [0x05, 0x06, 0x07, 0x08],
    [0x09, 0x0a, 0x0b, 0x0c],
    [0x0d, 0x0e, 0x0f, 0x10],
])

print(a == b)
print(type(a) == type(b))

print(numpy.rot90(a))  # rotate 90 degree

print(numpy.empty((2, 2)))
print(numpy.zeros((2, 2)))
print(numpy.ones((5, 3)))
print(numpy.full((3, 6), 8))

print(numpy.eye(7, dtype='u2'))  # create an identity-like matrix (can be a non-square matrix)
print(numpy.eye(3, 4, dtype='u2'))

print(numpy.identity(4, dtype='u2'))  # create an identity matrix (always a square matrix)

print(numpy.moveaxis(a, [0, 1], [-1, -2]))  # move axes of an array to new positions
print(numpy.transpose(a))  # transposed axes
print(numpy.swapaxes(a, 0, 1))  # move axes of an array to new positions

b = numpy.full((4, 4), 3)
print(a + b)
print(a * b)
print(numpy.mat(a) * numpy.mat(b))
print(numpy.inner(a, b))  # inner product of two arrays
print(numpy.dot(a, b))    # dot product of two arrays

x = numpy.zeros(4)
y = numpy.ones(4)

print(numpy.stack((x, y), axis=1))  # join a sequence of arrays along a new axis

print(numpy.repeat(a, 2, axis=1))
print(numpy.repeat(a, (1, 2, 3, 4), axis=1))

print(numpy.delete(a, 1, axis=0))  # return a new array with sub-arrays along an axis deleted
print(numpy.delete(a, 1, axis=1))

print(numpy.apply_over_axes(numpy.sum, a, 1))

print(numpy.random.rand(3, 3))  # random array in a given shape
print(numpy.random.randint(1, 3, (3, 3)))  # random integers from 1 to 3 in a given shape

mu, sigma = 0, 0.1                              # mean and standard deviation
print(numpy.random.normal(mu, sigma, (2, 10)))  # normal (gaussian) distribution


b = numpy.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
])

print(b)
numpy.random.shuffle(b)  # shuffle the array
print(b)

b = numpy.array([1, 2, 3, 4])
c = numpy.full(4, 2)
print(numpy.outer(c, b))  # outer product of two arrays


# ----------

a = numpy.array([
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ],
    [
        [10, 11, 12],
        [13, 14, 15],
        [16, 17, 18],
    ],
    [
        [19, 20, 21],
        [22, 23, 24],
        [25, 26, 27],
    ]
])

print(a)
print(a.ndim)
print(a.shape)

print(a[0])
print(a[0][0])
print(a[0][0][0])
print(a[0, 1, 2])
print(a[:, 1:, 1:3])
print(a[a % 2 == 0])
