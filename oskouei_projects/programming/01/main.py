#!/usr/bin/python

import sys
from random import choice

print('-------------------exercises1--------------------')

# 'J'
for _ in range(6):
    print('*', end='')
print()

for _ in range(4):
    print('  *')

for _ in range(2):
    print('* *')

print('\n-------------------exercises2--------------------')

inch = float(input('Give me the length in inch: '))
cm = inch * 2.54
print(f'{inch} inch = {cm} cm')

print('\n-------------------exercises3--------------------')

things = ['sang', 'kaghaz', 'gheychi']
user_thing = input(f'Choice one between {things}: ')
if user_thing in things:
    random_thing = choice(things)
    print(f'Your choice: {user_thing} | Computer\'s choice: {random_thing}')

    if user_thing == things[0] and random_thing == things[1]:
        print('Computer won!')
    elif user_thing == things[1] and random_thing == things[2]:
        print('Computer won!')
    elif user_thing == things[2] and random_thing == things[0]:
        print('Computer won!')
    elif user_thing == random_thing:
        print('Draw!')
    else:
        print('You won!')

else:
    print('Wrong choice!')

# Another solution:
#
# user_thing = things.index(user_thing)
# random_thing = random.randint(0, len(things)-1)
# solution = (user_thing + 1)
# solution = 0 if solution == 3 else solution
# 
# if solution == random_thing:
#     print('Computer Won!')
# elif user_thing == random_thing:
#     print('Draw!')
# else:
#     print('You won!')
#

print('\n-------------------exercises4--------------------')

x = int(input('x: '))
y = int(input('y: '))

if x == 0 or y == 0:
    print('Can you divide a number by zero?')
    sys.exit(1)

if x%y == 0 or y%x == 0:
    print('multiple')
else:
    print('not')

# Another solution:
#
# if math.gcd(x, y) == min(x, y)
#     print('multiple')
# else:
#     print('not')
#
