import sndobj
import time
import psutil
from accelsensor import *
from toneLibrary import *

def avgList(list):
	listSum = 0
	for item in list:
		listSum += item
	return listSum/len(list)

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
stepTime = 0.3

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
avgAccelXValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
avgAccelYValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
avgAccelZValue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
avgAccelXIndex = 0
avgAccelYIndex = 0
avgAccelZIndex = 0

while True:
	# Get the accelerometer values, ranging from ~(400-600), print out
	accelXValue = accelX.getAccelValue()
	accelYValue = accelY.getAccelValue()
	accelZValue = accelZ.getAccelValue()
	
	avgAccelXValue[avgAccelXIndex] = accelXValue
	avgAccelYValue[avgAccelYIndex] = accelYValue
	if(avgAccelXIndex == 19):
		avgAccelXIndex = 0
	else:
		avgAccelXIndex += 1
	if(avgAccelYIndex == 19):
		avgAccelYIndex = 0
	else:
		avgAccelYIndex += 1
	#mod.SetFreq(2 + (float(accelXValue)/100.0))
	#osc1.SetFreq(accelYValue, mod)
	print("AccelX: " + str(accelXValue))
	print("AccelY: " + str(accelYValue))
	print("AccelZ: " + str(accelZValue))
	#print("Running")
	print("Current Tone: " + currentTone)
	
	if(accelYValue < 550):
		if(toneLibrary.getToneToIndex('As3') > toneLibrary.getToneToIndex(currentTone)):
			highestTone = 'As3'
	elif(accelYValue < 580):
		if(toneLibrary.getToneToIndex('Fs4') > toneLibrary.getToneToIndex(currentTone)):
			highestTone = 'Fs4'
	elif(accelYValue < 610):
		if(toneLibrary.getToneToIndex('D5') > toneLibrary.getToneToIndex(currentTone)):
			highestTone = 'D5'
	elif(accelYValue < 640):
		if(toneLibrary.getToneToIndex('E6') > toneLibrary.getToneToIndex(currentTone)):
			highestTone = 'E6'
	elif(accelYValue >= 670):
		if(toneLibrary.getToneToIndex('B7') > toneLibrary.getToneToIndex(currentTone)):
			highestTone = 'B7'
		
	newStepTime = accelXValue - 450
	stepTimeCandidate = 0.3
	if(newStepTime < 0):
		newStepTime = 0
	else:
		# Will convert value 450-560 to 0.3-0.05
		stepTimeCandidate = 0.3 - (0.005 * newStepTime)
		if(stepTimeCandidate < 0.05):
			stepTimeCandidate = 0.05
	
	if(stepTimeCandidate <= stepTime):
		stepTime = stepTimeCandidate
	else:
		if(stepTime < 0.3):
			stepTime += 0.0003
	
	print(stepTime)
	#if(accelYValue < 500):
	#	harmTable.SetHarm(100, sndobj.SINE)
	#elif(accelYValue >= 500):
	#	harmTable.SetHarm(50, sndobj.SAW)
	
	
	if(stepTime > 0 and time.time() > deltaT + stepTime):
		deltaT = time.time()
		if(avgList(avgAccelXValue) > 450 and avgList(avgAccelYValue) > 550):
			if(toneLib.getToneToIndex(currentTone) >= toneLib.getToneToIndex(highestTone) or toneLib.getToneToIndex(currentTone) >= 71):
				scaleDirection = 'down'
				highestTone = toneLib.downSteps(4, highestTone)
			if(toneLib.getToneToIndex(currentTone) <= toneLib.getToneToIndex(lowestTone) or toneLib.getToneToIndex(currentTone) <= 2):
				scaleDirection = 'up'
			if(scaleDirection == 'up'):
				currentTone = toneLib.upSteps(2, currentTone)
			else:
				currentTone = toneLib.downSteps(2, currentTone)
			osc1.SetFreq(toneLib.getToneToFreq(currentTone))
		else:
			osc1.SetFreq(0)
	#newAmp = (accelYValue - 400)
	#if(newAmp < 0): newAmp = 0
	#osc1.SetAmp(newAmp * 20)
	
