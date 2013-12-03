from sensor import *

class lightSensor:
	def __init__(self, channel, sensitivity):
		self.sensor = sensor(channel,"light")
		self.sensitivity = sensitivity

	def __str__(self):
		return sensor.__str__()

	def getLightValue(self):
		self.sensor.update()
		if (self.sensor.getValue() > self.sensitivity): return (self.sensor.getValue() - self.sensitivity)
		return 0
