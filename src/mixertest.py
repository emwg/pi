import sndobj
import time
from sensor import *

knob = sensor(0, 'knob')
knob.setTolerance(2)

tab = sndobj.HarmTable(1000, 50, 1)
osc1 = sndobj.Oscili(tab, 1, 0)
osc1amp = 0
mod = sndobj.Oscili(tab, 1, 100)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
mixer = sndobj.Mixer()

mod.SetFreq(0)
osc1.SetFreq(0, mod)
osc1freq = 0
mixer.AddObj(osc1)

thread = sndobj.SndThread()
out.SetOutput(1, mixer)

thread.AddObj(mod)
thread.AddObj(osc1)
thread.AddObj(mixer)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()

#amounts the frequency and amplitude of the oscillators will change by during each loop iteration
freqStep = 10
ampStep = 200

#values with which to multiply the raw sensor values
lightAdjust = 15
flexAdjust = 1
knobAdjust = 0.1

while True:
    
    ###
    # Knob
    ###
    #get knob value
    knob.update()
    value = knob.getValue()
    mod.SetFreq(value * knobAdjust)
    print("Knob: " + str(value))
    
    osc1.SetFreq(osc1freq, mod)
    osc1.SetAmp(osc1amp)
    
    #wait before doing another iteration
    time.sleep(0.05)
thread.ProcOff()
