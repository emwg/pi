import sndobj
import time
import psutil
from pressureSensor import *
from toneLibrary import *
    
class pressureThing:

    def __init__(self, sleepTime):
        
        print("Creating pressureThing object")
        
        #Constants
        self.NUM_SENSORS = 3
    
        self.CHORD_SENSOR = 2
        self.STRUM_SENSOR = 1
        self.SPEED_SENSOR = 0
            
        self.SLEEP_TIME = 0.05
            
        self.sensors = []
            
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
            
        
        #thread.AddObj(pan)
        
        #thread.ProcOn()'''
        
        #print("Finished creating pressureThing object")

    def step(self, chord1, chord2, chord3, chord4):
        
        print("Beginning pressureThing step")
    
        #print system info
        '''ram = psutil.virtual_memory().percent
        print("Got ram")
        cpu = psutil.cpu_percent(interval=0)
        print("Got cpu")
        
        if (self.sysInfoSamples < self.avgSysInfoSamples):
            self.ramSum += ram
            self.cpuSum += cpu
            self.sysInfoSamples += 1
        else:
            avgRam = (ramSum / avgSysInfoSamples)
            avgCpu = (cpuSum / avgSysInfoSamples)
            sysInfoSamples = 0
            ramSum = 0
            cpuSum = 0
        
        print("RAM usage: " + str(avgRam) + "%")
        print("CPU usage: " + str(avgCpu) + "%")'''
        
        ###
        # Pressure sensors
        ###
        #get pressure sensor values
        print("got past cpu")
        for x in range(self.NUM_SENSORS):
            print("in loop " + str(x))
            if (self.sensorSamples[x] < self.avgSensorSamples):
                self.pressureSums[x] += self.sensors[x].getPressureValue() * self.pressureAdjust
                print("preesureSum: " + str(self.pressureSums))
                self.sensorSamples[x] += 1
            else:
                self.pressure[x] = self.pressureSums[x] / self.avgSensorSamples
                self.sensorSamples[x] = 0
                self.pressureSums[x] = 0
                
            #pressure[x] = sensors[x].getPressureValue() * pressureAdjust
    
            #interpolate pressureValue
            if (self.pressureValue[x] < self.pressure[x]):
                #slide up
                if (self.pressureValue[x] + self.pressureStep < self.pressure[x]): self.pressureValue[x] += self.pressureStep
                else: self.pressureValue[x] = self.pressure[x]
            elif (self.pressureValue[x] > self.pressure[x]):
                #slide down
                if (self.pressureValue[x] - self.pressureStep > self.pressure[x]): self.pressureValue[x] -= self.pressureStep
                else: self.pressureValue[x] = self.pressure[x]
        
        print("out of loop")
        print("Sensors: " + str(self.pressure))
            
        #osc1amp = pressureValue - osc1subtract
        #osc2amp = pressureValue - osc2subtract
        #osc3amp = pressureValue - osc3subtract
        #osc4amp = pressureValue - osc4subtract
        
        #set chord type
        if (self.pressureValue[self.CHORD_SENSOR] < self.chord1Cutoff):
            chord = 1
        elif (self.pressureValue[self.CHORD_SENSOR] < self.chord2Cutoff):
            chord = 2
        elif (self.pressureValue[self.CHORD_SENSOR] < self.chord3Cutoff):
            chord = 3
        else: #(pressureValue[CHORD_SENSOR] < chord4Cutoff):
            chord = 4
            
        print("Chord: " + str(chord))
        
        #check to see if a strum should happen
        if (self.pressureValue[self.STRUM_SENSOR] > self.strumCutoff):
            strumming = True
            amp = pressureValue[STRUM_SENSOR] * ampAdjust
        else:
            self.pluckIndex = 0
            strumming = False
            amp = 0
            
        print("Amplitude: " + str(amp))
            
        #set strum speed
        if (self.pressureValue[self.SPEED_SENSOR] < self.pluckWaitCutoff1):
            self.pluckWait = self.pluckWait1
        elif (self.pressureValue[self.SPEED_SENSOR] < self.pluckWaitCutoff2):
            self.pluckWait = self.pluckWait2
        else:
            self.pluckWait = self.pluckWait3
        
        print ("Pluck wait: " + str(self.pluckWait))
        
        #do a strum maybe
        if (((time.time() - self.pluckTime) > self.pluckWait) and strumming == True):
            if chord == 1:
                chord1[self.pluckIndex].SetAmp(amp) #setting the amplitude also plucks it, which is dumb but whattayagonnado
            elif chord == 2:
                chord2[self.pluckIndex].SetAmp(amp)
            elif chord == 3:
                chord3[self.pluckIndex].SetAmp(amp)
            else: #chord == 4
                chord4[self.pluckIndex].SetAmp(amp)
                
            if self.pluckIndex < len(chord1) - 1: #all chord arrays should be the same length
                self.pluckIndex += 1
            else:
                self.pluckIndex = 0
            self.pluckTime = time.time()
        
        #panning
        #pan.SetPan((pressureValue[PAN_SENSOR] / 512.0) - 1)
        
        #print("")
    
        #wait before doing another iteration
        time.sleep(SLEEP_TIME)