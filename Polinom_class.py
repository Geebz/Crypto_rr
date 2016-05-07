class Polinom(int):
    generator = 0b1000100000001010
    power=16

    def __xor__(self, other):
        return Polinom(super(Polinom, self).__xor__(other))

    def __add__(self, other):
        return Polinom(self^other)

    @property
    def degree(self):
        return len(bin(self)) - 3

    def make_file(self):
        return bin(self)[2:]

    def __mul__(self, other):
        bitsa = reversed("{0:b}".format(self))
        g = [(other<< i) * int(bit) for i, bit in enumerate(bitsa)]
        return Polinom(reduce(lambda x, y: x ^ y, g))

    def __mod__(self, other):
        deg = self.degree
        pol=self
        while deg>=self.power:
            pol = pol ^ (other << (deg - self.power))
            deg = pol.degree
        return Polinom(pol)

    def __pow__(self, power):
        b=Polinom(1)
        c = self
        m = reversed(Polinom(power).make_file())
        for bit in m:
            if bit:
                b = (b*c) % self.generator
            c = (c*c) % self.generator
        return Polinom(b)


var1=Polinom(2)
var2=Polinom(2)
print (var1**8).make_file()
# print (var1**15).make_file()
