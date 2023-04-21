#!/usr/bin/env python

import math


class Cylinder:
    def __init__(self, r=0.0, h=0.0, pi=math.pi):
        self.r = r
        self.h = h
        self.pi = pi


    def side_area(self):
        return 2 * self.pi * self.r * (self.r + self.h)


    def volume(self):
        return self.pi * self.r * self.r * self.h


x = Cylinder(1, 4)

print(x.side_area())
print(x.volume())
