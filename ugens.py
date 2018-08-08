from sc3_1 import mk_oscillator, mk_filter, mk_unary_operator, mk_binary_operator
from sc3_1 import mk_osc_id, mk_filter_mce, mk_filter_id
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
    def kr(self):
        return UgensPlay(self.func, *self.args, rate=Rate.RateKr)
    def ir(self):
        return UgensPlay(self.func, *self.args, rate=Rate.RateIr)
    def dr(self):
        return UgensPlay(self.func, *self.args, rate=Rate.RateDr)

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

def oscillator(name: str, inputs, rate, mulop, addop, ou=1):
    osc = mk_oscillator(rate=rate, name=name, inputs=inputs, ou=ou)
    if mulop is not 1:
        osc = mul(osc, mulop)
    if addop is not 0:
        osc = add(osc, addop)
    return osc

def oscillator_id(name: str, inputs, rate, mulop, addop, ou=1):
    osc = mk_osc_id(rate=rate, name=name, inputs=inputs, ou=ou)
    if mulop is not 1:
        osc = mul(osc, mulop)
    if addop is not 0:
        osc = add(osc, addop)
    return osc

# oscillators
def sin_osc(freq=440, phase=0, mulop=1, addop=0, rate=Rate.RateAr) -> Ugen:
    inputs = const_list(freq, phase)
    return oscillator("SinOsc", inputs, rate, mulop, addop)
    #return mk_oscillator(rate, "SinOsc", inputs=const_list(freq, phase), ou=1)

def sin_osc2(freq, phase=0, rate: Rate=Rate.RateAr) -> Ugen:
    return mk_oscillator(rate, "SinOsc", inputs=const_list(freq, phase), ou=1)

class SinOsc(UgensRate):
    def __init__(self, freq=440, phase=0, mulop=1, addop=0):
        super().__init__(sin_osc, freq, phase, mulop, addop)

def brown_noise (mulop=1, addop=0, rate: Rate=Rate.RateAr):
    inputs = []
    return oscillator_id("BrownNoise", inputs, rate, mulop, addop)
    #return mk_osc_id(rate=rate, name="BrownNoise", inputs=[], ou=1)

def dust(a, rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="Dust", inputs=const_list(a),  ou=1)

def impulse(freq=440, phase=0, rate: Rate=Rate.RateAr):
    return mk_oscillator(rate=rate, name="Impulse",  inputs=const_list(freq, phase), ou=1)

def line(a, b, c, d, rate: Rate=Rate.RateAr) -> Ugen:
    return mk_oscillator(rate, "Line", inputs=const_list(a, b, c, d), ou=1)

class Line(UgensRate):
    def __init__(self, a, b, c, d):
        super().__init__(line, a, b, c, d)

def lf_noise2(a, rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="LFNoise2", inputs=const_list(a),  ou=1)

def pink_noise(a, rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="PinkNoise", inputs=const_list(a),  ou=1)

def t2a(in1, offset=0):
    # return mk_filter(name="T2A", inputs=const_list(in1, offset), ou=1)
    return mk_oscillator(rate=Rate.RateAr, name="T2A", inputs=const_list(in1, offset), ou=1)


def env_gen(a, b, c, d, e, ugen, rate: Rate=Rate.RateAr):
    return mk_osc_mce(rate=rate, name="EnvGen", inputs=const_list(a, b, c, d, e), ugen=ugen, ou=1)

# filters

def clip(a, b, c):
    return mk_filter(name="Clip", inputs=const_list(a, b, c), ou=1)

def decay(in1, d_time):
    return mk_filter(name="Decay", inputs=const_list(in1, d_time), ou=1)

def decay2(a, b, c):
    return mk_filter(name="Decay2", inputs=const_list(a, b, c), ou=1)

#def demand(a, b, c):
#    return mk_filter(name="Demand", inputs=const_list(a, b, c), ou=1)

def lpf(a, b):
    return mk_filter(name="LPF", inputs=const_list(a, b), ou=1)

def rhpf(a, b, c):
    return mk_filter(name="RHPF", inputs=const_list(a, b, c), ou=1)

def ringz(a, b, c):
    return mk_filter(name="Ringz", inputs=const_list(a, b, c), ou=1)

def one_pole(a, b):
    return mk_filter(name="OnePole", inputs=const_list(a, b), ou=1)

def out(a, b):
    return mk_filter_mce(name="Out", inputs=const_list(a), ugen=b, ou=0)

