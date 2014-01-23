import sndobj
import time
from lightSensor import *

lsensor = lightSensor(0, 10)

tab = sndobj.HarmTable(1000, 50, 1)
osc1 = sndobj.Oscili(tab, 1, 0)
osc1amp = 0
#osc2 = sndobj.Oscili(tab, 1, 5000)
#osc3 = sndobj.Oscili(tab, 1, 5000)
#osc4 = sndobj.Oscili(tab, 1, 5000)
mod = sndobj.Oscili(tab, 1, 100)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
#delay = sndobj.DelayLine(1, osc2)
mixer = sndobj.Mixer()

mod.SetFreq(0)
osc1.SetFreq(0, mod)
osc1freq = 0
#osc2.SetFreq(400, mod)
#osc3.SetFreq(300, mod)
#osc4.SetFreq(500, mod)
mixer.AddObj(osc1)
#mixer.AddObj(osc2)
#mixer.AddObj(osc3)
#mixer.AddObj(osc4)

thread = sndobj.SndThread()
#mixer.AddObj(delay)
out.SetOutput(1, mixer)

thread.AddObj(mod)
thread.AddObj(osc1)
#thread.AddObj(osc2)
#thread.AddObj(osc3)
#thread.AddObj(osc4)
#thread.AddObj(delay)
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
    # Light sensor
    ###
    #get light sensor value
    light = lsensor.getLightValue()
    print("Light: " + str(light))
    #make amplitude slide smoothly to the new value
    if (osc1amp < light * lightAdjust):
        #slide up
        if (osc1amp + ampStep < light * lightAdjust): osc1amp += ampStep
        else: osc1amp = light * lightAdjust
    elif (osc1amp > light * lightAdjust):
        #slide down
        if (osc1amp - ampStep > light * lightAdjust): osc1amp -= ampStep
        else: osc1amp = light * lightAdjust
        
    #osc1.SetFreq(osc1freq, mod)
    osc1.SetAmp(osc1amp)
    
    #wait before doing another iteration
    time.sleep(0.05)
thread.ProcOff()
