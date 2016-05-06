# power = 16
#
pol_gen ='1000100000001010'
pol_gen_int = int(pol_gen,2)

def initialization(power):
    for i in range(2**power):
        binnum = bin(i)[2:]
        nullnum = power - len(binnum)
        fullnum = nullnum*'0' + binnum
        print fullnum

# power = 65534
# bin_power = bin(power)[2:]
# print bin_power

def multiply(a,b):
    a = int(a,2)
    b = int(b,2)
    bitsa = reversed("{0:b}".format(a))
    g = [(b<<i)*int(bit) for i,bit in enumerate(bitsa)]
    return bin(reduce(lambda x,y: x^y,g))[2:]


def mod(polinom,power,pol_gen):
    deg = polinom[::-1].rfind('1')+1
    if deg>=power:
        k=deg
        pol = int(polinom,2)
        pol = pol^(pol_gen<<(k-power))
    return bin(pol)[2:], pol

print mod('10000010101011001',16, pol_gen_int)

print mod('1111',4,'1011')