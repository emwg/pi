

import sndobj
from measure import *

class instrument:
    
    
    def __init__(self, numMeasures, beatsInMeasure, options):
        # List to hold the measures, all initialized in the constructor
        self.measures = []
        self.beatsInMeasure = beatsInMeasure
        for i in range(0, numMeasures):
            measures.append(measure(beatsInMeasure))
        
        # List to hold the notes are currently being sounded
        self.currentlyPlaying = []
        self.timeStep = 0
        self.maxTimeStep = (numMeasures * beatsInMeasure * 4) - 1
        self.loop = options.getLoop()
        
        self.harmonicTable = sndobj.HarmTable(options.getHarmTableLength(), options.getNumHarmonics(), options.getWaveType())
        self.oscillators = dict([])
        self.amplitude = options.getAmplitude()
    
    # Add notes to a specified measure, indexed starting at 1
    def addNoteToMeasureAsNote(self, measureNum, beat, subdivision, noteToAdd):
        if measureNum > numMeasures or measureNum < 1:
            raise Exception("Measure does not exist")
        measures[measureNum - 1].addNoteAsNote(noteToAdd, beat, subdivision)
    def addNoteToMeasure(self, measureNum, beat, subdivison, pitch, length):
        noteToAdd = note(length, pitch)
        addNoteToMeasureAsNote(measureNum, beat, subdivision, noteToAdd)
    
    # Called at every time step to process the next time step in the measure
    def processTimeStep(self):
        decrementCurrentlyPlayingNoteLengths()
        cleanOscillators()
        prepareNotes()
        incrementTimeStep()
    
    # Find notes that begin at the current time step and append them to the list currentlyPlaying
    def prepareNotes(self):
        # Calculate the current measure number and position in measure based on current time step
        measureNum = self.timeStep / (self.beatsInMeasure*4)
        measurePos = self.timeStep % (self.beatsInMeasure*4)
        # Get notes based on measure number and position
        notesInMeasure = measures[measureNum].getNotesAtPosition(measurePos)
        for note in notesInMeasure:
            self.currentlyPlaying.append(note)
            addOscillator(note.getPitchAsFreq(), note.getNoteId())
        
    # Search the list currentlyPlaying for the note with the corresponding noteId. If none is found, return None
    def getNoteById(self, noteId):
        for note in self.currentlyPlaying:
            if note.getNoteId() == noteId:
                return note
        return None
            
    # Decrement the note length of all notes currently being sounded
    def decrementCurrentlyPlayingNoteLengths(self):
        for note in self.currentlyPlaying:
            note.decrementNoteLength()
    
    # Increment the current time step
    def incrementTimeStep(self):
        self.timeStep += 1
        if(self.timeStep > self.maxTimeStep and self.loop):
            self.timeStep = 0
        
        
    # Adds an oscillator object to the list of oscillators. This method does not actually sound them, that is the job of the rhythm controller
    def addOscillator(self, pitch, noteId):
        osc = sndobj.Oscili(self.harmonicTable, pitch, self.amplitude)
        self.oscillators[noteId] = osc
      
    # Returns the list of oscillators
    def getOscillators(self):
        return self.oscillators
        
    # Removes from the list oscillators with note values that have expired
    def cleanOscillators(self):
        for noteId in self.oscillators:
            # I can get away from with because if the first conditional clause evaluates to false [getNoteById() returns None because the note doesn't exist] then the
            # second conditional clause is not evaluated. If Python even gets to the second clause, the noteId must be valid
            if getNoteById(noteId) != None and getNoteById(noteId).getNoteLength() == 0:
                del self.oscillators[noteId]
            
        