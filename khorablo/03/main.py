#!/usr/bin/env python

from math import sqrt

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
    answers = {}
    for key, value in colors.items():
        answers[key] = sqrt((color['R'] - value['R'])**2 +
                             (color['G'] - value['G'])**2 +
                             (color['B'] - value['B'])**2)

    answers = dict(sorted(answers.items(), key=lambda x: x[1]))
    keys, values = tuple(answers.keys()), tuple(answers.values())
    return None if values[0] == values[1] else keys[0]


color = dict(zip(('R', 'G', 'B'), map(int, input('R G B: ').split())))
print(detect_color(color))
