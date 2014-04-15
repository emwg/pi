import sndobj
import time
import psutil
from pressureSensor import *
from toneLibrary import *

NUM_SENSORS = 3
    
CHORD_SENSOR = 2
STRUM_SENSOR = 1
SPEED_SENSOR = 0
    
SLEEP_TIME = 0.05
    
sensors = []
chord1 = []
chord2 = []
chord3 = []
chord4 = []
    
chord1amp = 0
chord2amp = 0
chord3amp = 0
chord4amp = 0
    
#amounts the frequency and amplitude of the oscillators will change by during each loop iteration
freqStep = 10
pressureStep = 40
        
#values by which to multiply the raw sensor values
pressureAdjust = 1
ampAdjust = 10
freqAdjust = 1
        
#chord cutoffs
chord1Cutoff = 575
chord2Cutoff = 660
chord3Cutoff = 710
        
ampCutoff = 200
    
pluckWaitCutoff1 = 540
pluckWaitCutoff2 = 620
pluckWait1 = SLEEP_TIME * 3
pluckWait2 = SLEEP_TIME * 2
pluckWait3 = SLEEP_TIME
pluckWait = pluckWait1
pluckTime = 0
pluckIndex = 0
strumCutoff = 525
strummed = False

pressureValue = [0] * NUM_SENSORS
pressure = [0] * NUM_SENSORS
        
avgSysInfoSamples = 10
sysInfoSamples = 0
ramSum = 0
cpuSum = 0
avgRam = 0
avgCpu = 0
        
avgSensorSamples = 2
#avgSensorLoopIterations = avgSensorSamples * NUM_SENSORS
sensorSamples = [0] * NUM_SENSORS
pressureSums = [0] * NUM_SENSORS
    
class pressureThing:

    def __init__(self, sleepTime, mixer, thread):
        
        print("Creating pressureThing object")
        
        SLEEP_TIME = sleepTime
        
        for x in range(NUM_SENSORS):
            sensors.append(pressureSensor(0, x, 10))
            
        #build chords
        #C
        chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
        chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("E3"), 0))
        chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("G3"), 0))
        
        #D
        chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("D3"), 0))
        chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("Fs3"), 0))
        chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("A3"), 0))
        
        #G
        chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("G3"), 0))
        chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("B3"), 0))
        chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("D3"), 0))
        
        #am
        chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("A3"), 0))
        chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
        chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("E3"), 0))
        
        out = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
        #mixer = sndobj.Mixer()
        
        for x in chord1:
            mixer.AddObj(x)
        
        for x in chord2:
            mixer.AddObj(x)
        
        for x in chord3:
            mixer.AddObj(x)
        
        for x in chord4:
            mixer.AddObj(x)
        
        pan = sndobj.Pan(0, mixer)
        #thread = sndobj.SndThread()
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
        
        #thread.ProcOn()
        
        print("Finished creating pressureThing object")

    def step(self):
        
        print("Beginning pressureThing step")
        print(str(ramsum))
        print(str(ramsum + 1))
        ramsum += 1
        print(str(ramsum))
    
        #print system info
        ram = psutil.virtual_memory().percent
        print("Got ram")
        cpu = psutil.cpu_percent(interval=0)
        print("Got cpu")
        
        if (sysInfoSamples < avgSysInfoSamples):
            ramSum += ram
            cpuSum += cpu
            sysInfoSamples += 1
        else:
            avgRam = (ramSum / avgSysInfoSamples)
            avgCpu = (cpuSum / avgSysInfoSamples)
            sysInfoSamples = 0
            ramSum = 0
            cpuSum = 0
        
        print("RAM usage: " + str(avgRam) + "%")
        print("CPU usage: " + str(avgCpu) + "%")
        
        ###
        # Pressure sensors
        ###
        #get pressure sensor values
        for x in range(NUM_SENSORS):
            if (sensorSamples[x] < avgSensorSamples):
                pressureSums[x] += sensors[x].getPressureValue() * pressureAdjust
                sensorSamples[x] += 1
            else:
                pressure[x] = pressureSums[x] / avgSensorSamples
                sensorSamples[x] = 0
                pressureSums[x] = 0
                
            #pressure[x] = sensors[x].getPressureValue() * pressureAdjust
    
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
        
        #check to see if a strum should happen
        if (pressureValue[STRUM_SENSOR] > strumCutoff):
            strumming = True
            amp = pressureValue[STRUM_SENSOR] * ampAdjust
        else:
            pluckIndex = 0
            strumming = False
            amp = 0
            
        print("Amplitude: " + str(amp))
            
        #set strum speed
        if (pressureValue[SPEED_SENSOR] < pluckWaitCutoff1):
            pluckWait = pluckWait1
        elif (pressureValue[SPEED_SENSOR] < pluckWaitCutoff2):
            pluckWait = pluckWait2
        else:
            pluckWait = pluckWait3
        
        print ("Pluck wait: " + str(pluckWait))
        
        #do a strum maybe
        if (((time.time() - pluckTime) > pluckWait) and strumming == True):
            if chord == 1:
                chord1[pluckIndex].SetAmp(amp) #setting the amplitude also plucks it, which is dumb but whattayagonnado
            elif chord == 2:
                chord2[pluckIndex].SetAmp(amp)
            elif chord == 3:
                chord3[pluckIndex].SetAmp(amp)
            else: #chord == 4
                chord4[pluckIndex].SetAmp(amp)
                
            if pluckIndex < len(chord1) - 1: #all chord arrays should be the same length
                pluckIndex += 1
            else:
                pluckIndex = 0
            pluckTime = time.time()
        
        #panning
        #pan.SetPan((pressureValue[PAN_SENSOR] / 512.0) - 1)
        
        print("")
    
        #wait before doing another iteration
        time.sleep(SLEEP_TIME)
