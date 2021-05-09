from math import log2
a=[255]

def value(b):
    out=0
    t=0
    for x in b:
        out += x*(256**t)
        t+=1
    return out

print(value(a))