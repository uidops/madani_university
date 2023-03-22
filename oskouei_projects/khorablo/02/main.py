#!/usr/bin/env python

from math import sqrt
import sys

colors = {
        "lightsalmon": {"R": 255, "G": 160, "B": 122},
        "salmon": {"R": 250, "G": 128, "B": 114},
        "darksalmon": {"R": 233, "G": 150, "B": 122},
        "lightcoral": {"R": 240, "G": 128, "B": 128},
        "indianred": {"R": 205, "G": 92, "B": 92},
        "red": {"R": 255, "G": 0, "B": 0},
        #"white": {"R": 255, "G": 255, "B": 255},
        #"black": {"R": 0, "G": 0, "B": 0},
}


def detect_color(color):
    answer = None, 442
    for key, value in colors.items():
        x = sqrt((color['R'] - value['R'])**2 +
                             (color['G'] - value['G'])**2 +
                             (color['B'] - value['B'])**2)

        if x == answer[1]:
            answer = None, None
            break

        answer = (key, x) if x < answer[1] else answer

    return answer[0]


if sys.stdin.isatty():
    color = dict(zip(('R', 'G', 'B'), map(int, input('R G B: ').split())))
else:
    color = dict(zip(('R', 'G', 'B'), map(int, sys.stdin.read().split())))

print(detect_color(color))
