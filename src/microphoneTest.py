import sndobj
from microphoneSensor import *
from toneLibrary import *

microphone = microphoneSensor(0, 2, 10)
toneLib = toneLibrary()
middleC = toneLib.getToneToFreq('C4')

harmTable = sndobj.HarmTable(1024, 100, sndobj.SINE)
osc = sndobj.Oscili(harmTable, middleC, 900)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)

thread = sndobj.SndThread()
thread.AddObj(osc)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

while True:
    microphoneValue = microphone.getMicrophoneValue()
    print("Microphone: " + str(microphoneValue))
    #osc.SetFreq(middleC + microphoneValue)