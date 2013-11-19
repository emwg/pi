#!/usr/bin/env python
import sensor

class pressureSensor:
	
	def __init__(self, channel, sensitivity):
		self.sensor = sensor(self.channel,"pressure")
		self.sensitivity = sensitivity

	def __str__(self):

	def getPressureValue(self):
		self.sensor.update()
		if (self.sensor.getValue() > sensitivity)
			return (self.sensor.get(Value() - sensitivity)
		return 0
	
	