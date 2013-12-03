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
		value = self.sensor.maxValue - self.sensor.getValue()
		if (value > self.sensitivity): return (value - self.sensitivity)
		return 0
	
	
