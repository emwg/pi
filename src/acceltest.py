import sndobj
import time
import psutil
from accelsensor import *

accel = accelSensor(1, 10)

harmTable = sndobj.HarmTable()
harmTable.SetHarm(1, sndobj.SAW)
osc1 = sndobj.Oscili(harmTable, 0, 0)
osc1.SetAmp(3000)
osc1.SetFreq(1600)

mixer = sndobj.Mixer()
mixer.addObj(osc1)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
thread = sndobj.SndThread()
out.setOutput(1, mixer)

thread.AddObj(osc1)
thread.AddObj(mixer)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

while True:
	ocs1.SetAmp(3000)
