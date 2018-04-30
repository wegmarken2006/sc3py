from ugens import *
from sc3_1 import sc_start, sc_stop, sc_play


sc_start()
"""
freq = 440
ug = add(sin_osc(3*freq), sin_osc(6))
ug = sin_osc(3*freq)
sc_play(sin_osc(440, 0, mult=0.1))
sc_play(sin_osc2(440, 0))
sc_play(mul(sin_osc2(440, 0), Constant(0.1)))

x = 1000
ug2 = add(sin_osc(300 * x + 800, 0), pink_noise(0.1 * x + 0.1))
sc_play(ug2)
"""

sc_play(sin_osc2(440, 0))
sc_stop()

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
