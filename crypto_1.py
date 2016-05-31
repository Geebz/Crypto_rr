# -*- coding: utf-8 -*-

from Polinom_class import Polinom
from feature import Profiler
from multiprocessing import Pool, cpu_count


def kord_func(array):
    A = []
    for func in zip(*array):
        new_array = []
        for k in func:
            new_array.append(int(k))
        A.append(new_array)
    return A

def uolsh_adamar(array):
    walsh_ranges = []
    for func in array:
        init = [(-1)**i for i in func]
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
                a = array[func][elem]
                xe = elem ^ (1 << Polinom.power-1-i)
                b = array[func][xe]
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

def error_propagation_bool(array):
    error_array = []
    for i in range(Polinom.power):
        i_arr = []
        for elem in range(2 ** Polinom.power):
            a = array[elem]
            xe = elem ^ (1 << Polinom.power - 1 - i)
            b = array[xe]
            value = a ^ b
            wt = bin(value)[2:].count('1')
            i_arr.append(wt)
        sum_i_arr = sum(i_arr)
        error_array.append(sum_i_arr)
    return error_array

def koef_error_bool(array):
    vec_i_array = []
    for vec_i in range(Polinom.power):
        value = abs(array[vec_i] - Polinom.power * (2 ** (Polinom.power - 1))) / \
                float(Polinom.power * (2 ** (Polinom.power - 1)))
        vec_i_array.append(value)
    return vec_i_array

def Alg_degree(truth_table):
    F_degree = 0
    result = ''
    for num, func in enumerate(truth_table):
        array = list(func[:])
        for i in range(Polinom.power):
            used = set()
            for elem in range(2 ** Polinom.power):
                if elem in used:
                    continue
                elem_inv = elem ^ (1 << (Polinom.power - 1 - i))
                used.add(elem_inv)
                array[elem_inv] = array[elem] ^ array[elem_inv]

        max_fd = 0
        for number, elem in enumerate(array):
            if elem:
                max_fd = max(max_fd, bin(number)[2:].count('1'))
        result += 'f{} = {} \n'.format(num, max_fd)
        F_degree = max(F_degree, max_fd)
    result += 'F = {}'.format(F_degree)
    return result

def avalanche_effect(array,bool_array):

    for num,func in enumerate(array):
        for elem in func:
            if elem != 2**(Polinom.power-1):
                print 'f {} avelanche effect False'.format(num)
                break

    for num,elem in enumerate(bool_array):
        if elem != Polinom.power * (2 ** Polinom.power):
            print 'F avg. avelanche effect False'


def get_mdp(a):
    b = [0] * (2 ** Polinom.power)
    for x in range(2 ** Polinom.power):
        b[truth_table[x] ^ truth_table[x ^ a]] += 1
    return max(b)

def mdp():
    cpu_size = cpu_count() - 1
    processes = Pool(cpu_size)
    gf = truth_table[1:]

    MDP = processes.map(get_mdp,gf)

    return '{}/2^{}'.format(max(MDP), Polinom.power)


with Profiler() as p:
    # f = open('results.txt','r+')

    truth_table = [Polinom(i) ** 65534 for i in range(2 ** Polinom.power)]
    #
    b = ["{0:016b}".format(i) for i in truth_table]
    # #
    c = kord_func(b)
    uolsh = uolsh_adamar(c)
    # disb = disbalance(uolsh)
    # kor_imun = k_balance(uolsh)
    # non = nonlinearity(uolsh)
    bi = error_propagation(c)
    # avalanche_effect(b)
    # print mdp()
    k = error_propagation_bool(truth_table)