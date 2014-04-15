import sndobj
import time
import psutil
from pressureSensor import *
from toneLibrary import *
    
class pressureThing:

    def __init__(self, sleepTime, mixer, thread):
        
        print("Creating pressureThing object")
        
        #Constants
        self.NUM_SENSORS = 3
    
        self.CHORD_SENSOR = 2
        self.STRUM_SENSOR = 1
        self.SPEED_SENSOR = 0
            
        self.SLEEP_TIME = 0.05
            
        self.sensors = []
        self.chord1 = []
        self.chord2 = []
        self.chord3 = []
        self.chord4 = []
            
        self.chord1amp = 0
        self.chord2amp = 0
        self.chord3amp = 0
        self.chord4amp = 0
            
        #amounts the frequency and amplitude of the oscillators will change by during each loop iteration
        self.freqStep = 10
        self.pressureStep = 40
                
        #values by which to multiply the raw sensor values
        self.pressureAdjust = 1
        self.ampAdjust = 10
        self.freqAdjust = 1
                
        #chord cutoffs
        self.chord1Cutoff = 575
        self.chord2Cutoff = 660
        self.chord3Cutoff = 710
                
        self.ampCutoff = 200
            
        self.pluckWaitCutoff1 = 540
        self.pluckWaitCutoff2 = 620
        self.pluckWait1 = self.SLEEP_TIME * 3
        self.pluckWait2 = self.SLEEP_TIME * 2
        self.pluckWait3 = self.SLEEP_TIME
        self.pluckWait = self.pluckWait1
        self.pluckTime = 0
        self.pluckIndex = 0
        self.strumCutoff = 525
        self.strummed = False
        
        self.pressureValue = [0] * self.NUM_SENSORS
        self.pressure = [0] * self.NUM_SENSORS
                
        self.avgSysInfoSamples = 10
        self.sysInfoSamples = 0
        self.ramSum = 0
        self.cpuSum = 0
        self.avgRam = 0
        self.avgCpu = 0
                
        self.avgSensorSamples = 2
        #avgSensorLoopIterations = avgSensorSamples * NUM_SENSORS
        self.sensorSamples = [0] * self.NUM_SENSORS
        self.pressureSums = [0] * self.NUM_SENSORS
        
        self.SLEEP_TIME = sleepTime
        
        for x in range(self.NUM_SENSORS):
            self.sensors.append(pressureSensor(0, x, 10))
            
        #build chords
        #C
        self.chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
        self.chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("E3"), 0))
        self.chord1.append(sndobj.Pluck(toneLibrary.getToneToFreq("G3"), 0))
        
        #D
        self.chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("D3"), 0))
        self.chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("Fs3"), 0))
        self.chord2.append(sndobj.Pluck(toneLibrary.getToneToFreq("A3"), 0))
        
        #G
        self.chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("G3"), 0))
        self.chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("B3"), 0))
        self.chord3.append(sndobj.Pluck(toneLibrary.getToneToFreq("D3"), 0))
        
        #am
        self.chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("A3"), 0))
        self.chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("C3"), 0))
        self.chord4.append(sndobj.Pluck(toneLibrary.getToneToFreq("E3"), 0))
        
        out = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
        #mixer = sndobj.Mixer()
        
        for x in self.chord1:
            mixer.AddObj(x)
        
        for x in self.chord2:
            mixer.AddObj(x)
        
        for x in self.chord3:
            mixer.AddObj(x)
        
        for x in self.chord4:
            mixer.AddObj(x)
        
        pan = sndobj.Pan(0, mixer)
        #thread = sndobj.SndThread()
        out.SetOutput(1, pan.left)
        out.SetOutput(2, pan.right)
        
        for x in self.chord1:
            thread.AddObj(x)
            
        for x in self.chord2:
            thread.AddObj(x)
            
        for x in self.chord3:
            thread.AddObj(x)
            
        for x in self.chord4:
            thread.AddObj(x)
        
        thread.AddObj(mixer)
        thread.AddObj(pan)
        thread.AddObj(out, sndobj.SNDIO_OUT)
        
        #thread.ProcOn()
        
        print("Finished creating pressureThing object")

    def step(self):
        
        print("Beginning pressureThing step")
        print(str(self.ramSum))
        print(str(self.ramSum + 1))
        self.ramSum += 1
        print(str(self.ramSum))
    
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
