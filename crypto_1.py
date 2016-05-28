# -*- coding: utf-8 -*-

from Polinom_class import Polinom
from feature import Profiler


def kord_func(array):
    return zip(*array)

def scalar_mul(a,b):
    return sum(int(bit) for bit in bin(a & b)[2:])

def uolsh_adamar(array):
    walsh_ranges = []
    for func in array:
        init = [(-1)**int(i, 2) for i in func]
        for i in range(Polinom.power):
            used = set()
            for num in range(2 ** Polinom.power):
                if num in used:
                    continue
                num_inv = num ^ (1 << (Polinom.power - 1 - i))
                used.add(num_inv)
                init[num], init[num_inv] = init[num] + init[num_inv], init[num] - init[num_inv]
        walsh_ranges.append(init)
        assert sum([i**2 for i in init])==2**(2*Polinom.power)
    return walsh_ranges

def disbalance(array):
    return [abs(i[0]) for i in array]

def k_balance(uolsh_array):
    array = []
    k=16
    for fx in range(Polinom.power):
        for elem in range(2**Polinom.power):
            wt = bin(elem).count('1')
            if wt<k and uolsh_array[fx][elem]!=0:
                k = wt
        array.append(k)
    return array

def nonlinearity(uolsh_array):
    array = []
    for func in range(Polinom.power):
        array.append(int(2**(Polinom.power-1) - 0.5*max(uolsh_array[func])))
    return array

def error_propagation(array):
    error_array = []
    for func in range(Polinom.power):
        func_arr = []
        for i in range(Polinom.power):
            i_arr = []
            for elem in range(2**Polinom.power):
                a = int(array[func][elem],2)
                xe = elem ^ (1 << Polinom.power-1-i)
                b = int(array[func][xe], 2)
                value = a ^ b
                i_arr.append(value)
            sum_i_arr = sum(i_arr)
            func_arr.append(sum_i_arr)
        error_array.append(func_arr)
    return error_array

def koef_error_propagation(array):
    func_array = []
    for func in range(Polinom.power):
        vec_i_array = []
        for vec_i in range(Polinom.power):
            value = abs(array[func][vec_i]-2**(Polinom.power-1))/float(2**(Polinom.power-1))
            vec_i_array.append(value)
        func_array.append(vec_i_array)
    return func_array

def koef_Zhegalkin(truth_table):
    koef_zheg = []
    for num, func in enumerate(truth_table):
        array = []
        for i in range(Polinom.power):
            used = set()
            for num in range(2 ** Polinom.power):
                if num in used:
                    continue
                num_inv = num ^ (1 << (Polinom.power - 1 - i))
                used.add(num_inv)
                array[num_inv] = array[num]^array[num_inv]
        koef_zheg.append(array)
        return koef_zheg


def calc_max_alg_degree(truth_table):
    F_degree = 0
    result = ''
    for num, func in enumerate(zip(*truth_table)):
        A = list(func[:])
        for i in range(Polinom.power):
            used = set()
            for elem in range(2 ** Polinom.power):
                if elem in used:
                    continue
                elem_inv = elem ^ (1 << (Polinom.power - 1 - i))
                used.add(elem_inv)
                A[elem_inv] = A[elem] ^ A[elem_inv]

        max_wt = 0
        for number, elem in enumerate(A):
            if elem:
                max_wt = max(max_wt, bin(number)[2:].count('1'))
        result += 'f{} = {} \n'.format(num, max_wt)
        F_degree = max(F_degree, max_wt)
    result += 'F = {}'.format(F_degree)
    return result



with Profiler() as p:
    # f = open('results.txt','r+')

    truth_table = [Polinom(i) ** 65534 for i in range(2 ** Polinom.power)]
    #
    b = ["{0:016b}".format(i) for i in truth_table]
    # #
    c = kord_func(b)
    # uolsh = uolsh_adamar(c)
    # disb = disbalance(uolsh)
    # kor_imun = k_balance(uolsh)
    # non = nonlinearity(uolsh)
