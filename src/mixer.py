import sndobj
import time
from sensor import *
#import pressuresensor
#import lightsensor
#import flexSensor

#floating point frequencies?

#fsensor = flexSensor() #appropriate sensitivity values need to be placed in sensors.
#psensor = pressuresensor()
#lsensor = lightsensor()
tab = sndobj.HarmTable()
osc1 = sndobj.Oscili(tab, 1, 5000)
osc2 = sndobj.Oscili(tab, 1, 5000)
mod = sndobj.Oscili(tab, 1000, 200)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
delay = sndobj.DelayLine(1, osc2)
mixer = sndobj.Mixer()


mod.SetFreq(5)
osc1.SetFreq(440, mod)
osc2.SetFreq(800, mod)
mixer.AddObj(osc1)
mixer.AddObj(osc2)
mixer.AddObj(delay)
out.SetOutput(1, mixer)
knob = sensor(0, 'knob')
knob.setTolerance(5)

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
    value = knob.getValue() / 2
    #mod.SetFreq(value)
    mod.SetAmp(value)
    print(value)
    time.sleep(0.1)
thread.ProcOff()
