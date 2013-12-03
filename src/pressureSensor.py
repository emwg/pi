#!/usr/bin/env python
from sensor import *

class pressureSensor:
	
	def __init__(self, channel, sensitivity):
		self.sensor = sensor(channel,"pressure")
		self.sensitivity = sensitivity

	def __str__(self):
		return sensor.__str__()

	def getPressureValue(self):
		self.sensor.update()
		if (self.sensor.getValue() > self.sensitivity)
			return (self.sensor.get(Value() - sensitivity)
		return 0
	
	
