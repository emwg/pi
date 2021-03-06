'''
int tempo
int beatsInMeasure
int numMeasures

Measure[] measures
'''
import sndobj
import time
from instrument import *
from instrumentOptions import *

class rhythmController:
    rhythmControllerMixer = sndobj.Mixer()
    rhythmControllerPan = sndobj.Pan(0, rhythmControllerMixer)
    rhythmControllerOut = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
    rhythmControllerSoundThread = sndobj.SndThread()
    
    rhythmControllerTempo = 120 #Default tempo
    rhythmControllerNewTempoFlag = False
    rhythmControllerTimeStepLength = 1.0 / float((120 * 4))
    
    # Set up and program instrument 1
    instr1Options = instrumentOptions(1024, 10, sndobj.SINE, 800, True)
    instr1 = instrument(2, 4, instr1Options)
    # Measure 1
    instr1.addNoteToMeasure(1, 1, 1, 'G5', 4)
    instr1.addNoteToMeasure(1, 2, 1, 'A5', 4)
    instr1.addNoteToMeasure(1, 3, 1, 'B5', 4)
    instr1.addNoteToMeasure(1, 4, 1, 'C5', 4)
    # Measure 2
    instr1.addNoteToMeasure(2, 1, 1, 'D5', 4)
    instr1.addNoteToMeasure(2, 2, 1, 'E5', 4)
    instr1.addNoteToMeasure(2, 3, 1, 'F5', 4)
    instr1.addNoteToMeasure(2, 4, 1, 'Fs5', 4)
    
    
    
    rhythmControllerOut.SetOutput(1, rhythmControllerPan.left)
    rhythmControllerOut.SetOutput(2, rhythmControllerPan.right)
    rhythmControllerSoundThread.AddObj(rhythmControllerMixer)
    rhythmControllerSoundThread.AddObj(rhythmControllerPan)
    rhythmControllerSoundThread.AddObj(rhythmControllerOut, sndobj.SNDIO_OUT)
    rhythmControllerSoundThread.ProcOn()
    
    
    # Sets the tempo for the rhythm controller
    @staticmethod
    def setTempo(newTempo):
        rhythmController.rhythmControllerTempo = newTempo
        rhythmController.rhythmControllerNewTempoFlag = True
    
    # Computes and returns the time in seconds that a time step will last at a given tempo
    # One time step is always equal to the length on one sixteenth note at the given tempo
    @staticmethod
    def computeTimeStepLength(tempo):
        return 1.0 / float((tempo * 4))
    
    @staticmethod
    def startRhythmController():
        timeInSeconds = time.time()
        while True:
            print("Running")
            if(timeInSeconds - time.time() < -rhythmController.rhythmControllerTimeStepLength):
                rhythmController.instr1.processTimeStep()
                instr1Oscillators = rhythmController.instr1.getOscillators() 
                for instr1OscId in instr1Oscillators:
                    print("DEBUG about to add object:")
                    print(instr1OscId)
                    rhythmController.rhythmControllerSoundThread.AddObj(instr1Oscillators[instr1OscId])
                timeInSeconds = time.time()

rhythmController.startRhythmController()
