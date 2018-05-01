from ugens import *
from sc3_1 import sc_start, sc_stop, sc_play


sc_start()

"""
# stereo
s1 = mul(sin_osc2(440, 0), 0.1)
s2 = mul(sin_osc2(100, 0), 0.1)
sc_play([s1, s2])

"""
"""
# bubbles
ug20 = one_pole(brown_noise(), 0.99)
ug21 = lpf(brown_noise(), 14)
ug22 = add(mul(ug21, 400), 500)
ug100 = mul(rhpf(ug20, ug22, 0.03), 0.03)

sc_play([ug100, ug100])
"""


trig = impulse(freq=1000, phase=0)
ug1 = ringz(t2a(trig), 800, 0.01)

ug10 = ringz(dust(3), 2000, 2)

sc_play(ug1)
sc_stop()



"""
(defcgen kick-drum
  "basic synthesised kick drum"
  [bpm {:default 120 :doc "tempo of kick in beats per minute"}
   pattern {:default [1 0] :doc "sequence pattern of beats"}]
  (:ar
   (let [kickenv (decay (t2a (demand (impulse:kr (/ bpm 30)) 0 (dseq pattern INF))) 0.7)
         kick (* (* kickenv 7) (sin-osc (+ 40 (* kickenv kickenv kickenv 200))))]
     (clip2 kick 1))))
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
