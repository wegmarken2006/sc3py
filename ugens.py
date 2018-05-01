from sc3_1 import mk_oscillator, mk_filter, mk_unary_operator, mk_binary_operator, Constant
from sc3_1 import mk_osc_id, mk_filter_mce
from sc3_1 import mk_osc_mce
from sc3_1 import Constant, Ugen, Rate, Control
from sc3_1 import sc_play
from typing import List


def f1(*args):
    print(*args)

class UgensRate:
    def __init__(self, func, *args) -> None:
        self.args = args
        self.func = func
    def ar(self):
        return UgensPlay(self.func, *self.args, rate=Rate.RateAr)

class UgensPlay(UgensRate):
    def __init__(self, func, *args, rate: Rate) -> None:
        self.args = args
        self.func = func
        self.rate = rate
    def play(self):
        sc_play(self.func(*self.args, rate=self.rate))


# unary
def u_abs(ugen: Ugen):
    return mk_unary_operator(5, abs, ugen)

# binary
def add(op1, op2) -> Ugen:
    return mk_binary_operator(0, lambda x, y: x+y, op1, op2)
def sub(op1, op2) -> Ugen:
    return mk_binary_operator(1, lambda x, y: x-y, op1, op2)
def mul(op1, op2) -> Ugen:
    return mk_binary_operator(2, lambda x, y: x*y, op1, op2)


def const_list(*args) -> List[Ugen]:
    out: List[Ugen] = []
    for elem in args:
        if type(elem) == int or type(elem) == float:
            out.append(Constant(value=elem))
        else:
            out.append(elem)
    return out


# oscillators
def sin_osc(freq, phase=0, mult=1, rate: Rate=Rate.RateAr) -> Ugen:
    return mul(mk_oscillator(rate, "SinOsc", inputs=const_list(freq, phase), ou=1), Constant(mult))

def sin_osc2(freq, phase=0, rate: Rate=Rate.RateAr) -> Ugen:
    return mk_oscillator(rate, "SinOsc", inputs=const_list(freq, phase), ou=1)

class SinOsc2(UgensRate):
    def __init__(self, freq=440, phase=0):
        super().__init__(sin_osc2, freq, phase)

def brown_noise (rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="BrownNoise", inputs=[], ou=1)

def line(a, b, c, d, rate: Rate=Rate.RateAr) -> Ugen:
    return mk_oscillator(rate, "Line", inputs=const_list(a, b, c, d), ou=1)

def lf_noise2(a, rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="LFNoise2", inputs=const_list(a),  ou=1)

def pink_noise(a, rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="PinkNoise", inputs=const_list(a),  ou=1)

def env_gen(a, b, c, d, e, ugen, rate: Rate=Rate.RateAr):
    return mk_osc_mce(rate=rate, name="EnvGen", inputs=const_list(a, b, c, d, e), ugen=ugen, ou=1)

# filters

def clip(a, b, c):
    return mk_filter(name="Clip", inputs=const_list(a, b, c), ou=1)

def decay2(a, b, c):
    return mk_filter(name="Decay2", inputs=const_list(a, b, c), ou=1)

def lpf(a, b):
    return mk_filter(name="LPF", inputs=const_list(a, b), ou=1)

def rhpf(a, b, c):
    return mk_filter(name="RHPF", inputs=const_list(a, b, c), ou=1)

def one_pole(a, b):
    return mk_filter(name="OnePole", inputs=const_list(a, b), ou=1)

def out(a, b):
    return mk_filter_mce(name="Out", inputs=const_list(a), ugen=b, ou=0)
