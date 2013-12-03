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
osc1 = sndobj.Oscili(tab, 1, 5000)
#osc2 = sndobj.Oscili(tab, 1, 5000)
#osc3 = sndobj.Oscili(tab, 1, 5000)
#osc4 = sndobj.Oscili(tab, 1, 5000)
mod = sndobj.Oscili(tab, 1000, 200)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
#delay = sndobj.DelayLine(1, osc2)
mixer = sndobj.Mixer()

mod.SetFreq(5)
osc1.SetFreq(440, mod)
osc1freq = 440
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
    light = lsensor.getLightValue()
    print("Light: " + str(light))
    freqStep = 15
    if (osc1freq < light * 2):
        osc1freq += freqStep
        osc1.SetFreq(osc1freq)
    elif (osc1freq > light * 2):
        osc1freq -= freqStep
        osc1.SetFreq(osc1freq)
    
    pressure = psensor.getPressureValue()
    print("Pressure: " + str(pressure))
    osc1.SetAmp(pressure * 15)
    
    knob.update()
    value = knob.getValue() / 10.0
    mod.SetFreq(value)
    print("Knob: " + str(value))
    
    time.sleep(0.05)
thread.ProcOff()
