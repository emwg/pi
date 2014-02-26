import sndobj
import time
import psutil
from accelsensor import *
from toneLibrary import *

# Create the accelerometer sensor objects
accelY = accelSensor(0, 10)

# Create toneLibrary object
toneLib = toneLibrary()
currentTone = 'C2'

# Create the harmonic table and attach to oscilators
# The higher the first parameter in harmTable.SetHarm is, the buzzier the sound
#coeffs = [4.0, 2.0];
harmTable = sndobj.HarmTable()
harmTable.SetHarm(100, sndobj.SINE)
osc1 = sndobj.Oscili(harmTable, 440, 900)
osc1.SetAmp(9000)
osc1.SetFreq(600)

# Create a mixer
mixer = sndobj.Mixer()
mixer.AddObj(osc1)

out = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
thread = sndobj.SndThread()
out.SetOutput(1, mixer)

# Attach sound objects to the sound thread
thread.AddObj(osc1)
thread.AddObj(mixer)
thread.AddObj(out, sndobj.SNDIO_OUT)
thread.ProcOn()

deltaT = time.time()

while True:
	# Get the accelerometer values, ranging from ~(400-600), print out
	accelYValue = accelY.getAccelValue()
	print("AccelY:" + str(accelYValue))
	
	if(time.time() > deltaT):
		deltaT = time.time()
		currentTone = toneLib.upSteps(2, currentTone)
		osc1.SetFreq(toneLib.toneToFreq(currentTone))
	#newAmp = (accelYValue - 400)
	#if(newAmp < 0): newAmp = 0
	#osc1.SetAmp(newAmp * 20)
	
