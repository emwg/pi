from sensor import *

class accelSensor:
	def __init__(self, adc, channel, sensitivity):
		self.sensor = sensor(adc, channel, "accel")
		self.sensitivity = sensitivity
	def __str__(self):
		return sensor.__str__()
	def getAccelValue(self):
		self.sensor.update()
		value = self.sensor.maxValue - self.sensor.getValue()
		if(value > self.sensitivity): return (value - self.sensitivity)
		return 0
