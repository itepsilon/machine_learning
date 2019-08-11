from functools import reduce
from prettytable import PrettyTable
train_set = [(1, 1.8), (2, 2.4), (3.3, 2.3), (4.3, 3.8), (5.3, 5.3),
             (1.4, 1.5), (2.5, 2.2), (2.8, 3.8), (4.1, 4.0), (5.1, 5.4)]
validation_set = [(1.5,	1.7), (2.9,	2.7), (3.7,	2.5), (4.7,	2.8), (5.1,	5.5)]
test = [1.4, 2.5, 3.6, 4.5, 5.4]


def slope1(data):
    """ slope b = (NΣXY - (ΣX)(ΣY)) / (NΣX2 - (ΣX)2)
    >>> data = [(60, 3.1), (61, 3.6), (62, 3.8), (63, 4), (65, 4.1)]
    >>> slope(data)
    0.18783783783783292
    """
    n = len(data)
    xy = reduce(lambda a, b: a + b, [d[0] * d[1] for d in data])
    x = reduce(lambda a, b: a + b, [d[0] for d in data])
    y = reduce(lambda a, b: a + b, [d[1] for d in data])
    x2 = reduce(lambda a, b: a + b, [d[0]**2 for d in data])
    return (n * xy - x * y) / (n * x2 - x**2)


def intercept1(data, s):
    """ intercept a = (ΣY - b(ΣX)) / N
    >>> data = [(60, 3.1), (61, 3.6), (62, 3.8), (63, 4), (65, 4.1)]
    >>> s = slope(data)
    >>> intercept(data, s)
    -7.963513513513208
    """
    n = len(data)
    x = reduce(lambda a, b: a + b, [d[0] for d in data])
    y = reduce(lambda a, b: a + b, [d[1] for d in data])
    return (y - s * x) / n


def linear(a, b, x):
    ''' y = a + bx
    '''
    return a + b * x


def slope2(data):
    """ slope b = (NΣPY - (ΣP)(ΣY)) / (NΣP2 - (ΣP)2)
    >>> data = [(60, 3.1), (61, 3.6), (62, 3.8), (63, 4), (65, 4.1)]
    """
    n = len(data)
    xxy = reduce(lambda a, b: a + b, [d[0] * d[0] * d[1] for d in data])
    y = reduce(lambda a, b: a + b, [d[1] for d in data])
    xxxx = reduce(lambda a, b: a + b, [d[0]**4 for d in data])
    xx = reduce(lambda a, b: a + b, [d[0]**2 for d in data])
    return (n * xxy - xx * y) / (n * xxxx - xx**2)


def intercept2(data, b):
    """ intercept a = (ΣY - b(ΣP)) / N
    >>> data = [(60, 3.1), (61, 3.6), (62, 3.8), (63, 4), (65, 4.1)]
    """
    n = len(data)
    y = reduce(lambda a, b: a + b, [d[1] for d in data])
    xx = reduce(lambda a, b: a + b, [d[0]**2 for d in data])
    return (y - b * xx) / n


def non_linear(a, b, x):
    """ y = a + bx2
    """
    return a + b * x * x


def mse(y1, y2):
    result = 0
    for i in range(len(y1)):
        result += (y1[i] - y2[i])**2
    return result / len(y1)


b1 = slope1(train_set)
a1 = intercept1(train_set, b1)

b2 = slope2(train_set)
a2 = intercept2(train_set, b2)

t1 = PrettyTable()
t1.field_names = ["x", "y", "ŷ = a1 + b1 * x", "ŷ = a2 + b2 * x**2"]

for t in train_set:
    t1.add_row([t[0], t[1], linear(a1, b1, t[0]), non_linear(a2, b2, t[0])])

ty = [t[1] for t in train_set]
ty1 = [linear(a1, b1, t[0]) for t in train_set]
ty2 = [non_linear(a2, b2, t[0]) for t in train_set]

print("Training Set:")
print(t1)
print("MSE linear:", mse(ty1, ty))
print("MSE non linear:", mse(ty2, ty))
print()

t2 = PrettyTable()
t2.field_names = ["x", "y", "ŷ = a1 + b1 * x", "ŷ = a2 + b2 * x**2"]

for t in validation_set:
    t2.add_row([t[0], t[1], linear(a1, b1, t[0]), non_linear(a2, b2, t[0])])

vy = [v[1] for v in validation_set]
vy1 = [linear(a1, b1, v[0]) for v in validation_set]
vy2 = [non_linear(a2, b2, v[0]) for v in validation_set]

print("Validation Set:")
print(t2)
print("MSE linear:", mse(vy1, vy))
print("MSE non linear:", mse(vy2, vy))
print()
model = "ŷ = a1 + b1 * x"
better = linear
a = a1
b = b1
if mse(vy1, vy) / mse(ty1, ty) > mse(vy2, vy) / mse(ty2, ty):
    model = "ŷ = a2 + b2 * x**2"
    better = non_linear
    a = a2
    b = b2

# print(mse(vy1, vy) / mse(ty1, ty))
# print(mse(vy2, vy) / mse(ty2, ty))
print("Model " + model + " is better")

t3 = PrettyTable()
t3.field_names = ["x", model]

for t in test:
    t3.add_row([t, better(a, b, t)])
print(t3)
print()
