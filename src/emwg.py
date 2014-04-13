import sndobj
from acceltest import *

accelObj = accel()

harmTable = sndobj.HarmTable()
harmTable.SetHarm(100, sndobj.SINE)
osc1 = sndobj.Oscili(harmTable, 440, 900)

# Create a mixer
mixer = sndobj.Mixer()
mixer.AddObj(osc1)
#mixer.AddObj(sound2)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
out.SetOutput(1, mixer)
#out.SetOutput(1, osc1)

#mod = sndobj.Oscili(harmTable, 2, 150)
#osc1.SetFreq(440, mod)

thread = sndobj.SndThread()

# Attach sound objects to the sound thread
thread.AddObj(osc1)
#thread.AddObj(sound2)
thread.AddObj(mixer)
#thread.AddObj(mod)
#thread.AddObj(noise)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

while True:
    accelObj.runAccel(osc1)