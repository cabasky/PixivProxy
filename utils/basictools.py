import random


def randnum(len):
    ret = 0
    for i in range(len):
        ret *= 2
        ret += random.randint(0, 1)
    return ret


def randstr(len):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', len))
