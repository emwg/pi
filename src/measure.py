'''
int beatsInMeasure
int rythmicCount - this is the beats in the measure * 4












'''

from note import *

class measure:
    def __init__(self, beatsInMeasure):
        self.beatsInMeasure = beatsInMeasure
        self.notesInMeasure = dict([])
        for i in range(1,beatsInMeasure*4+1):
            self.notesInMeasure[i] = []
    
    # Adds a note to the measure
    # <code>length</code> is a value 1 through 16 that specifies the location of the note in the measure, broken down to sixteenth notes
    # <code>pitch</code> is a string value of the pitch, as required by the <code>toneLibrary</code>
    # <code>beat</code> is the beat the note falls on, <code>subdivision</code> is the subdivision within that beat, broken down to sixteenth notes
    def addNote(self, length, pitch, beat, subdivision):
        try:
            newNote = note(length, pitch)
            self.addNoteAsNote(newNote, beat, subdivision)
        except Exception:
            raise Exception("New note could not be created")
        
    def addNoteAsNote(self, newNote, beat, subdivision):
        if beat > self.beatsInMeasure or beat < 1:
            raise ValueError("Given beat does not exist in the measure")
        if subdivision > 4 or subdivision < 1:
            raise ValueError("Given subdivision does not exist in the beat")
        if length < 1:
            raise ValueError("Note cannot have must have nonzero positive length")
        startPos = ((beat-1) * 4 + 1) + (subdivision - 1)
        self.notesInMeasure[startPos].append(newNote)
        
    def getNotesAtPosition(self, position):
        if position < 1 or position > (beatsInMeasure * 4):
            raise ValueError("Given beat or subdivision does not exist in the measure")
        return self.notesInMeasure[position]
        '''notesAtPosition = []
        for posNote in self.notesInMeasure:
            if posNote.getStartingPosition() == position:
                notesAtPosition.append(posNote)
        return notesAtPosition'''