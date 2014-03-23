'''
int noteLength
const int WHOLE_NOTE = 0
const int HALF_NOTE = 1
const int QUARTER_NOTE = 2
const int EIGHTH_NOTE = 3
const int SIXTEENTH_NOTE = 4

bool tied
string pitch

Note is responsible for its own pitch and keeping track of its initial and remaining duration
'''
from toneLibrary import *

class note:
    WHOLE_NOTE = 16
    HALF_NOTE = 8
    QUARTER_NOTE = 4
    EIGHTH_NOTE = 2
    SIXTEENTH_NOTE = 1
    DOTTED_HALF_NOTE = 12
    DOTTED_QUARTER_NOTE = 6
    DOTTED_EIGHTH_NOTE = 3
    
    def __init__(self, noteLength, pitch):
        self.noteLength = noteLength
        self.pitch = pitch
    
    def getPitchAsName(self):
        return self.pitch
    
    def getPitchAsFreq(self):
        return toneLibrary.getToneToFreq(self.pitch)
    
    def getNoteLength(self):
        return self.noteLength
    
    def decrementNoteLength(self):
        self.noteLength -= 1
        
    