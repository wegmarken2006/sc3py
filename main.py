from ugens import *
from osc_1 import  sc_start, sc_stop, osc_send
from sc3_1 import synthdef

sc_start()
freq = 440
ug = add(sin_osc(3*freq), sin_osc(6))
osc_send(synthdef("HH", ug))

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
