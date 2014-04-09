import sndobj
import time
import psutil
from pressureSensor import *
from toneLibrary import *

NUM_SENSORS = 3

CHORD_SENSOR = 0
STRUM_SENSOR = 1
PITCH_SENSOR = 2
FIXME_SENSOR = 0

sensors = []

for x in range(NUM_SENSORS):
    sensors.append(pressureSensor(0, x, 10))
    
#build chords
#C
chord1 = []
chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("D3"), 0))
chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("Fs3"), 0))
chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("A3"), 0))

#D
chord2 = []
chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))

#G
chord3 = []
chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("G3"), 0))
chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("B3"), 0))
chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("D3"), 0))

#another chord
chord4 = []
chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))

chord1amp = 0
chord2amp = 0
chord3amp = 0
chord4amp = 0
out = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
mixer = sndobj.Mixer()

for x in chord1:
    mixer.AddObj(x)

for x in chord2:
    mixer.AddObj(x)

for x in chord3:
    mixer.AddObj(x)

for x in chord4:
    mixer.AddObj(x)

pan = sndobj.Pan(0, mixer)
thread = sndobj.SndThread()
out.SetOutput(1, pan.left)
out.SetOutput(2, pan.right)

for x in chord1:
    thread.AddObj(x)
    
for x in chord2:
    thread.AddObj(x)
    
for x in chord3:
    thread.AddObj(x)
    
for x in chord4:
    thread.AddObj(x)

thread.AddObj(mixer)
thread.AddObj(pan)
thread.AddObj(out, sndobj.SNDIO_OUT)

thread.ProcOn()

#amounts the frequency and amplitude of the oscillators will change by during each loop iteration
freqStep = 10
pressureStep = 40

#values by which to multiply the raw sensor values
pressureAdjust = 1
ampAdjust = 10
freqAdjust = 1

#chord cutoffs
chord1Cutoff = 200
chord2Cutoff = 500
chord3Cutoff = 700

ampCutoff = 200

pluckWait = 0.15
pluckTime = 0
pluckIndex = 0
strumCutoff = 600
strummed = False

pressureValue = [0] * NUM_SENSORS
pressure = [0] * NUM_SENSORS

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
    if (pressureValue[CHORD_SENSOR] < chord1Cutoff):
        chord = 1
    elif (pressureValue[CHORD_SENSOR] < chord2Cutoff):
        chord = 2
    elif (pressureValue[CHORD_SENSOR] < chord3Cutoff):
        chord = 3
    else: #(pressureValue[CHORD_SENSOR] < chord4Cutoff):
        chord = 4
        
    print("Chord: " + str(chord))


    if (pressureValue[STRUM_SENSOR] < ampCutoff):
        amp = 0
    else:
        amp = pressureValue[STRUM_SENSOR] * ampAdjust
    print("Amplitude: " + str(amp))
    
    for x in chord1:
        x.SetAmp(amp)
    
    for x in chord2:
        x.SetAmp(amp)
    
    for x in chord3:
        x.SetAmp(amp)
    
    for x in chord4:
        x.SetAmp(amp)
    
    #check to see if a strum should happen
    if (pressureValue[STRUM_SENSOR] > strumCutoff):
        strummed = False
        print("WE WILL DO A STRUM")
    else:
        print("NO STRUMS FOR US")
        pluckIndex = 0
        strummed = True
    
    #do a strum maybe
    if (((time.time() - pluckTime) > pluckWait) and strummed == False):
        print("NOW WE ARE STRUMMING")
        chord1[pluckIndex].RePluck()
        if pluckIndex < len(chord1) - 1:
            pluckIndex += 1
        else:
            pluckIndex = 0
            strummed = True
        pluckTime = time.time()
    
    #panning
    #pan.SetPan((pressureValue[PAN_SENSOR] / 512.0) - 1)
    
    print("")

    #wait before doing another iteration
    time.sleep(0.05)
thread.ProcOff()
