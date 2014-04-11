import sndobj
from microphoneSensor import *
from toneLibrary import *
import time

def calculateMicStatus(micNum):
    micValue = microphone[micNum].getMicrophoneValue()
    avgValue[micNum][currentAvgIndex[micNum]] = micValue
    if(currentAvgIndex[micNum] < 19):
        currentAvgIndex[micNum] += 1
    else:
        currentAvgIndex[micNum] = 0
    avgMicValue = 0
    summedValues = 0
    for avgM in avgValue[micNum]:
        if(avgM > 500):
            avgMicValue += avgM
            summedValues += 1
    avgMicValue /= summedValues
    if (avgMicValue >= 600):
        return 1
    return 0

microphone = []
microphone.append(microphoneSensor(2, 3, 10))
microphone.append(microphoneSensor(2, 4, 10))
microphone.append(microphoneSensor(2, 5, 10))
microphone.append(microphoneSensor(2, 6, 10))
toneLib = toneLibrary()
middleC = toneLib.getToneToFreq('C4')

twelveToneTable = dict([])
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
twelveToneTable['RI11'] = ['F4', 'Fs4', 'A4', 'As4', 'D4', 'Ds4', 'C4', 'Cs4', 'E4', 'G4', 'Gs4', 'B4']


harmTable = sndobj.HarmTable(1024, 100, sndobj.SINE)
osc = sndobj.Oscili(harmTable, toneLib.getToneToFreq('C4'), 900)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
out.SetOutput(1, osc)

thread = sndobj.SndThread()
thread.AddObj(osc)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

currentAvgIndex = []
currentAvgIndex.append(0)
currentAvgIndex.append(0)
currentAvgIndex.append(0)
currentAvgIndex.append(0)
avgValue = []
avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
avgValue.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

deltaT = time.time()
currentToneTable = 'null'
previousToneTable = ''
newToneTableFlag = False
stepTime = 0.1
toneTableIndex = 0
while True:
    mic0Status = calculateMicStatus(0)
    mic1Status = calculateMicStatus(1)
    mic2Status = calculateMicStatus(2)
    mic3Status = calculateMicStatus(3)
    
    micStatus = str(mic0Status) + str(mic1Status) + str(mic2Status) + str(mic3Status)

    if(micStatus == "0000"):
        currentToneTable = 'null'
    elif(micStatus == "0001"):
        currentToneTable = 'I0'
    elif(micStatus == "0010"):
        currentToneTable = 'P3'
    elif(micStatus == "0011"):
        currentToneTable = 'P5'
    elif(micStatus == "0100"):
        currentToneTable = 'R3'
    elif(micStatus == "0101"):
        currentToneTable = 'I9'
    elif(micStatus == "0110"):
        currentToneTable = 'P0'
    elif(micStatus == "0111"):
        currentToneTable = 'I7'
    elif(micStatus == "1000"):
       currentToneTable = 'RI0'
    elif(micStatus == "1001"):
       currentToneTable = 'P0'
    elif(micStatus == "1010"):
        currentToneTable = 'RI9'
    elif(micStatus == "1011"):
        currentToneTable = 'RI11'
    elif(micStatus == "1100"):
        currentToneTable = 'R5'
    elif(micStatus == "1101"):
        currentToneTable = 'I11'
    elif(micStatus == "1110"):
        currentToneTable = 'RI7'
    elif(micStatus == "1111"):
        currentToneTable = 'P0'
        
    if(currentToneTable != previousToneTable):
        newToneTableFlag = True
        previousToneTable = currentToneTable
        toneTableIndex = 0
        
    if(stepTime > 0 and time.time() > deltaT + stepTime):
        print("Running")
        print("Status: [" + micStatus + "]")
        deltaT = time.time()
        if(currentToneTable != 'null'):
            currentTone = toneLib.getToneToFreq(twelveToneTable[currentToneTable][toneTableIndex])
            if(toneTableIndex == 11):
                toneTableIndex = 0
            else:
                toneTableIndex += 1
            print(currentTone)
            osc.SetFreq(currentTone)
        else:
            osc.SetFreq(0)
    
    