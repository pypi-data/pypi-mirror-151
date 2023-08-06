# -*- coding: utf-8 -*-
# hmath
# by caleb7023

def inf():
    return float("inf")


def complex_test(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        try:
            a = _x.imag
            if a == 0:
                return False
            else:
                return True
        except:
            return True
    else:
        _x = list(_x)
        return [complex_test(value1) for value1 in _x]


def primality_test(_n):
    if type(_n) == int:
        root_n = _n ** 0.5
        divisible = True
        for test in range(int(root_n) - 1):
            if  int(_n / (test + 2)) == _n / (test + 2):
                divisible = False
                break
        return divisible
    else:
        _n = list(_n)
        return [primality_test(value1) for value1 in _n]


def prime_factorization(_n):
    if type(_n) == int:
        if primality_test(_n):
            return _n
        decomposition_result = []
        prime_factorization2_ans_1 = _n
        prime_factorization2_ans_2 = 1
        while not(prime_factorization2_ans_1 == 1):
            prime_factorization2_ans_2 = prime_factorization2_ans_1
            for k in range(2 , int(prime_factorization2_ans_1 ** 0.5) + 1):
                if prime_factorization2_ans_1 / k == prime_factorization2_ans_1 // k / 1:
                    if primality_test(k):
                        prime_factorization2_ans_2 = k
                        break
            prime_factorization2_ans_1 = prime_factorization2_ans_1 / prime_factorization2_ans_2
            if not(prime_factorization2_ans_2 == 1):
                decomposition_result += [int(prime_factorization2_ans_2)]
        return decomposition_result
    else:
        _n = list(_n)
        return [prime_factorization(value1) for value1 in _n]


def rad(_n):
    if type(_n) == int:
        factorization = prime_factorization(_n)
        existing_value = []
        for k in factorization:
            if k not in existing_value:
                existing_value += [k]
        return existing_value
    else:
        _n = list(_n)
        return [rad(value1) for value1 in _n]


def division(_x , _y):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        if _y == 0:
            if   0 < _x:
                return  inf()
            elif _x < 0:
                return -inf()
            else:
                return  0
        elif _y == inf():
            return 0
        else:
            return _x / _y
    else:
        _x = list(_x)
        return [division(value1, _y) for value1 in _x]


def imag_part(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        try:
            return _x.imag
        except:
            return 0
    else:
        _x = list(_x)
        return [imag_part(value1) for value1 in _x]


def real_part(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        try:
            return _x.real
        except:
            return 0
    else:
        _x = list(_x)
        return [real_part(value1) for value1 in _x]


def pi():
    return 3.1415926535897932384626433832795


def e():
    return 2.7182818284590452353602874713527


def phi(): # φ
    return 1.6180339887498948482045868343656


def C(): #Euler's gamma
    return 0.5772156649015328606065120900824


def exp(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return e() ** _x
    else:
        _x = list(_x)
        return [exp(value1) for value1 in _x]


def ln(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        value_2 = 0
        for n in range(1 , 2000):
            value_3 = 2 ** (-n)
            value_2 += division(value_3 * (_x ** value_3), 1 + (_x ** value_3))
        return division(1 , division(_x , _x - 1) - value_2)
    else:
        _x = list(_x)
        return [ln(value1) for value1 in _x]


def log(_x , _y):
    if type(_y) == int or type(_y) == float or type(_y) == complex:
        return division(ln(_y) , ln(_x))
    else:
        _y = list(_y)
        return [log(_x, value1) for value1 in _y]


def square_root(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return _x ** 0.5
    else:
        _x = list(_x)
        return [square_root(value1) for value1 in _x]


def cube_root(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return _x ** 0.3333333333333333333333333333333333333333
    else:
        _x = list(_x)
        return [cube_root(value1) for value1 in _x]


def root_of(_x , _y):
    if type(_y) == int or type(_y) == float or type(_y) == complex:
        return _y ** (1 / _x)
    else:
        _y = list(_y)
        return [root_of(_x, value1) for value1 in _y]


def gamma(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        if not complex_test(_x):
            if _x < 0:
                value_1 = 1
                for n in range(1 , 100000):
                    value_1 *= division(((1 + (1 / n)) ** _x) , (1 + (_x / n)))
                return 1 / _x * value_1
        return 2.5066282746310002 * exp(-_x) * square_root(division(1, _x)) * (_x * square_root(division(1, 810 * (_x ** 6))  + _x * sinh(division(1, _x)))) ** _x
    else:
        _x = list(_x)
        return [gamma(value1) for value1 in _x]


def factorial(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        if not complex_test(_x):
            if _x % 1 == 0 and 0 < _x:
                ans = 1
                for process in range(1 , _x + 1):
                    ans = ans * process
                return ans
            if  _x < 0:
                return -factorial(-_x)
        return gamma(_x + 1)
    else:
        _x = list(_x)
        return [factorial(value1) for value1 in _x]


def sin(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return (exp(1j * _θ) - exp(-(1j * _θ))) / 2j
    else:
        _θ = list(_θ)
        return [sin(value1) for value1 in _θ]


def cos(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return (exp(1j * _θ) + exp(-(1j * _θ))) / 2
    else:
        _θ = list(_θ)
        return [cos(value1) for value1 in _θ]


def tan(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return division(sin(_θ) , cos(_θ))
    else:
        _θ = list(_θ)
        return [tan(value1) for value1 in _θ]


def csc(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return division(1 , sin(_θ))
    else:
        _θ = list(_θ)
        return [csc(value1) for value1 in _θ]


def sec(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return division(1 , cos(_θ))
    else:
        _θ = list(_θ)
        return [sec(value1) for value1 in _θ]


def cot(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return division(1 , tan(_θ))
    else:
        _θ = list(_θ)
        return [cot(value1) for value1 in _θ]


def asin(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return -1j * ln(1j * _x + square_root(1 - (_x ** 2)))
    else:
        _x = list(_x)
        return [asin(value1) for value1 in _x]


def acos(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return -1j * ln(_x - 1j * square_root(1 - (_x ** 2)))
    else:
        _x = list(_x)
        return [acos(value1) for value1 in _x]


def atan(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return 1j * (ln(1 - _x * 1j) - ln(1 + _x * 1j)) / 2
    else:
        _x = list(_x)
        return [atan(value1) for value1 in _x]


def acsc(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return asin(division(1 , _x))
    else:
        _x = list(_x)
        return [acsc(value1) for value1 in _x]


def asec(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return acos(division(1 , _x))
    else:
        _x = list(_x)
        return [asec(value1) for value1 in _x]


def acot(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return atan(division(1 , _x))
    else:
        _x = list(_x)
        return [acot(value1) for value1 in _x]


def sinh(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return (exp(_x) - exp(-_x)) / 2
    else:
        _x = list(_x)
        return [sinh(value1) for value1 in _x]


def cosh(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return (exp(_x) + exp(-_x)) / 2
    else:
        _x = list(_x)
        return [cosh(value1) for value1 in _x]


def tanh(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return sinh(_x) / cosh(_x)
    else:
        _x = list(_x)
        return [tanh(value1) for value1 in _x]


def csch(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return 1 / sinh(_x)
    else:
        _x = list(_x)
        return [csch(value1) for value1 in _x]


def sech(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return 1 / cosh(_x)
    else:
        _x = list(_x)
        return [sech(value1) for value1 in _x]


def coth(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return 1 / tanh(_x)
    else:
        _x = list(_x)
        return [coth(value1) for value1 in _x]


def asinh(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return ln(_x + square_root((_x ** 2) + 1))
    else:
        _x = list(_x)
        return [asinh(value1) for value1 in _x]


def acosh(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return ln(_x + square_root((_x + 1) * (_x - 1)))
    else:
        _x = list(_x)
        return [acosh(value1) for value1 in _x]


def atanh(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return ln((1 + _x) / (1 - _x)) / 2
    else:
        _x = list(_x)
        return [atanh(value1) for value1 in _x]


def acsch(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return asinh(1 / _x)
    else:
        _x = list(_x)
        return [acsch(value1) for value1 in _x]


def asech(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return acosh(1 / _x)
    else:
        _x = list(_x)
        return [asech(value1) for value1 in _x]


def acoth(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return atanh(1 / _x)
    else:
        _x = list(_x)
        return [acoth(value1) for value1 in _x]


def radian(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return _θ * 57.295779513082320876798154814105
    else:
        _x = list(_x)
        return [radian(value1) for value1 in _x]


def degrees(_θ):
    if type(_θ) == int or type(_θ) == float or type(_θ) == complex:
        return _θ / 57.295779513082320876798154814105
    else:
        _x = list(_x)
        return [degrees(value1) for value1 in _x]


def sinT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sin(ans + k) - sin(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sin(ans)
    return ans


def sinT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sin(ans + k) - sin(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sin(ans)
    return ans


def cosT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (cos(ans + k) - cos(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = cos(ans)
    return ans


def tanT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (tan(ans + k) - tan(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = tan(ans)
    return ans


def cscT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (csc(ans + k) - csc(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = csc(ans)
    return ans


def secT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sec(ans + k) - sec(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sec(ans)
    return ans


def cotT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (cot(ans + k) - cot(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = cot(ans)
    return ans


def asinT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asin(ans + k) - asin(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asin(ans)
    return ans


def acosT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acos(ans + k) - acos(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acos(ans)
    return ans


def atanT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (atan(ans + k) - atan(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = atan(ans)
    return ans


def acscT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acsc(ans + k) - acsc(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acsc(ans)
    return ans


def asecT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asec(ans + k) - asec(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asec(ans)
    return ans


def acotT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acot(ans + k) - acot(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acot(ans)
    return ans


def sinhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sinh(ans + k) - sinh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sinh(ans)
    return ans


def coshT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (cosh(ans + k) - cosh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = cosh(ans)
    return ans


def tanhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (tanh(ans + k) - tanh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = tanh(ans)
    return ans


def cschT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (csch(ans + k) - csch(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = csch(ans)
    return ans


def sechT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (sech(ans + k) - sech(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = sech(ans)
    return ans


def cothT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (coth(ans + k) - coth(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = coth(ans)
    return ans


def asinhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asinh(ans + k) - asinh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asinh(ans)
    return ans


def acoshT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acosh(ans + k) - acosh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acosh(ans)
    return ans


def atanhT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (atanh(ans + k) - atanh(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = atanh(ans)
    return ans


def acschT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acsch(ans + k) - acsch(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acsch(ans)
    return ans


def asechT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (asech(ans + k) - asech(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = asech(ans)
    return ans


def acothT(_n , _θ):
    if type(_n)==str:
        k = 0.01
        ans = _θ
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (acoth(ans + k) - acoth(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _θ
        for k in range(_n + 1):
            ans = acoth(ans)
    return ans


def gammaT(_n , _x):
    if type(_n)==str:
        k = 0.01
        ans = _x
        for h in range(len(_n)):
            if _n[h] == "d":
                ans = (gamma(ans + k) - gamma(ans)) / k
            else:
                raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
        return ans
    elif _n <= 0 or not _n % 1 == 0:
        raise Exception('The value of the argument must be a string that contains only "d" or a natural number.')
    else:
        ans = _x
        for k in range(_n + 1):
            ans = gamma(ans)
    return ans

def polygamma(_x):
    if type(_x) == int or type(_x) == float or type(_x) == complex:
        return gammaT("d", _x) / gamma(_x)
    else:
        _x = list(_x)
        return [polygamma(value1) for value1 in _x]