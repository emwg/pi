

import sndobj
from measure import *

class instrument:
    def __init__(self, numMeasures, beatsInMeasure, options):
        # List to hold the measures, all initialized in the constructor
        self.measures = []
        self.beatsInMeasure = beatsInMeasure
        for i in range(0,numMeasures):
            measures.append(measure(beatsInMeasure))
        
        # List to hold the notes are currently being sounded
        self.preparedNotes = []
        self.currentlyPlaying = []
        self.timeStep = 0
        
        self.harmonicTable = sndobj.HarmTable(options.getHarmTableLength(), options.getNumHarmonics(), options.getWaveType())
        # TODO still need to set up the harm table and oscillators and mixer thread and all that
        self.oscillators = []
        self.amplitude = options.getAmplitude()
    
    # Find notes that begin at the current time step and append them to the list preparedNotes
    def prepareNotes(self):
        # Calculate the current measure number and position in measure based on current time step
        measureNum = self.timeStep / (self.beatsInMeasure*4)
        measurePos = self.timeStep % (self.beatsInMeasure*4)
        # Get notes based on measure number and position
        notesInMeasure = measures[measureNum].getNotesAtPosition(measurePos)
        for note in notesInMeasure:
            self.preparedNotes.append(note)
    
    # Notes in the preparedNotes list do not yet have an oscillator and all that attached, so they need to be assigned one, then moved to the currenlyPlaying list
    # Notes in the currenlyPlaying list need to be checked to make sure they still have a nonzero duration
    # All notes need to be decremented
    def play(self):
        
        decrementCurrentlyPlayingNoteLengths()
        incrementTimeStep()
        
            
    # Decrement the note length of all notes currently being sounded
    def decrementCurrentlyPlayingNoteLengths(self):
        for note in self.currentlyPlaying:
            note.decrementNoteLength()
    
    # Increment the current time step
    def incrementTimeStep(self):
        self.timeStep += 1
        
    def addOscillator(self, pitch):
        osc = sndobj.Oscili(self.harmonicTable, pitch, self.amplitude)
        self.oscillators.append(osc)
        
    def cleanOscilators:
        