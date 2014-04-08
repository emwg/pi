import sndobj
import time
import psutil
from pressureSensor import *

NUM_SENSORS = 4

CHORD_SENSOR = 0
AMP_SENSOR = 0
PAN_SENSOR = 0
COMB_SENSOR = 0
FIXME_SENSOR = 0

sensors = []

for x in range(NUM_SENSORS):
    sensors.append(pressureSensor(0, x, 10))

sine = sndobj.HarmTable(1000, 20, sndobj.SINE)
saw = sndobj.HarmTable(1000, 20, sndobj.SAW)
square = sndobj.HarmTable(1000, 20, sndobj.SQUARE)
buzz = sndobj.HarmTable(1000, 20, sndobj.BUZZ)
osc1 = sndobj.Oscili(sine, 0, 0)
osc2 = sndobj.Oscili(sine, 0, 0)
osc3 = sndobj.Oscili(sine, 0, 0)
osc4 = sndobj.Oscili(sine, 0, 0)
comb1 = sndobj.Comb(0, 0.2, osc1)
comb2 = sndobj.Comb(0, 0.2, osc2)
comb3 = sndobj.Comb(0, 0.2, osc3)
comb4 = sndobj.Comb(0, 0.2, osc4)
#ring = sndobj.Ring(osc1, osc2)
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
mixer.AddObj(comb1)
mixer.AddObj(comb2)
mixer.AddObj(comb3)
mixer.AddObj(comb4)
#mixer.AddObj(ring)
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
thread.AddObj(comb1)
thread.AddObj(comb2)
thread.AddObj(comb3)
thread.AddObj(comb4)
#thread.AddObj(ring)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()

#amounts the frequency and amplitude of the oscillators will change by during each loop iteration
freqStep = 10
pressureStep = 40

#values with which to multiply the raw sensor values
pressureAdjust = 1
ampAdjust = 10
freqAdjust = 1

#chord cutoffs
dimCutoff = 200
minCutoff = 500
majCutoff = 700

#wave cutoffs
sineCutoff = 200
sawCutoff = 500
squareCutoff = 700

ampCutoff = 200

alreadySine = True
alreadySaw = False
alreadySquare = False
alreadyBuzz = False

pluckWait = 0.25
pluckTime = 0

combGainMult = 0.99

pressureValue = [0] * NUM_SENSORS
pressure = [0] * NUM_SENSORS
    
rhythmCount = 0
subtractMult = 5000
osc1subtract = 1
osc2subtract = osc1subtract * subtractMult
osc3subtract = osc2subtract * subtractMult
osc4subtract = osc3subtract * subtractMult

