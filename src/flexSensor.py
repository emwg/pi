import sensor

class flexSensor:
	
	def __init__(self, channel, pluck):
		self.sensor = sensor(self.channel,"flex")
		self.pluck = pluck
		self.lastValue = 0
		self.temp = 0

	def __str__(self):

	def getFlexValue(self):
		self.sensor.update()
		return self.sensor.getValue()

	def pluckVelocity(self):
		self.update()
		self.temp =self.lastValue
		self.lastValue = self.sensor.getValue()
		return abs(self.lastValue - temp)

		