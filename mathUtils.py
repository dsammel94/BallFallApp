import math
def perpendicular(a):
    return [a[1], -1*a[0]]

def mag(a):
    return math.sqrt(sum(a[i]*a[i] for i in range(len(a))))

def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def scalar_mult(a, b):
    return [b*a for a in a]

def sub(a,b):
    return [a[i]-b[i] for i in range(len(a))]

def normalize(a):
    m = mag(a)
    return [a[i]/m for i in range(len(a))]
