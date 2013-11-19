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
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0;
pot1 = 1;

last_read = 0
last_read1 = 0        # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

while True:
        # we'll assume that the pot didn't move
        trim_pot_changed = False
	trim_pot_changed1 = False

        # read the analog pin
        trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	trim_pot1 = readadc(pot1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # how much has it changed since the last read?
        pot_adjust = abs(trim_pot - last_read)
	pot_adjust1 = abs(trim_pot1 - last_read1)

        if DEBUG:
                print "trim_pot0:", trim_pot
                print "pot_adjust0:", pot_adjust
                print "last_read0", last_read
		
		print "trim_pot1:", trim_pot1
                print "pot_adjust1:", pot_adjust1
                print "last_read1", last_read1

        if ( pot_adjust > tolerance ):
               trim_pot_changed = True
	if ( pot_adjust1 > tolerance ):
               trim_pot_changed1 = True


        if DEBUG:
                print "trim_pot_changed", trim_pot_changed
		print "trim_pot_changed1", trim_pot_changed1

        if ( trim_pot_changed ):
                
                
                last_read = trim_pot
		last_read1 = trim_pot1

        # hang out and do nothing for a half second
        time.sleep(0.5)