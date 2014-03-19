from sensor import *

class flexSensor:
	
	def __init__(self, adc, channel, pluck):
		self.sensor = sensor(adc, channel, "flex")
		self.pluck = pluck
		self.lastValue = 0
		self.temp = 0

	def __str__(self):
		return sensor.__str__()

	def getFlexValue(self):
		self.sensor.update()
		return self.sensor.getValue()

	def pluckVelocity(self):
		self.sensor.update()
		self.temp = self.lastValue
		self.lastValue = self.sensor.getValue()
		return abs(self.lastValue - self.temp)

		
