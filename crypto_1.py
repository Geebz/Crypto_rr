from Polinom_class import Polinom
from feature import Profiler

with Profiler() as p:
    a = [Polinom(i) ** 16 for i in range(2 ** 16)]
    print a