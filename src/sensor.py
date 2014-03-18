#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0

        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
		
                if (GPIO.input(misopin)):
                        adcout |= 0x1
			


        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO0 = 23
SPIMISO1 = 22
SPIMOSI = 24
SPICS = 25

class sensor:
	
	def __init__(self, adc, channel, type):
		self.channel = channel
		self.type = type
		self.changed = False
		self.value = 0.0
		self.tolerance = .005
		self.lastread = 0
		self.maxValue = 1024
        print ("adc = " + str(adc))
        self.adc = adc
        
        # set up the SPI interface pins
        GPIO.setup(SPIMOSI, GPIO.OUT)
        if (adc == 0):
            GPIO.setup(SPIMISO0, GPIO.IN)
        elif (adc == 1):
            GPIO.setup(SPIMISO1)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)

	def __str__(self):
		return ("Channel: " + self.channel + " Value: " + self.value)

	def hasChanged(self):
		return self.changed

	def getValue(self):
		return self.value

	def getTolerance(self):
		return self.tolerance

	def setTolerance(self, newTolerance):
		self.tolerance = newTolerance

	def update(self):
		potadjust = 0
		currentvalue = readadc(self.channel, SPICLK, SPIMOSI, SPIMISO, SPICS)
		potadjust = abs(currentvalue - self.lastread)
		if (potadjust > self.tolerance):
			self.changed = True
			self.value = currentvalue
			self.lastread = currentvalue

	
