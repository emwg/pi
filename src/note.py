'''
int noteLength
const int WHOLE_NOTE = 0
const int HALF_NOTE = 1
const int QUARTER_NOTE = 2
const int EIGHTH_NOTE = 3
const int SIXTEENTH_NOTE = 4

bool tied
string pitch
'''
from toneLibrary import *

class note:
    self.WHOLE_NOTE = 16
    self.HALF_NOTE = 8
    self.QUARTER_NOTE = 4
    self.EIGHTH_NOTE = 2
    self.SIXTEENTH_NOTE = 1
    self.DOTTED_HALF_NOTE = 12
    self.DOTTED_QUARTER_NOTE = 6
    self.DOTTED_EIGHTH_NOTE = 3
    
    def __init__(self, noteLength, pitch, start):
        self.noteType = noteLength
        self.pitch = pitch
        self.start = start
    
    def getStartingPosition(self):
        return self.start
    
    def getPitchAsName(self):
        return self.pitch
    
    def getPitchAsFreq(self):
        
        
    