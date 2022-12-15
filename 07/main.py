#!/usr/bin/env python

import math
import operator
import os
import secrets
import sys
import time


print('--------------------exercises1--------------------')

def minimum(words: list, length: int, n=0) -> int:
    if length < 0:
        return n

    return minimum(words, length-1, length if len(words[n]) >= len(words[length]) else n)


words = input('text: ').split()
small = None
if words != []:
   small = words[minimum(words, len(words)-1)]

print(f'the smallest word is "{small}"')


print('--------------------exercises2--------------------')

def is_interest_matrix(matrix: list) -> bool:
    return not (sum((*matrix[0][1:-1], *matrix[3][1:-1],
                    *map(operator.itemgetter(0), matrix),  *map(operator.itemgetter(3), matrix))) - \
                sum((matrix[i][i]+matrix[i][3-i] for i in range(4))))


matrix = []
for _ in range(4):
    matrix.append(list(map(float, input(f'row {_}: ').split())))

print(is_interest_matrix(matrix))


print('--------------------exercises3--------------------')

days_of_months = {'Farvardin': 31, 'Ordibehesht': 31, 'Khordaad': 31,
                  'Tir': 31, 'Mordad': 31, 'Shahrivar': 31,
                  'Mehr': 30, 'Ababn': 30, 'Azar': 30,
                  'Dey': 30, 'Bahman': 30, 'Esfand': 29}


def datebyday(day: int) -> tuple:
    day = day%sum(days_of_months.values())
    for month in days_of_months:
        if day <= days_of_months[month]:
            break

        day -= days_of_months[month]

    return month, day


day = int(input('day of year: '))
if day:
    print(datebyday(day))
else:
    print('zero?')


print('--------------------exercises4--------------------')

def facture(clients: list) -> list:
    factures = []
    for client in clients:
        used_water, client_type = client.values()
        if client_type.lower() == 'h':
            factures.append(used_water/100*500)
        elif client_type.lower() == 'i':
            n = (4E6, used_water-4E6) if used_water > 4E6 else (used_water, 0)
            factures.append((n[0]/1000*750) + (n[1]*(750.00025)))
        elif client_type.lower() == 'e':
            n = (2E6, used_water-2E6) if used_water > 2E6 else (used_water, 0)
            factures.append((n[0]/1500*600) + (n[1]*(600.00004)))
        else:
            factures.append(0)

    return factures


clients = []
n = int(input('number of clients: '))
for _ in range(n):
    raw = input(f'client-{_} used_water client_type: ').split()
    raw[0] = int(raw[0])
    clients.append(dict(zip(('used_water', 'client_type'), raw)))

print()
factures = facture(clients)
for i in range(len(factures)):
    print(f'{clients[i]} : {factures[i]}')


print('--------------------exercises5--------------------')

def is_armstrong(n: int) -> bool:
    if not n:
        return False

    x = n
    length = math.floor(math.log10(n)) + 1
    answer = 0
    while x != 0:
        answer += math.pow(x%10, length)
        x //= 10

    return n == answer


n = int(input('number: '))
print(is_armstrong(n))


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
if length < 3 and length&1:
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
