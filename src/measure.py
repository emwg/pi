'''
int beatsInMeasure
int rythmicCount - this is the beats in the measure * 4












'''
class measure:
    def __init__(self, beatsInMeasure):
        self.beatsInMeasure = beatsInMeasure
        self.notesInMeasure = []
        
    def addNote(self, length, pitch, beat, subdivision):
        startPos = ((beat-1) * 4 + 1) + (subdivision - 1)
        newNote = note(length, pitch, startPos)
        self.notesInMeasure.append(newNote)
        
    def addNoteAsNote(self, newNote):
        self.notesInMeasure.append(newNote)
        
    def getNoteAtPosition(self, position):
        if position < 1 or position > (beatsInMeasure + 3):
            return 0
        notesAtPosition = []
        for posNote in self.notesInMeasure:
            if posNote.getStartingPosition() == position:
                notesAtPosition.append(posNote)
        return notesAtPosition