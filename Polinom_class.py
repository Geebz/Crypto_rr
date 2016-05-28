class Polinom(int):
    generator = 0b10001000000001011
    power = 16

    def __xor__(self, other):
        return Polinom(super(Polinom, self).__xor__(other))

    def __and__(self, other):
        return Polinom(super(Polinom,self).__and__(other))

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
        pol = self
        while deg >= self.power:
            pol = pol ^ (other << (deg - self.power))
            deg = pol.degree
        return Polinom(pol)

    def __pow__(self, power):
        b=Polinom(1)
        c = self
        m = reversed(Polinom(power).make_file())
        for bit in m:
            if int(bit):
                b = (b*c) % self.generator
            c = (c*c) % self.generator
        return Polinom(b)