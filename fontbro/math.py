import math


def get_euclidean_distance(a, b):
    # https://en.wikipedia.org/wiki/Euclidean_distance#Higher_dimensions
    keys = set(list(a.keys()) + list(b.keys()))
    return math.sqrt(sum([math.pow(a.get(key, 0) - b.get(key, 0), 2) for key in keys]))
