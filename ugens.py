from sc3_1 import mk_oscillator, mk_filter, mk_unary_operator, mk_binary_operator
from sc3_1 import mk_osc_id, mk_filter_mce
from sc3_1 import mk_osc_mce
from sc3_1 import Constant, Ugen, Rate
from typing import List

uid = 0

def next_uid():
    global uid
    uid = uid + 1
    return uid

# unary
def u_abs(ugen: Ugen):
    return mk_unary_operator(5, abs, ugen)

# binary
def add(ugen1: Ugen, ugen2: Ugen) -> Ugen:
    return mk_binary_operator(0, lambda x, y: x+y, ugen1, ugen2)
def sub(ugen1: Ugen, ugen2: Ugen) -> Ugen:
    return mk_binary_operator(1, lambda x, y: x-y, ugen1, ugen2)
def mul(ugen1: Ugen, ugen2: Ugen) -> Ugen:
    return mk_binary_operator(2, lambda x, y: x*y, ugen1, ugen2)


def const_list(*args) -> List[Constant]:
    out: List[Constant] = []
    for elem in args:
        out.append(Constant(value=elem))
    return out

# oscillators
def sin_osc(freq, phase=0, rate: Rate=Rate.RateAr) -> Ugen:
    uf = Constant(freq)
    uph = Constant(phase)
    return mk_oscillator(rate, "SinOsc", inputs=[uf, uph], ou=1)
    #return mk_oscillator(rate, "SinOsc", inputs=const_list(freq, phase), ou=1)

def line(a, b, c, d, rate: Rate=Rate.RateAr) -> Ugen:
    return mk_oscillator(rate, "Line", inputs=const_list(a, b, c, d), ou=1)

def lf_noise2 (a, rate: Rate=Rate.RateAr):
    return mk_osc_id(rate=rate, name="LFNoise2", inputs=const_list(a),  ou=1, uid=next_uid())

def env_gen(a, b, c, d, e, ugen, rate: Rate=Rate.RateAr):
    return mk_osc_mce(rate=rate, name="EnvGen", inputs=const_list(a, b, c, d, e), ugen=ugen, ou=1)

# filters
def out(a, b):
    return mk_filter_mce(name="Out", inputs=const_list(a), ugen=b, ou=0)

def decay2(a, b, c):
    return mk_filter(name="Decay2", inputs=const_list(a, b, c), ou=1)

def clip(a, b, c):
    return mk_filter(name="Clip", inputs=const_list(a, b, c), ou=1)


