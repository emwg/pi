from sensor import *

class lightSensor:
	def __init__(channel, sensitivity):
		#self.sensor = sensor(channel,"light")
		#self.sensitivity = sensitivity
		print("Light sensor initialized")

	def __str__(self):
		return sensor.__str__()

	def getLightValue(self):
		self.sensor.update()
		value = self.sensor.maxValue - self.sensor.getValue()
		if (value > self.sensitivity): return (value - self.sensitivity)
		return 0
