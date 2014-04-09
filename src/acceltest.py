import sndobj
import time
import psutil
from accelsensor import *
from toneLibrary import *

# Create the accelerometer sensor objects
accelX = accelSensor(2, 0, 10)
accelY = accelSensor(2, 1, 10)
accelZ = accelSensor(2, 2, 10)

# Create toneLibrary object
toneLib = toneLibrary()
# Define tone library parameters
currentTone = 'C2'
lowestTone = 'C2'
highestTone = 'C3'
stepTime = 0.1

# Create the harmonic table and attach to oscilators
# The higher the first parameter in harmTable.SetHarm is, the buzzier the sound
#coeffs = [4.0, 2.0];
harmTable = sndobj.HarmTable()
harmTable.SetHarm(100, sndobj.SINE)
osc1 = sndobj.Oscili(harmTable, 440, 900)
sound2 = sndobj.Oscili(harmTable, 550, 900)
noise = sndobj.Randh(10000, 1000)
#osc1.SetAmp(6000)
#osc1.SetFreq(600)

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

deltaT = time.time()
scaleDirection = 'up'

while True:
	# Get the accelerometer values, ranging from ~(400-600), print out
	accelXValue = accelX.getAccelValue()
	accelYValue = accelY.getAccelValue()
	accelZValue = accelZ.getAccelValue()
	#mod.SetFreq(2 + (float(accelXValue)/100.0))
	#osc1.SetFreq(accelYValue, mod)
	print("AccelX: " + str(accelXValue))
	print("AccelY: " + str(accelYValue))
	print("AccelZ: " + str(accelZValue))
	#print("Running")
	#print("Current Tone: " + currentTone)
	
	if(accelYValue < 400):
		highestTone = 'As4'
	elif(accelYValue < 450):
		highestTone = 'Fs5'
	elif(accelYValue < 500):
		highestTone = 'D6'
	elif(accelYValue < 550):
		highestTone = 'As6'
	elif(accelYValue >= 550):
		highestTone = 'Fs7'
	
	#if(accelYValue < 500):
	#	harmTable.SetHarm(100, sndobj.SINE)
	#elif(accelYValue >= 500):
	#	harmTable.SetHarm(50, sndobj.SAW)
	
	if(time.time() > deltaT + stepTime):
		deltaT = time.time()
		if(toneLib.getToneToIndex(currentTone) >= toneLib.getToneToIndex(highestTone) or toneLib.getToneToIndex(currentTone) >= 71):
			scaleDirection = 'down'
		if(toneLib.getToneToIndex(currentTone) <= toneLib.getToneToIndex(lowestTone) or toneLib.getToneToIndex(currentTone) <= 2):
			scaleDirection = 'up'
		if(scaleDirection == 'up'):
			currentTone = toneLib.upSteps(2, currentTone)
		else:
			currentTone = toneLib.downSteps(2, currentTone)
		osc1.SetFreq(toneLib.getToneToFreq(currentTone))
	#newAmp = (accelYValue - 400)
	#if(newAmp < 0): newAmp = 0
	#osc1.SetAmp(newAmp * 20)
	
