#!/usr/bin/env python

import math
import operator
import os
import secrets
import sys
import time
print('--------------------exercises6--------------------')

players = ('U', 'C', '0')
func = (min, max)

def print_matrix(matrix: list) -> None:
    os.system('clear' if os.name == 'posix' else 'cls')
    for _ in matrix:
        print(*_)


def evaluation(matrix: list) -> int:
    o, c = [], []
    stat = 0
    for row in range(length):
        x = matrix[row]
        y = list(map(operator.itemgetter(row), matrix))
        if [players[1]]*length in (x, y):
            return 1
        elif [players[0]]*length in (x, y):
            return -1
        elif players[2] in x:
            stat = 2

        o.append(matrix[row][row])
        c.append(matrix[row][length-row-1])

    if [players[1]]*length in (o, c):
        return 1
    elif [players[0]]*length in (o, c):
        return -1

    return stat


def get_depth(matrix: list) -> int:
    x = 0
    for row in matrix:
        x += row.count(players[2])

    return x


def minimax(matrix: list, depth: int, player: int) -> int:
    value = evaluation(matrix)
    if not depth or value != 2:
        return value

    result = -math.inf if player else math.inf
    for row in range(length):
        for col in range(length):
            if matrix[row][col] == players[2]:
                matrix[row][col] = players[player]
                result = func[player](result, minimax(matrix, depth-1, player^1))
                matrix[row][col] = players[2]

    return result


def computer_choice(matrix: list, easy_mode: int) -> tuple:
    position = 0, 0
    if easy_mode or first:
        position = secrets.randbelow(length), secrets.randbelow(length)
        while matrix[position[0]][position[1]] != players[2]:
            position = secrets.randbelow(length), secrets.randbelow(length)

    else:
        result = -math.inf
        for row in range(length):
            for col in range(length):
                if matrix[row][col] == players[2]:
                    matrix[row][col] = players[1]
                    c = minimax(matrix, get_depth(matrix), 0)
                    matrix[row][col] = players[2]
                    if c > result:
                        position, result = (row, col), c

    return position


length = int(input('n: '))
if length < 3 or not length&1:
    print(f'{length}x{length} is not a valid board')
    sys.exit(0)

matrix = []
for _ in range(length):
    matrix.append([players[2]]*length)

first = True
player = secrets.randbelow(2)
while True:
    print_matrix(matrix)
    if player:
        if length > 3:
            position = computer_choice(matrix, True)
        else:
            position = computer_choice(matrix, False)
    else:
        position = tuple(map(int, input('X,Y: ').split(',')))
        if not (0 <= position[0] < length and 0 <= position[1] < length):
            print(f'position X({position[0]}),Y({position[1]}) is invalid!')
            time.sleep(1)
            continue
        elif matrix[position[0]][position[1]] != players[2]:
            print(f'you are not allowed to select position X({position[0]}),Y({position[1]})')
            time.sleep(1)
            continue

    matrix[position[0]][position[1]] = players[player]
    c = evaluation(matrix)
    if c != 2:
        print_matrix(matrix)
        if c == 0:
            print('Draw!')
        elif c == 1:
            print('I won!')
        else:
            print('You won!')

        break

    player ^= 1
    first = False