avgSamples = 10
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
    # Pressure sensors
    ###
    #get pressure sensor values
    for x in range(NUM_SENSORS):
        pressure[x] = sensors[x].getPressureValue() * pressureAdjust
        #print("Sensor " + str(x) + ": " + str(pressure[x]))
        #interpolate pressureValue
        if (pressureValue[x] < pressure[x]):
            #slide up
            if (pressureValue[x] + pressureStep < pressure[x]): pressureValue[x] += pressureStep
            else: pressureValue[x] = pressure[x]
        elif (pressureValue[x] > pressure[x]):
            #slide down
            if (pressureValue[x] - pressureStep > pressure[x]): pressureValue[x] -= pressureStep
            else: pressureValue[x] = pressure[x]
    
    print("Sensors: " + str(pressure))
        
    #osc1amp = pressureValue - osc1subtract
    #osc2amp = pressureValue - osc2subtract
    #osc3amp = pressureValue - osc3subtract
    #osc4amp = pressureValue - osc4subtract
    
    #set chord type
    if (pressureValue[CHORD_SENSOR] < dimCutoff):
        chord = "dim"
    elif (pressureValue[CHORD_SENSOR] < minCutoff):
        chord = "min"
    elif (pressureValue[CHORD_SENSOR] < majCutoff):
        chord = "maj"
    else: #(pressureValue[CHORD_SENSOR] < augCutoff):
        chord = "aug"
        
    print("Chord: " + chord)
    
    #set wave type
    if (pressureValue[FIXME_SENSOR] < sineCutoff):
        wave = "sine"
    elif (pressureValue[FIXME_SENSOR] < sawCutoff):
        wave = "saw"
    elif (pressureValue[FIXME_SENSOR] < squareCutoff):
        wave = "square"
    else: #(pressureValue[FIXME_SENSOR] < buzzCutoff):
        wave = "buzz"
        
    print ("Wave: " + wave)
    
    if (wave == "sine" and alreadySine == False):
        osc1.SetTable(sine)
        osc2.SetTable(sine)
        osc3.SetTable(sine)
        osc4.SetTable(sine)
        alreadySine = True
        alreadySaw = False
        alreadySquare = False
        alreadyBuzz = False
    elif (wave == "saw" and alreadySaw == False):
        osc1.SetTable(saw)
        osc2.SetTable(saw)
        osc3.SetTable(saw)
        osc4.SetTable(saw)
        alreadySine = False
        alreadySaw = True
        alreadySquare = False
        alreadyBuzz = False
    elif (wave == "square" and alreadySquare == False):
        osc1.SetTable(square)
        osc2.SetTable(square)
        osc3.SetTable(square)
        osc4.SetTable(square)
        alreadySine = False
        alreadySaw = False
        alreadySquare = True
        alreadyBuzz = False
    elif (alreadyBuzz == False):
        osc1.SetTable(buzz)
        osc2.SetTable(buzz)
        osc3.SetTable(buzz)
        osc4.SetTable(buzz)
        alreadySine = False
        alreadySaw = False
        alreadySquare = False
        alreadyBuzz = True
        
        
    #print("osc1amp: " + str(osc4amp))    
    #set amplitudes
    osc1.SetAmp(osc1amp)
    osc2.SetAmp(osc2amp)
    osc3.SetAmp(osc3amp)
    osc4.SetAmp(osc4amp)


    if (pressureValue[AMP_SENSOR] < ampCutoff):
        amp = 0
    else:
        amp = pressureValue[AMP_SENSOR] * ampAdjust
    print("Amplitude: " + str(amp))
    
    osc1.SetAmp(amp)
    osc2.SetAmp(amp)
    osc3.SetAmp(amp)
    osc4.SetAmp(amp)
    #buzz.SetAmp(amp)
    
    #pluckWait = 500.0 / amp
    #print("Pluck delay: " + str(pluckWait))
    
    #if ((time.time() - pluckTime) > pluckWait):
        #pluck1.SetAmp(amp)
        #pluckTime = time.time()
    
    freq = pressureValue[FIXME_SENSOR] * freqAdjust
    print("Frequency: " + str(freq))
    
    if (freq != 0):
        # root
        osc1freq = freq
        # fifth
        osc2freq = osc1freq * (3/2)
        # third
        osc3freq = osc1freq * (osc1freq * 5) / (osc2freq * 4)
        # octave
        osc4freq = osc1freq * 2
    else:
        osc1freq = 0
        osc2freq = 0
        osc3freq = 0
        osc4freq = 0
        
    if (chord == "dim"):
        osc2freq = osc3freq * (2^(-1/12))
        osc3freq = osc3freq * (2^(-1/12))
    elif (chord == "min"):
        osc3freq = osc3freq * (2^(-1/12))
    elif (chord == "aug"):
        osc2freq = osc3freq * (2^(1/12))
        osc3freq = osc3freq * (2^(1/12))
        
    #pluck1freq = 700 #this does nothing
    
    #buzz.SetFreq(amp / 2)
    #buzz.SetHarm(amp / 20)
    
    #set frequencies
    osc1.SetFreq(osc1freq, mod)
    osc2.SetFreq(osc2freq, mod)
    osc3.SetFreq(osc3freq, mod)
    osc4.SetFreq(osc4freq, mod)
    
    #comb
    comb1.SetGain(((pressureValue[COMB_SENSOR] / pressureAdjust) / 1024) * combGainMult)
    comb2.SetGain(((pressureValue[COMB_SENSOR] / pressureAdjust) / 1024) * combGainMult)
    comb3.SetGain(((pressureValue[COMB_SENSOR] / pressureAdjust) / 1024) * combGainMult)
    comb4.SetGain(((pressureValue[COMB_SENSOR] / pressureAdjust) / 1024) * combGainMult)
    
    #panning
    pan.SetPan((pressureValue[PAN_SENSOR] / 512.0) - 1)
    
    print("")

    #wait before doing another iteration
    time.sleep(0.05)
thread.ProcOff()
