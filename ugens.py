from sc3_1 import mk_oscillator, mk_filter, mk_unary_operator, mk_binary_operator
from sc3_1 import Constant, Ugen, Rate

def sin_osc(a, b, rate: Rate=Rate.RateKr) -> Ugen:
    ua = Constant(value=a)
    ub = Constant(value=b)
    return mk_oscillator(rate, "SinOsc", inputs=[ua, ub], ou=1)


def u_abs(ugen: Ugen):
    return mk_unary_operator(5, abs, ugen)

