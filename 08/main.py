#!/usr/bin/env python

def rot(s: str, n=1, k='a:d/fc') -> str:
    if s.startswith(k):
        n *= -1
        s = s[len(k):]
        k = ''

    s = list(s)
    for i in range(len(s)):
        if s[i].isupper():
            s[i] = chr(65+((ord(s[i])-65+n)%26))
        elif s[i].islower():
            s[i] = chr(97+((ord(s[i])-97+n)%26))

    return k+''.join(s)


print(rot(input('text to enctypt: ')))
print(rot(input('text to decrypt: ')))
