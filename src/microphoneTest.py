import sndobj
from microphoneSensor import *
from toneLibrary import *
import time

class microphones:
    
    def __init__(self):
        self.microphone = []
        self.microphone.append(microphoneSensor(2, 3, 10))
        self.microphone.append(microphoneSensor(2, 4, 10))
        self.microphone.append(microphoneSensor(2, 5, 10))
        self.microphone.append(microphoneSensor(2, 6, 10))
        self.toneLib = toneLibrary()
        self.middleC = toneLib.getToneToFreq('C4')
        
        self.twelveToneTable = dict([])
        self.twelveToneTable['P0'] = ['C4', 'Ds4', 'E4', 'G4', 'As4', 'B4', 'Gs4', 'A4', 'Cs4', 'D4', 'F4', 'Fs4']
        self.twelveToneTable['P3'] = ['Ds4', 'Fs4', 'G4', 'As4', 'Cs4', 'D4', 'B4', 'C4', 'E4', 'F4', 'Gs4', 'A4']
        self.twelveToneTable['P5'] = ['F4', 'Gs4', 'A4', 'C4', 'Ds4', 'E4', 'Cs4', 'D4', 'Fs4', 'G4', 'As4', 'B4']
        self.twelveToneTable['I0'] = ['C4', 'A4', 'Gs4', 'F4', 'D4', 'Cs4', 'E4', 'Ds4', 'B4', 'As4', 'G4', 'Fs4']
        self.twelveToneTable['I7'] = ['Cs4', 'As4', 'A4', 'Fs4', 'Ds4', 'D4', 'F4', 'E4', 'C4', 'B4', 'Gs4', 'G4']
        self.twelveToneTable['I9'] = ['A4', 'Fs4', 'F4', 'D4', 'B4', 'As4', 'Cs4', 'C4', 'Gs4', 'G4', 'E4', 'Ds4']
        self.twelveToneTable['I11'] = ['B4', 'Gs4', 'G4', 'E4', 'Cs4', 'C4', 'Ds4', 'D4', 'As4', 'A4', 'Fs4', 'F4']
        self.twelveToneTable['R3'] = ['A4', 'Gs4', 'F4', 'E4', 'C4', 'B4', 'D4', 'Cs4', 'As4', 'G4', 'Fs4', 'Ds4']
        self.twelveToneTable['R5'] = ['B4', 'As4', 'G4', 'Fs4', 'D4', 'Cs4', 'E4', 'Ds4', 'C4', 'A4', 'Gs4', 'F4']
        self.twelveToneTable['RI0'] = ['Fs4', 'G4', 'As4', 'B4', 'Ds4', 'E4', 'Cs4', 'D4', 'F4', 'Gs4', 'A4', 'C4']
        self.twelveToneTable['RI7'] = ['Cs4', 'D4', 'F4', 'Fs4', 'As4', 'B4', 'Gs4', 'A4', 'C4', 'Ds4', 'E4', 'G4']
        self.twelveToneTable['RI9'] = ['Ds4', 'E4', 'G4', 'Gs4', 'C4', 'Cs4', 'As4', 'B4', 'D4', 'F4', 'Fs4', 'A4']
        self.twelveToneTable['RI11'] = ['F4', 'Fs4', 'A4', 'As4', 'D4', 'Ds4', 'C4', 'Cs4', 'E4', 'G4', 'Gs4', 'B4']
        
        self.currentAvgIndex = []
        self.currentAvgIndex.append(0)
        self.currentAvgIndex.append(0)
        self.currentAvgIndex.append(0)
        self.currentAvgIndex.append(0)
        self.avgValue = []
        self.avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        self.deltaT = time.time()
        self.currentToneTable = 'null'
        self.previousToneTable = ''
        self.stepTime = 0.1
        self.toneTableIndex = 0
    
    def calculateMicStatus(self, micNum):
        micValue = self.microphone[micNum].getMicrophoneValue()
        avgValue[micNum][self.currentAvgIndex[micNum]] = micValue
        if(self.currentAvgIndex[micNum] < 19):
            self.currentAvgIndex[micNum] += 1
        else:
            self.currentAvgIndex[micNum] = 0
        avgMicValue = 0
        summedValues = 0
        for avgM in avgValue[micNum]:
            if(avgM > 500):
                avgMicValue += avgM
                summedValues += 1
        if(summedValues > 0):
            avgMicValue /= summedValues
        if (avgMicValue >= 600):
            return 1
        return 0
    
    '''microphone = []
    microphone.append(microphoneSensor(2, 3, 10))
    microphone.append(microphoneSensor(2, 4, 10))
    microphone.append(microphoneSensor(2, 5, 10))
    microphone.append(microphoneSensor(2, 6, 10))
    toneLib = toneLibrary()
    middleC = toneLib.getToneToFreq('C4')'''
    
    '''twelveToneTable = dict([])
    twelveToneTable['P0'] = ['C4', 'Ds4', 'E4', 'G4', 'As4', 'B4', 'Gs4', 'A4', 'Cs4', 'D4', 'F4', 'Fs4']
    twelveToneTable['P3'] = ['Ds4', 'Fs4', 'G4', 'As4', 'Cs4', 'D4', 'B4', 'C4', 'E4', 'F4', 'Gs4', 'A4']
    twelveToneTable['P5'] = ['F4', 'Gs4', 'A4', 'C4', 'Ds4', 'E4', 'Cs4', 'D4', 'Fs4', 'G4', 'As4', 'B4']
    twelveToneTable['I0'] = ['C4', 'A4', 'Gs4', 'F4', 'D4', 'Cs4', 'E4', 'Ds4', 'B4', 'As4', 'G4', 'Fs4']
    twelveToneTable['I7'] = ['Cs4', 'As4', 'A4', 'Fs4', 'Ds4', 'D4', 'F4', 'E4', 'C4', 'B4', 'Gs4', 'G4']
    twelveToneTable['I9'] = ['A4', 'Fs4', 'F4', 'D4', 'B4', 'As4', 'Cs4', 'C4', 'Gs4', 'G4', 'E4', 'Ds4']
    twelveToneTable['I11'] = ['B4', 'Gs4', 'G4', 'E4', 'Cs4', 'C4', 'Ds4', 'D4', 'As4', 'A4', 'Fs4', 'F4']
    twelveToneTable['R3'] = ['A4', 'Gs4', 'F4', 'E4', 'C4', 'B4', 'D4', 'Cs4', 'As4', 'G4', 'Fs4', 'Ds4']
    twelveToneTable['R5'] = ['B4', 'As4', 'G4', 'Fs4', 'D4', 'Cs4', 'E4', 'Ds4', 'C4', 'A4', 'Gs4', 'F4']
    twelveToneTable['RI0'] = ['Fs4', 'G4', 'As4', 'B4', 'Ds4', 'E4', 'Cs4', 'D4', 'F4', 'Gs4', 'A4', 'C4']
    twelveToneTable['RI7'] = ['Cs4', 'D4', 'F4', 'Fs4', 'As4', 'B4', 'Gs4', 'A4', 'C4', 'Ds4', 'E4', 'G4']
    twelveToneTable['RI9'] = ['Ds4', 'E4', 'G4', 'Gs4', 'C4', 'Cs4', 'As4', 'B4', 'D4', 'F4', 'Fs4', 'A4']
    twelveToneTable['RI11'] = ['F4', 'Fs4', 'A4', 'As4', 'D4', 'Ds4', 'C4', 'Cs4', 'E4', 'G4', 'Gs4', 'B4']'''
    
    
    harmTable = sndobj.HarmTable(1024, 100, sndobj.SINE)
    osc = sndobj.Oscili(harmTable, toneLib.getToneToFreq('C4'), 900)
    
    out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
    out.SetOutput(1, osc)
    
    thread = sndobj.SndThread()
    thread.AddObj(osc)
    thread.AddObj(out, sndobj.SNDIO_OUT)
    thread.ProcOn()
    
    '''currentAvgIndex = []
    currentAvgIndex.append(0)
    currentAvgIndex.append(0)
    currentAvgIndex.append(0)
    currentAvgIndex.append(0)
    avgValue = []
    avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])'''
    
    '''deltaT = time.time()
    currentToneTable = 'null'
    previousToneTable = ''
    stepTime = 0.1
    toneTableIndex = 0'''
    def runMicrophones(self, osc):
        mic0Status = self.calculateMicStatus(0)
        mic1Status = self.calculateMicStatus(1)
        mic2Status = self.calculateMicStatus(2)
        mic3Status = self.calculateMicStatus(3)
        
        micStatus = str(mic0Status) + str(mic1Status) + str(mic2Status) + str(mic3Status)
    
        if(micStatus == "0000"):
            self.currentToneTable = 'null'
        elif(micStatus == "0001"):
            self.currentToneTable = 'I0'
        elif(micStatus == "0010"):
            self.currentToneTable = 'P3'
        elif(micStatus == "0011"):
            self.currentToneTable = 'P5'
        elif(micStatus == "0100"):
            self.currentToneTable = 'R3'
        elif(micStatus == "0101"):
            self.currentToneTable = 'I9'
        elif(micStatus == "0110"):
            self.currentToneTable = 'P0'
        elif(micStatus == "0111"):
            self.currentToneTable = 'I7'
        elif(micStatus == "1000"):
            self.currentToneTable = 'RI0'
        elif(micStatus == "1001"):
            self.currentToneTable = 'P0'
        elif(micStatus == "1010"):
            self.currentToneTable = 'RI9'
        elif(micStatus == "1011"):
            self.currentToneTable = 'RI11'
        elif(micStatus == "1100"):
            self.currentToneTable = 'R5'
        elif(micStatus == "1101"):
            self.currentToneTable = 'I11'
        elif(micStatus == "1110"):
            self.currentToneTable = 'RI7'
        elif(micStatus == "1111"):
            self.currentToneTable = 'P0'
            
        if(self.currentToneTable != self.previousToneTable):
            self.previousToneTable = self.currentToneTable
            self.toneTableIndex = 0
            
        if(self.stepTime > 0 and time.time() > self.deltaT + self.stepTime):
            print("Running")
            print("Status: [" + micStatus + "]")
            self.deltaT = time.time()
            if(self.currentToneTable != 'null'):
                currentTone = self.toneLib.getToneToFreq(self.twelveToneTable[self.currentToneTable][self.toneTableIndex])
                if(self.toneTableIndex == 11):
                    self.toneTableIndex = 0
                else:
                    self.toneTableIndex += 1
                print(currentTone)
                osc.SetFreq(currentTone)
            else:
                osc.SetFreq(0)
    
    