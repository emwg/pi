import sndobj
from acceltest import *
from microphoneTest import *
from pressureThing import *
from lighttest import *
import time

SLEEP_TIME = 0.05

mixer = sndobj.Mixer()
thread = sndobj.SndThread()

accelObj = accel()
microphonesObj = microphones()
pressureObj = pressureThing(SLEEP_TIME)
lightObj = lightThing()

###
# set up light object things
###
lsine = sndobj.HarmTable(1000, 20, sndobj.SINE)
lsaw = sndobj.HarmTable(1000, 20, sndobj.SAW)
lsquare = sndobj.HarmTable(1000, 20, sndobj.SQUARE)
lbuzz = sndobj.HarmTable(1000, 20, sndobj.BUZZ)
losc1 = sndobj.Oscili(lsine, 0, 0)
losc2 = sndobj.Oscili(lsine, 0, 0)
losc3 = sndobj.Oscili(lsine, 0, 0)
losc4 = sndobj.Oscili(lsine, 0, 0)
lcomb1 = sndobj.Comb(0, 0.2, losc1)
lcomb2 = sndobj.Comb(0, 0.2, losc2)
lcomb3 = sndobj.Comb(0, 0.2, losc3)
lcomb4 = sndobj.Comb(0, 0.2, losc4)
lmod = sndobj.Oscili(lsine, 0, 100)


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
osc1 = sndobj.Oscili(harmTable, 0, 1200)
osc2 = sndobj.Oscili(harmTable, 0, 1000)

# Add things to mixer
mixer.AddObj(osc1)
mixer.AddObj(osc2)
#mixer.AddObj(sound2)

mixer.AddObj(losc1)
mixer.AddObj(losc2)
mixer.AddObj(losc3)
mixer.AddObj(losc4)
mixer.AddObj(lcomb1)
mixer.AddObj(lcomb2)
mixer.AddObj(lcomb3)
mixer.AddObj(lcomb4)

out = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
pan = sndobj.Pan(0, mixer)
out.SetOutput(1, pan.left)
out.SetOutput(2, pan.right)


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

thread.AddObj(lmod)
thread.AddObj(losc1)
thread.AddObj(losc2)
thread.AddObj(losc3)
thread.AddObj(losc4)
thread.AddObj(mixer)
thread.AddObj(pan)
thread.AddObj(lcomb1)
thread.AddObj(lcomb2)
thread.AddObj(lcomb3)
thread.AddObj(lcomb4)

thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

osc2.SetFreq(0)

while True:
    accelObj.runAccel(osc2)
    microphonesObj.runMicrophones(osc1)
    pressureObj.step(chord1, chord2, chord3, chord4)
    lightObj.step(losc1, losc2, losc3, losc4, lsine, lsaw, lsquare, lbuzz, lcomb1, lcomb2, lcomb3, lcomb4, lmod, pan)
    time.sleep(0.05)
