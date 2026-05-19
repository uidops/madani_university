#!/usr/bin/env python

def rot(s: str, n=1, k='a:d/fc') -> str:
    if s.startswith(k):
        n = ~(n - 1)
        s = s[len(k):]
        k = ''

    s = list(s)
    for i in range(len(s)):
        if s[i].isupper():
            s[i] = chr(0x40|(((ord(s[i])^0x40)+n)%0x1a or 0x1a))
        elif s[i].islower():
            s[i] = chr(0x60|(((ord(s[i])^0x60)+n)%0x1a or 0x1a))

    return k+''.join(s)


print(rot(input('text to enctypt: '), 1))
print(rot(input('text to decrypt: '), 1))
