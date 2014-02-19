import sndobj
import time
import psutil
from lightSensor import *

#stereo?

lsensor = lightSensor(0, 10)

tab = sndobj.HarmTable(1000, 50, 1)
osc1 = sndobj.Oscili(tab, 0, 0)
osc2 = sndobj.Oscili(tab, 0, 0)
osc3 = sndobj.Oscili(tab, 0, 0)
osc4 = sndobj.Oscili(tab, 0, 0)
buzz = sndobj.Buzz(0, 0, 0)
pluck1 = sndobj.Pluck(400, 0)
osc1amp = 0
osc2amp = 0
osc3amp = 0
osc4amp = 0
pluck1amp = 0
osc1freq = 100
osc2freq = 200
osc3freq = 300
osc4freq = 400
pluck1freq = 0
mod = sndobj.Oscili(tab, 0, 100)
out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
mixer = sndobj.Mixer()
mixer.AddObj(osc1)
mixer.AddObj(osc2)
mixer.AddObj(osc3)
mixer.AddObj(osc4)
mixer.AddObj(pluck1)
mixer.AddObj(buzz)

pan = sndobj.Pan(-1, mixer)

thread = sndobj.SndThread()
out.SetOutput(0, pan.left)
out.SetOutput(1, pan.right)

thread.AddObj(mod)
thread.AddObj(osc1)
thread.AddObj(osc2)
thread.AddObj(osc3)
thread.AddObj(osc4)
thread.AddObj(pluck1)
thread.AddObj(buzz)
thread.AddObj(mixer)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()

#amounts the frequency and amplitude of the oscillators will change by during each loop iteration
freqStep = 10
lightStep = 40

#values with which to multiply the raw sensor values
lightAdjust = 1
flexAdjust = 1
knobAdjust = 0.1

pluckWait = 0.25
pluckTime = 0

lightValue = 0
rhythmCount = 0
subtractMult = 5000
osc1subtract = 1
osc2subtract = osc1subtract * subtractMult
osc3subtract = osc2subtract * subtractMult
osc4subtract = osc3subtract * subtractMult

while True:
    
    #print system info
    print("RAM usage: " + str(psutil.virtual_memory().percent) + "%")
    print("CPU usage: " + str(psutil.cpu_percent(interval=0)) + "%")
    
    ###
    # Light sensor
    ###
    #get light sensor value
    light = lsensor.getLightValue() * lightAdjust
    print("Light: " + str(light))
    #interpolate lightValue
    if (lightValue < light):
        #slide up
        if (lightValue + lightStep < light): lightValue += lightStep
        else: lightValue = light
    elif (lightValue > light):
        #slide down
        if (lightValue - lightStep > light): lightValue -= lightStep
        else: lightValue = light
        
    #osc1amp = lightValue - osc1subtract
    #osc2amp = lightValue - osc2subtract
    #osc3amp = lightValue - osc3subtract
    #osc4amp = lightValue - osc4subtract
        
        
    #print("osc1amp: " + str(osc4amp))    
    #set amplitudes
    #osc1.SetAmp(osc1amp)
    #osc2.SetAmp(osc2amp)
    #osc3.SetAmp(osc3amp)
    #osc4.SetAmp(osc4amp)

    if(lightValue != 0):
        amp = lightValue * 10
    else:
        amp = 4
    #print(amp)
    osc1.SetAmp(amp)
    osc2.SetAmp(amp)
    osc3.SetAmp(amp)
    osc4.SetAmp(amp)
    buzz.SetAmp(amp)
    
    pluckWait = 500.0 / amp
    print(str(pluckWait))
    
    if ((time.time() - pluckTime) > pluckWait):
        pluck1.SetAmp(amp)
        pluckTime = time.time()
    
    # root
    osc1freq = amp / 4
    # fifth
    osc2freq = osc1freq * (osc1freq * 3) / (osc1freq * 2) 
    # third
    osc3freq = osc1freq * (osc1freq * 5) / (osc2freq * 4)
    # constant pitch
    osc4freq = 900
    pluck1freq = 700 #this does nothing
    
    buzz.SetFreq(amp / 2)
    buzz.SetHarm(amp / 20)
    
    #set frequencies
    osc1.SetFreq(osc1freq, mod)
    osc2.SetFreq(osc2freq, mod)
    osc3.SetFreq(osc3freq, mod)
    osc4.SetFreq(osc4freq, mod)
    
    #panning
    #pan.SetPan((lightValue / 512) - 1)
    
    print("")

    #wait before doing another iteration
    time.sleep(0.05)
thread.ProcOff()
