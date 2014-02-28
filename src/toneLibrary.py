# This object makes it easier to produce the frequencies required to sound musical notes of 12-equal temperament tuned to 440.
class toneLibrary:
    # The constructor defines the arrays containing the index value of a note, as well as its frequency value
    # The reason a separate index array is needed is because Python dictionaries do not keep track of indices. In order to do simple addition and subtraction of scale
    # values, we need to keep track of the index value of a particular tone. Though it's not ideal, as of right now this library increments steps by converting the note
    # name string value to the index number, incrementing that index number, then converting the index number back to the note name string value. The note name string value
    # can also be converted to its corresponding frequency value.
    def __init__(self):
        self.toneToIndex = dict([('C2',1), ('Cs2',2), ('D2',3), ('Ds2',4), ('E2', 5), ('F2', 6), ('Fs2', 7), ('G2', 8), ('Gs2',9), ('A2',10), ('As2',11), ('B2',12),
                                     ('C3',13), ('Cs3',14), ('D3',15), ('Ds3',16), ('E3', 17), ('F3', 18), ('Fs3', 19), ('G3', 20), ('Gs3',21), ('A3',22), ('As3',23), ('B3',24),
                                     ('C4',25), ('Cs4',26), ('D4',27), ('Ds4',28), ('E4', 29), ('F4', 30), ('Fs4', 31), ('G4', 32), ('Gs4',33), ('A4',34), ('As4',35), ('B4',36),
                                     ('C5',37), ('Cs5',38), ('D5',39), ('Ds5',40), ('E5', 41), ('F5', 42), ('Fs5', 43), ('G5', 44), ('Gs5',45), ('A5',46), ('As5',47), ('B5',48),
                                     ('C6',49), ('Cs6',50), ('D6',51), ('Ds6',52), ('E6', 53), ('F6', 54), ('Fs6', 55), ('G6', 56), ('Gs6',57), ('A6',58), ('As6',59), ('B6',60),
                                     ('C7',61), ('Cs7',62), ('D7',63), ('Ds7',64), ('E7', 65), ('F7', 66), ('Fs7', 67), ('G7', 68), ('Gs7',69), ('A7',70), ('As7',71), ('B7',72)])
        self.indexToTone = dict((v,k) for k,v in self.toneToIndex.items())
        self.toneToFreq = dict([('C2',65.41), ('Cs2',69.30), ('D2',73.42), ('Ds2',77.78), ('E2',82.41), ('F2',87.31), ('Fs2',92.5), ('G2',98), ('Gs2',103.83), ('A2',110), ('As2',116.54), ('B2',123.47),
                           ('C3',130.81), ('Cs3',138.59), ('D3',146.83), ('Ds3',155.56), ('E3',164.81), ('F3',174.61), ('Fs3',185), ('G3',196), ('Gs3',207.65), ('A3',220), ('As3',233.08), ('B3',246.94),
                           ('C4',261.63), ('Cs4',277.18), ('D4',293.66), ('Ds4',311.13), ('E4',329.63), ('F4',349.23), ('Fs4',369.99), ('G4',392), ('Gs4',415.30), ('A4',440), ('As4',466.16), ('B4',493.88),
                           ('C5',523.25), ('Cs5',554.37), ('D5',587.33), ('Ds5',622.25), ('E5',659.25), ('F5',698.46), ('Fs5',739.99), ('G5',783.99), ('Gs5',830.61), ('A5',880), ('As5',932.33), ('B5',987.77),
                           ('C6',1046.5), ('Cs6',1108.73), ('D6',1174.66), ('Ds6',1244.51), ('E6',1318.51), ('F6',1396.91), ('Fs6',1479.98), ('G6',1567.98), ('Gs6',1661.22), ('A6',1760), ('As6',1864.66), ('B6',1975.53),
                           ('C7',2093), ('Cs7',2217.46), ('D7',2349.32), ('Ds7',2489.02), ('E7',2637.02), ('F7',2793.83), ('Fs7',2959.96), ('G7',3135.96), ('Gs7',3322.44), ('A7',3520), ('As7',3729.31), ('B7',3951.07)])
    
    # Takes a note name string value and returns the corresponding index value
    def getToneToIndex(self, tone):
        return self.toneToIndex[tone]
    
    # Takes an index value and returns the corresponding note name string value
    def getIndexToTone(self, index):
        return self.indexToTone[index]
    
    # Raises the startingTone note name string value by numSteps number of half steps, returns the note name string value of the result
    def upSteps(self, numSteps, startingTone):
        index = self.toneToIndex[startingTone]
        index += numSteps
        if index <= 72 and index >= 0:
            return self.indexToTone[index]
        elif index > 72:
            return 'B7'
        elif index < 1:
            return 'C2'
    
    # Lowering the startingTone note name string value by numSteps number of half steps, returns the note name string value of the result
    def downSteps(self, numSteps, startingTone):
        index = self.toneToIndex[startingTone]
        index -= numSteps
        if index <= 72 and index >= 0:
            return self.indexToTone[index]
        elif index > 72:
            return 'B7'
        elif index < 1:
            return 'C2'
    
    # Takes a note name string value and returns the corresponding frequency value
    def getToneToFreq(self, tone):
        return self.toneToFreq[tone]