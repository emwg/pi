import sndobj
from microphoneSensor import *
from toneLibrary import *

microphone = microphoneSensor(0, 0, 10)
toneLib = toneLibrary()
middleC = toneLib.getToneToFreq('C4')

harmTable = sndobj.HarmTable(1024, 100, sndobj.SINE)
osc = sndobj.Oscili(harmTable, toneLib.getToneToFreq('C4'), 900)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
out.SetOutput(1, osc)

thread = sndobj.SndThread()
thread.AddObj(osc)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

currentAvgIndex = 0
avgValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
while True:
    microphoneValue = microphone.getMicrophoneValue()
    avgValue[currentAvgIndex] = microphoneValue
    if(currentAvgIndex < 19):
        currentAvgIndex +=1
    else:
        currentAvgIndex = 0
    avgMicrophoneValue = 0
    summedValues = 0
    for avgM in avgValue:
        if(avgM > 500):
            avgMicrophoneValue += avgM
            summedValues += 1
    avgMicrophoneValue /= summedValues
    if avgMicrophoneValue > 600:
        print("Microphone High" + str(avgMicrophoneValue))
    else: print("Microphone Low " + str(avgMicrophoneValue))
    #print(avgValue)
    '''
    if avgMicrophoneValue - 500 < 0 or avgMicrophoneValue - 500 > 100:
        osc.SetFreq(1318)
    else:
        osc.SetFreq(middleC)'''