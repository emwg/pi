

class instrumentOptions:
    def __init__(self, harmTableLength, numHarmonics, waveType, amplitude):
        self.harmTableLength = harmTableLength
        self.numHarmonics = numHarmonics
        self.waveType = waveType
        self.amplitude = amplitude
        
    def setHarmTableLength(self, harmTableLength):
        self.harmTableLength = harmTableLength
        
    def setNumHarmonics(self, numHarmonics):
        self.numHarmonics = numHarmonics
        
    def setWaveType(self, waveType):
        self.waveType = waveType
        
    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
        
    def getHarmTableLength(self):
        return self.harmTableLength
    
    def getNumHarmonics(self):
        return self.numHarmonics
    
    def getWaveType(self):
        return self.waveType
    
    def getAmplitude(self):
        return self.amplitude