from ugens import *
from sc3_1 import sc_start, sc_stop, sc_play, Mrg, Mce


sc_start()

s1 = mul(sin_osc2(440, 0), 0.1)
s2 = mul(sin_osc2(100, 0), 0.1)
sc_play([s1, s2])

"""
ug1 = mul(rhpf(one_pole(brown_noise(), 0.99), add(mul(lpf(brown_noise(), 14), 400), 500), 0.03), 0.003)
ug2 = mul(rhpf(one_pole(brown_noise(), 0.99), add(mul(lpf(brown_noise(), 20), 800), 1000), 0.03), 0.005)
ug3 = mul(add(ug1, ug2), 4)
ug10 = one_pole(brown_noise(), 0.99)
ug11 = mul(lpf(brown_noise(), 14), 400)
ug12 = rhpf(one_pole(brown_noise(), 0.99), add(mul(lpf(brown_noise(), 14), 400), 500), 0.03)
ug13 = mul(lpf(brown_noise(), 14), 100)

sc_play(ug13)
"""

sc_stop()

"""
{
({RHPF.ar(OnePole.ar(BrownNoise.ar, 0.99), LPF.ar(BrownNoise.ar, 14)
* 400 + 500, 0.03, 0.003)}!2)
+ ({RHPF.ar(OnePole.ar(BrownNoise.ar, 0.99), LPF.ar(BrownNoise.ar, 20)
* 800 + 1000, 0.03, 0.005)}!2)
* 4
}.play

"""

"""
(definst organ [freq 440 dur 1 land 0.9 volume 1.0]
  (-> (square freq)
      (+ (sin-osc (* 3 freq) (sin-osc 6)))
      (+ (sin-osc (* 1/2 freq) (sin-osc 3)))
      (* (env-gen (adsr 0.03 0.3 0.4) (line:kr 1 0 dur) :action FREE))
      (* (sin-osc (* freq 2)))
      (clip2 (line:kr 1 land 16))
      (* volume)))
      """
