import sndobj
import time
from sensor import *

#floating point frequencies?

tab = sndobj.HarmTable()
osc1 = sndobj.Oscili(tab, 1, 5000)
osc2 = sndobj.Oscili(tab, 1, 5000)
mod = sndobj.Oscili(tab, 1000, 200)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
delay = sndobj.DelayLine(1, osc2)
mixer = sndobj.Mixer()


mod.SetFreq(1)
osc1.SetFreq(440, mod)
osc2.SetFreq(800, mod)
mixer.AddObj(osc1)
mixer.AddObj(osc2)
mixer.AddObj(delay)
out.SetOutput(1, mixer)
knob = sensor(0, 'knob')

thread = sndobj.SndThread()
thread.AddObj(mod)
thread.AddObj(osc1)
thread.AddObj(osc2)
thread.AddObj(delay)
thread.AddObj(mixer)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()
while True:
    knob.update()
    mod.SetFreq(float(knob.getValue() / 50))
    print(knob.getValue() / 50.0)
    time.sleep(0.1)
thread.ProcOff()
