import sndobj
import time
from sensor import *
#import pressuresensor
#import lightsensor
#import flexSensor

#fsensor = flexSensor() #appropriate sensitivity values need to be placed in sensors.
#psensor = pressuresensor()
#lsensor = lightsensor()
tab = sndobj.HarmTable()
tab.SetHarm(50, 2)
tab.MakeTable()
osc1 = sndobj.Oscili(tab, 1, 5000)
osc2 = sndobj.Oscili(tab, 1, 5000)
osc3 = sndobj.Oscili(tab, 1, 5000)
osc4 = sndobj.Oscili(tab, 1, 5000)
mod = sndobj.Oscili(tab, 1000, 200)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
delay = sndobj.DelayLine(1, osc2)
mixer = sndobj.Mixer()


mod.SetFreq(5)
osc1.SetFreq(440)
osc2.SetFreq(400, mod)
osc3.SetFreq(300, mod)
osc4.SetFreq(500, mod)
mixer.AddObj(osc1)
#mixer.AddObj(osc2)
#mixer.AddObj(osc3)
#mixer.AddObj(osc4)

thread = sndobj.SndThread()
#mixer.AddObj(delay)
out.SetOutput(1, mixer)
knob = sensor(0, 'knob')
knob.setTolerance(2)

#thread.AddObj(mod)
thread.AddObj(osc1)
#thread.AddObj(osc2)
#thread.AddObj(osc3)
#thread.AddObj(osc4)
#thread.AddObj(delay)
thread.AddObj(mixer)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()
while True:
    knob.update()
    value = knob.getValue() / 10.0
    mod.SetFreq(value)
    print(value)
    time.sleep(0.1)
thread.ProcOff()
