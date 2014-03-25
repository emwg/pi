import sndobj
import time
import psutil
from lightSensor import *

lsensor = lightSensor(1, 0, 10)

sine = sndobj.HarmTable(1000, 20, sndobj.SINE)
saw = sndobj.HarmTable(1000, 20, sndobj.SAW)
square = sndobj.HarmTable(1000, 20, sndobj.SQUARE)
buzz = sndobj.HarmTable(1000, 20, sndobj.BUZZ)
osc1 = sndobj.Oscili(sine, 0, 0)
osc2 = sndobj.Oscili(saw, 0, 0)
osc3 = sndobj.Oscili(square, 0, 0)
osc4 = sndobj.Oscili(buzz, 0, 0)
#buzz = sndobj.Buzz(0, 0, 0)
#pluck1 = sndobj.Pluck(400, 0)
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
mod = sndobj.Oscili(sine, 0, 100)
out = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
mixer = sndobj.Mixer()
mixer.AddObj(osc1)
mixer.AddObj(osc2)
mixer.AddObj(osc3)
mixer.AddObj(osc4)
#mixer.AddObj(pluck1)
#mixer.AddObj(buzz)

pan = sndobj.Pan(0, mixer)

thread = sndobj.SndThread()
out.SetOutput(1, pan.left)
out.SetOutput(2, pan.right)

thread.AddObj(mod)
thread.AddObj(osc1)
thread.AddObj(osc2)
thread.AddObj(osc3)
thread.AddObj(osc4)
#thread.AddObj(pluck1)
#thread.AddObj(buzz)
thread.AddObj(mixer)
thread.AddObj(pan)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()

#amounts the frequency and amplitude of the oscillators will change by during each loop iteration
freqStep = 10
lightStep = 40

#values with which to multiply the raw sensor values
lightAdjust = 1
flexAdjust = 1
knobAdjust = 0.1

dimCutoff = 200
minCutoff = 500
majCutoff = 700

pluckWait = 0.25
pluckTime = 0

lightValue = 0
rhythmCount = 0
subtractMult = 5000
osc1subtract = 1
osc2subtract = osc1subtract * subtractMult
osc3subtract = osc2subtract * subtractMult
osc4subtract = osc3subtract * subtractMult

avgSamples = 20
samples = 0
ramSum = 0
cpuSum = 0
avgRam = 0
avgCpu = 0

while True:
    
    #print system info
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=0)
    
    if (samples < avgSamples):
        ramSum += ram
        cpuSum += cpu
        samples += 1
    else:
        avgRam = (ramSum / avgSamples)
        avgCpu = (cpuSum / avgSamples)
        samples = 0
        ramSum = 0
        cpuSum = 0
    
    print("RAM usage: " + str(avgRam) + "%")
    print("CPU usage: " + str(avgCpu) + "%")
    
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
    
    #set chord type
    if (lightValue < dimCutoff):
        chord = "dim"
    elif(lightValue < minCutoff):
        chord = "min"
    elif(lightValue < majCutoff):
        chord = "maj"
    else: #(lightValue < augCutoff):
        chord = "aug"
        
        
    #print("osc1amp: " + str(osc4amp))    
    #set amplitudes
    osc1.SetAmp(osc1amp)
    osc2.SetAmp(osc2amp)
    osc3.SetAmp(osc3amp)
    osc4.SetAmp(osc4amp)

    if(lightValue != 0):
        amp = lightValue * 10
    else:
        amp = 4
    #print(amp)
    osc1.SetAmp(amp)
    osc2.SetAmp(amp)
    osc3.SetAmp(amp)
    osc4.SetAmp(amp)
    #buzz.SetAmp(amp)
    
    pluckWait = 500.0 / amp
    print(str(pluckWait))
    
    #if ((time.time() - pluckTime) > pluckWait):
        #pluck1.SetAmp(amp)
        #pluckTime = time.time()
    
    # root
    osc1freq = amp / 4
    # fifth
    osc2freq = osc1freq * (3/2)
    # third
    osc3freq = osc1freq * (osc1freq * 5) / (osc2freq * 4)
    # constant pitch
    osc4freq = 900
    pluck1freq = 700 #this does nothing
    
    #buzz.SetFreq(amp / 2)
    #buzz.SetHarm(amp / 20)
    
    #set frequencies
    osc1.SetFreq(osc1freq, mod)
    osc2.SetFreq(osc2freq, mod)
    osc3.SetFreq(osc3freq, mod)
    osc4.SetFreq(osc4freq, mod)
    
    #panning
    pan.SetPan((lightValue / 512.0) - 1)
    
    print("")

    #wait before doing another iteration
    time.sleep(0.05)
thread.ProcOff()
