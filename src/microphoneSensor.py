from sensor import *

class microphoneSensor:
    def __init__(self, adc, channel, sensitivity):
        self.sensor = sensor(adc, channel, "microphone")
        self.sensitivity = sensitivity
    def __str__(self):
        return sensor.__str__()
    def getMicrophoneValue(self):
        self.sensor.update()
        value = self.sensor.maxValue - self.sensor.getValue()
        if(value > self.sensitivity): return (value - self.sensitivity)
        return 0