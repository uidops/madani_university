#!/usr/bin/env python

def encrypt(data):
    data = data[:-1].lower().split(' ')

    for i, j in enumerate(data):
        if j[0] in ('a', 'e', 'i', 'o', 'u'):
            j = j[1:] + j[0] + 'v'
        elif len(j) > 2:
            j = j[2:] + j[:2]

        data[i] = j

    return ' '.join(data) + '.'

def decrypt(data):
    data = data[:-1].lower().split(' ')

    for i, j in enumerate(data):
        if j[-1] == 'v' and j[-2] in ('a', 'e', 'i', 'o' ,'u'):
            j = j[-2] + j[:-2]
        elif len(j) > 2:
            j = j[-2:] + j[:-2]

        data[i] = j

    return ' '.join(data) + '.'

the_input = input('give me the encrypted data to decrypt: ')

de = decrypt(the_input)
print('\ndecrypted data:', de)
print('encrypted data:', encrypt(de))

# INPUT : we lwaysav ytr to epke urov tada cretse.
# OUTPUT: we always try to keep our data secret.
