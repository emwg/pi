#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
from sensor import *

### creates a sensor object out of the first channel and displays the
### value on the screen as you turn the knob







mySensor = sensor(0,'knob')

while True:
	mySensor.update()
	### system volume requires an int 0..100
	set_volume = mySensor.getValue()/10.24
	set_volume = round(set_volume)
	set_volume = int(set_volume)
	
	###Operating system magic
	set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
	os.system(set_vol_cmd)
	
