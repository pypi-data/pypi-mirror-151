import numpy as np

from typing import Any


# sin, cos, exp, log, tan = np.sin, np.cos, np.exp, np.log, np.tan


def sin(x, *args, **kwargs):
    '''
    forward alias to numpy.sin
    '''
    return np.sin(x, *args, **kwargs)


def cos(x, *args, **kwargs):
    '''
    forward alias to numpy.cos
    '''
    return np.cos(x, *args, **kwargs)


def exp(x, *args, **kwargs):
    '''
    forward alias to numpy.exp
    '''
    return np.exp(x, *args, **kwargs)


def log(x, *args, **kwargs):
    '''
    forward alias to numpy.log
    '''
    return np.log(x, *args, **kwargs)


def tan(x, *args, **kwargs):
    '''
    forward alias to numpy.tan
    '''
    return np.tan(x, *args, **kwargs)


def abspow(base: float | Any, power: float | int | Any = 2.0):
    if hasattr(base, 'abspow'): return base.abspow(power)
    if hasattr(power, 'rabspow'): return power.rabspow(base)
    if power < 1.0: raise AssertionError('power to small!')
    if power == 1.0: return abs(base)
    if power == 2.0: return abs(base)*base
    return abs(base)*(base**(power - 1.0))


def arctan2(x1: float | Any, x2: float | Any):
    if hasattr(x1, 'arctan2'): return x1.arctan2(x2)
    if hasattr(x2, 'rarctan2'): return x2.rarctan2(x1)
    return np.arctan2(x1, x2)


def relu(arg: float | Any):
    if hasattr(arg, 'relu'): return arg.relu()
    return maximum(0.0, arg)


def maximum(*others: float | Any):
    for other in others:
        if hasattr(other, 'maximum'): return other.maximum(*others)
        if hasattr(other, 'max'): return other.maximum(*others)
    return max(*others)


def minimum(*others: float | Any):
    for other in others:
        if hasattr(other, 'minimum'): return other.minimum(*others)
        if hasattr(other, 'min'): return other.minimum(*others)
    return min(*others)
