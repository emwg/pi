import sndobj
from acceltest import *
from microphoneTest import *
from pressureThing import *

SLEEP_TIME = 0.05

mixer = sndobj.Mixer()
thread = sndobj.SndThread()

accelObj = accel()
microphonesObj = microphones()
pressureObj = pressureThing(SLEEP_TIME, mixer, thread)

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
    #print("Accel step")
    #accelObj.runAccel(osc2)
    #print("Mic step")
    #microphonesObj.runMicrophones(osc1)
    print("Press step")
