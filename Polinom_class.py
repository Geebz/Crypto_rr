class Polinom():
    generator = int('1000100000001010',2)
    power=4
    pol_value = 0
    pol_int = 0

    def __init__(self,pol_value):
        self.pol_value = pol_value
        self.pol_int = int(pol_value,2)

    def getter(self):
        return self.pol_value

    def setter(self,value):
        self.pol_value = value

    def __mul__(self, other):
        bitsa = reversed("{0:b}".format(self.pol_int))
        g = [(other.pol_int << i) * int(bit) for i, bit in enumerate(bitsa)]
        return reduce(lambda x, y: x ^ y, g)

    def __mod__(self, other):
        deg = self.pol_value[::-1].rfind('1')+1
        if deg>=self.power:
            pol = self.pol_int
            pol = pol ^ (other << (deg - self.power))
        else:
            raise Exception
        return pol

    def __pow__(self, power):
        b=1
        c = self.pol_int
        m = bin(power)[2:][::-1]
        for i,n in enumerate(m):
            if m[i] == '1':
                b = (b*c) % self.generator
            c = (c*c) % self.generator
        return b


var1=Polinom('10')

print var1**7