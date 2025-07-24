import math

def divide(a, t):
    tmp1 = math.exp(a*t)
    tmp2 = tmp1 - 1 # equals 0 when a is very tiny.
    tmp3 = tmp2 / a
    return tmp3

def taylor_expansion(a, t, n=3):
    """
    (exp(a*t) - 1)/a = t + a/2!*pow(t, 2) + pow(a, 2)/3!*pow(t, 3) + ...

    Bigger n let ret closer to real value.
    """
    assert n>0 and isinstance(n, int)

    ret = t
    factor = 1
    for i in range(1, n):
        factor = factor * (a / (i+1))
        ret = ret + factor * pow(t, i+1)
    return ret


t = 5
for n in range(60):
    a = math.pow(2, n)
    print('\nn', n)
    print('2^n', a)
    print('a', 1/a)
    ret_taylor = taylor_expansion(1/a, t)
    try:
        ret_divide = divide(1/a, t)
    except:
        ret_divide = 'ERROR'
    print('Taylor expansion', ret_taylor)
    print('sample divide', ret_divide)