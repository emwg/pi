import sndobj
import time
import psutil
from lightSensor import *

class lightThing:
    
    def __init__(self):

        self.NUM_SENSORS = 6
    
        self.CHORD_SENSOR = 0
        self.AMP_SENSOR = 1
        self.PAN_SENSOR = 2
        self.COMB_SENSOR = 3
        self.FREQ_SENSOR = 4
        self.WAVE_SENSOR = 5
    
        self.sensors = []
    
        for x in range(self.NUM_SENSORS):
            self.sensors.append(lightSensor(1, x, 10))
    
        self.osc1amp = 0
        self.osc2amp = 0
        self.osc3amp = 0
        self.osc4amp = 0
        self.pluck1amp = 0
        self.osc1freq = 100
        self.osc2freq = 200
        self.osc3freq = 300
        self.osc4freq = 400
        self.pluck1freq = 0
    
        #amounts the frequency and amplitude of the oscillators will change by during each loop iteration
        self.freqStep = 10
        self.lightStep = 40
    
        #values with which to multiply the raw sensor values
        self.lightAdjust = 1
        self.flexAdjust = 1
        self.knobAdjust = 0.1
        self.ampAdjust = 10
        self.freqAdjust = 1
    
        #chord cutoffs
        self.dimCutoff = 350
        self.minCutoff = 650
        self.majCutoff = 750
    
        #wave cutoffs
        self.sineCutoff = 350
        self.sawCutoff = 450
        self.squareCutoff = 750
    
        self.ampCutoff = 350
    
        self.alreadySine = True
        self.alreadySaw = False
        self.alreadySquare = False
        self.alreadyBuzz = False
    
        self.combGainMult = 0.99
    
        self.lightValue = [0] * self.NUM_SENSORS
        self.light = [0] * self.NUM_SENSORS
        
        self.rhythmCount = 0
        self.subtractMult = 5000
        self.osc1subtract = 1
        self.osc2subtract = self.osc1subtract * self.subtractMult
        self.osc3subtract = self.osc2subtract * self.subtractMult
        self.osc4subtract = self.osc3subtract * self.subtractMult
    
        self.avgSamples = 10
        self.samples = 0
        self.ramSum = 0
        self.cpuSum = 0
        self.avgRam = 0
        self.avgCpu = 0

    def step(self, osc1, osc2, osc3, osc4, sine, saw, square, buzz, comb1, comb2, comb3, comb4, mod, pan):
    
        #print system info
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=0)
        
        if (self.samples < self.avgSamples):
            self.ramSum += ram
            self.cpuSum += cpu
            self.samples += 1
        else:
            self.avgRam = (self.ramSum / self.avgSamples)
            self.avgCpu = (self.cpuSum / self.avgSamples)
            self.samples = 0
            self.ramSum = 0
            self.cpuSum = 0
        
        #print("RAM usage: " + str(self.avgRam) + "%")
        #print("CPU usage: " + str(self.avgCpu) + "%")
        
        ###
        # Light sensor
        ###
        #get light sensor values
        for x in range(self.NUM_SENSORS):
            self.light[x] = self.sensors[x].getLightValue() * self.lightAdjust
            #print("Sensor " + str(x) + ": " + str(light[x]))
            #interpolate lightValue
            if (self.lightValue[x] < self.light[x]):
                #slide up
                if (self.lightValue[x] + self.lightStep < self.light[x]): self.lightValue[x] += self.lightStep
                else: self.lightValue[x] = self.light[x]
            elif (self.lightValue[x] > self.light[x]):
                #slide down
                if (self.lightValue[x] - self.lightStep > self.light[x]): self.lightValue[x] -= self.lightStep
                else: self.lightValue[x] = self.light[x]
        
       # print("Sensors: " + str(self.light))
            
        #osc1amp = lightValue - osc1subtract
        #osc2amp = lightValue - osc2subtract
        #osc3amp = lightValue - osc3subtract
        #osc4amp = lightValue - osc4subtract
        
        #set chord type
        if (self.lightValue[self.CHORD_SENSOR] < self.dimCutoff):
            chord = "dim"
        elif (self.lightValue[self.CHORD_SENSOR] < self.minCutoff):
            chord = "min"
        elif (self.lightValue[self.CHORD_SENSOR] < self.majCutoff):
            chord = "maj"
        else: #(self.lightValue[self.CHORD_SENSOR] < self.augCutoff):
            chord = "aug"
            
        #print("Chord: " + chord)
        
        #set wave type
        if (self.lightValue[self.WAVE_SENSOR] < self.sineCutoff):
            wave = "sine"
        elif (self.lightValue[self.WAVE_SENSOR] < self.sawCutoff):
            wave = "saw"
        elif (self.lightValue[self.WAVE_SENSOR] < self.squareCutoff):
            wave = "square"
        else: #(self.lightValue[self.WAVE_SENSOR] < self.buzzCutoff):
            wave = "buzz"
            
        #print ("Wave: " + wave)
        
        if (wave == "sine" and self.alreadySine == False):
            osc1.SetTable(sine)
            osc2.SetTable(sine)
            osc3.SetTable(sine)
            osc4.SetTable(sine)
            self.alreadySine = True
            self.alreadySaw = False
            self.alreadySquare = False
            self.alreadyBuzz = False
        elif (wave == "saw" and self.alreadySaw == False):
            osc1.SetTable(saw)
            osc2.SetTable(saw)
            osc3.SetTable(saw)
            osc4.SetTable(saw)
            self.alreadySine = False
            self.alreadySaw = True
            self.alreadySquare = False
            self.alreadyBuzz = False
        elif (wave == "square" and self.alreadySquare == False):
            osc1.SetTable(square)
            osc2.SetTable(square)
            osc3.SetTable(square)
            osc4.SetTable(square)
            self.alreadySine = False
            self.alreadySaw = False
            self.alreadySquare = True
            self.alreadyBuzz = False
        elif (self.alreadyBuzz == False):
            osc1.SetTable(buzz)
            osc2.SetTable(buzz)
            osc3.SetTable(buzz)
            osc4.SetTable(buzz)
            self.alreadySine = False
            self.alreadySaw = False
            self.alreadySquare = False
            self.alreadyBuzz = True
            
            
        #print("osc1amp: " + str(osc4amp))    
        #set amplitudes
        osc1.SetAmp(self.osc1amp)
        osc2.SetAmp(self.osc2amp)
        osc3.SetAmp(self.osc3amp)
        osc4.SetAmp(self.osc4amp)
    
    
        if (self.lightValue[self.AMP_SENSOR] < self.ampCutoff):
            amp = 0
        else:
            amp = self.lightValue[self.AMP_SENSOR] * self.ampAdjust
        #print("Amplitude: " + str(amp))
        
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
        
        freq = self.lightValue[self.FREQ_SENSOR] * self.freqAdjust
        #print("Frequency: " + str(freq))
        
        if (freq != 0):
            # root
            self.osc1freq = freq
            # fifth
            self.osc2freq = self.osc1freq * (3/2)
            # third
            self.osc3freq = self.osc1freq * (self.osc1freq * 5) / (self.osc2freq * 4)
            # octave
            self.osc4freq = self.osc1freq * 2
        else:
            self.osc1freq = 0
            self.osc2freq = 0
            self.osc3freq = 0
            self.osc4freq = 0
            
        if (chord == "dim"):
            self.osc2freq = self.osc3freq * (2^(-1/12))
            self.osc3freq = self.osc3freq * (2^(-1/12))
        elif (chord == "min"):
            self.osc3freq = self.osc3freq * (2^(-1/12))
        elif (chord == "aug"):
            self.osc2freq = self.osc3freq * (2^(1/12))
            self.osc3freq = self.osc3freq * (2^(1/12))
            
        #pluck1freq = 700 #this does nothing
        
        #buzz.SetFreq(amp / 2)
        #buzz.SetHarm(amp / 20)
        
        #set frequencies
        osc1.SetFreq(self.osc1freq, mod)
        osc2.SetFreq(self.osc2freq, mod)
        osc3.SetFreq(self.osc3freq, mod)
        osc4.SetFreq(self.osc4freq, mod)
        
        #comb
        comb1.SetGain(((self.lightValue[self.COMB_SENSOR] / self.lightAdjust) / 1024) * self.combGainMult)
        comb2.SetGain(((self.lightValue[self.COMB_SENSOR] / self.lightAdjust) / 1024) * self.combGainMult)
        comb3.SetGain(((self.lightValue[self.COMB_SENSOR] / self.lightAdjust) / 1024) * self.combGainMult)
        comb4.SetGain(((self.lightValue[self.COMB_SENSOR] / self.lightAdjust) / 1024) * self.combGainMult)
        
        #panning
        pan.SetPan((self.lightValue[self.PAN_SENSOR] / 512.0) - 1)
        
        #print("")
    
        #wait before doing another iteration
        time.sleep(0.05)
