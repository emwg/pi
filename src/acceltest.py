import sndobj
import time
import psutil
from accelsensor import *
from toneLibrary import *

# Create the accelerometer sensor objects

# Create toneLibrary object
# Define tone library parameters


# Create the harmonic table and attach to oscilators
# The higher the first parameter in harmTable.SetHarm is, the buzzier the sound
#coeffs = [4.0, 2.0];'''
'''harmTable = sndobj.HarmTable()
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

deltaT = time.time()
scaleDirection = 'up'
silencerCount = 0'''

class accel:

	def __init__(self):
		self.accelX = accelSensor(2, 0, 10)
		self.accelY = accelSensor(2, 1, 10)
		self.accelZ = accelSensor(2, 2, 10)
		self.toneLib = toneLibrary()
		self.currentTone = 'C2'
		self.lowestTone = 'C2'
		self.highestTone = 'C3'
		self.stepTime = 0.3
		self.deltaT = time.time()
		self.scaleDirection = 'up'
		self.silencerCount = 0
	
	#while True:
	def runAccel(self, osc):
		# Get the accelerometer values, ranging from ~(400-600), print out
		self.accelXValue = self.accelX.getAccelValue()
		self.accelYValue = self.accelY.getAccelValue()
		self.accelZValue = self.accelZ.getAccelValue()
		
		print("AccelX: " + str(self.accelXValue) + " AccelY: " + str(self.accelYValue))
		
		# Set highest tone based on AccelY value
		if(self.accelYValue < 550):
			if(self.toneLib.getToneToIndex('As3') > self.toneLib.getToneToIndex(self.currentTone)):
				self.highestTone = 'As3'
		elif(self.accelYValue < 580):
			if(self.toneLib.getToneToIndex('Fs4') > self.toneLib.getToneToIndex(self.currentTone)):
				self.highestTone = 'Fs4'
		elif(self.accelYValue < 610):
			if(self.toneLib.getToneToIndex('D5') > self.toneLib.getToneToIndex(self.currentTone)):
				self.highestTone = 'D5'
		elif(self.accelYValue < 640):
			if(self.toneLib.getToneToIndex('E6') > self.toneLib.getToneToIndex(self.currentTone)):
				highestTone = 'E6'
		elif(self.accelYValue >= 670):
			if(self.toneLib.getToneToIndex('B7') > self.toneLib.getToneToIndex(self.currentTone)):
				self.highestTone = 'B7'
			
		# Set tempo based on AccelX value
		newStepTime = self.accelXValue - 450
		stepTimeCandidate = 0.3
		if(newStepTime < 0):
			newStepTime = 0
		else:
			# Will convert value 450-560 to 0.3-0.05
			stepTimeCandidate = 0.3 - (0.005 * newStepTime)
			if(stepTimeCandidate < 0.05):
				stepTimeCandidate = 0.05
		if(stepTimeCandidate <= self.stepTime):
			self.stepTime = stepTimeCandidate
		else:
			if(self.stepTime < 0.3):
				self.stepTime += 0.0003
		
		# Increment silencer if needed
		if(self.stepTime >= 0.3):
			if(self.silencerCount < 1200):
				self.silencerCount += 1
		else:
			self.silencerCount = 0
		
		# Calculate next tone at the next time step
		if(self.stepTime > 0 and time.time() > self.deltaT + self.stepTime):
			self.deltaT = time.time()
			if(self.silencerCount < 1200):
				if(self.toneLib.getToneToIndex(self.currentTone) >= self.toneLib.getToneToIndex(self.highestTone) or self.toneLib.getToneToIndex(self.currentTone) >= 71):
					self.scaleDirection = 'down'
					self.highestTone = self.toneLib.downSteps(4, self.highestTone)
				if(self.toneLib.getToneToIndex(self.currentTone) <= self.toneLib.getToneToIndex(self.lowestTone) or self.toneLib.getToneToIndex(self.currentTone) <= 2):
					self.scaleDirection = 'up'
				if(self.scaleDirection == 'up'):
					self.currentTone = self.toneLib.upSteps(2, self.currentTone)
				else:
					self.currentTone = self.toneLib.downSteps(2, self.currentTone)
				osc.SetFreq(self.toneLib.getToneToFreq(self.currentTone))
			else:
				osc.SetFreq(0)
