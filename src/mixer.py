import sndobj
import time
from sensor import *
from pressureSensor import *
from lightSensor import *
#import flexSensor

#fsensor = flexSensor() #appropriate sensitivity values need to be placed in sensors.
psensor = pressureSensor(2, 1)
lsensor = lightSensor(1, 10)
knob = sensor(0, 'knob')
knob.setTolerance(2)

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

freqStep = 10
ampStep = 200
lightAdjust = 15
pressureAdjust = 2
knobAdjust = 0.1

while True:
    light = lsensor.getLightValue()
    print("Light: " + str(light))
    if (osc1amp < light * lightAdjust):
        if (osc1amp + ampStep < light * lightAdjust): osc1amp += ampStep
        else: osc1amp = light * lightAdjust
    elif (osc1amp > light * lightAdjust):
        if (osc1amp - ampStep > light * lightAdjust): osc1amp -= ampStep
        else: osc1amp = light * lightAdjust
    
    pressure = psensor.getPressureValue()
    print("Pressure: " + str(pressure))
    if (osc1freq < pressure * pressureAdjust):
        if (osc1freq + freqStep < pressure * pressureAdjust): osc1freq += freqStep
        else: osc1freq = pressure * pressureAdjust
    elif (osc1freq > pressure * pressureAdjust):
        if (osc1freq - freqStep < pressure * pressureAdjust): osc1freq -= freqStep
        else: osc1freq = pressure * pressureAdjust
    
    knob.update()
    value = knob.getValue()
    mod.SetFreq(value * knobAdjust)
    print("Knob: " + str(value))
    
    osc1.SetFreq(osc1freq, mod)
    osc1.SetAmp(osc1amp)
    
    time.sleep(0.05)
thread.ProcOff()
