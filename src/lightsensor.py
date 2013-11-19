import sensor

class lightSensor:
	
	def __init__(self, channel, sensitivity):
		self.sensor = sensor(self.channel,"light")
		self.sensitivity = sensitivity

	def __str__(self):

	def getLightValue(self)
		self.sensor.update()
		return (self.sensor.get(Value() - sensitivity)