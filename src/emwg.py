import sndobj
from acceltest import *
from microphoneTest import *
from pressureThing import *

SLEEP_TIME = 0.05

mixer = sndobj.Mixer()
thread = sndobj.SndThread()

accelObj = accel()
microphonesObj = microphones()
pressureObj = pressureThing(SLEEP_TIME)


#build chords
chord1 = []
chord2 = []
chord3 = []
chord4 = []

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

#out = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
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
'''#thread = sndobj.SndThread()
out.SetOutput(1, pan.left)
out.SetOutput(2, pan.right)'''

for x in chord1:
    thread.AddObj(x)
    
for x in chord2:
    thread.AddObj(x)
    
for x in chord3:
    thread.AddObj(x)
    
for x in chord4:
    thread.AddObj(x)



harmTable = sndobj.HarmTable()
harmTable.SetHarm(100, sndobj.SINE)
osc1 = sndobj.Oscili(harmTable, 440, 600)
osc2 = sndobj.Oscili(harmTable, 440, 900)

# Add things to mixer
mixer.AddObj(osc1)
mixer.AddObj(osc2)
#mixer.AddObj(sound2)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
out.SetOutput(1, mixer)
#out.SetOutput(1, osc1)

#mod = sndobj.Oscili(harmTable, 2, 150)
#osc1.SetFreq(440, mod)



# Attach sound objects to the sound thread
thread.AddObj(osc1)
thread.AddObj(osc2)
#thread.AddObj(sound2)
thread.AddObj(mixer)
#thread.AddObj(mod)
#thread.AddObj(noise)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

osc2.SetFreq(0)

while True:
    accelObj.runAccel(osc2)
    microphonesObj.runMicrophones(osc1)
    pressureObj.step(chord1, chord2, chord3, chord4)
