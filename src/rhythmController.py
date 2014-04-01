'''
int tempo
int beatsInMeasure
int numMeasures

Measure[] measures
'''

class rhythmController:
    rhythmControllerMixer = sndobj.Mixer()
    rhythmControllerPan = sndobj.Pan(0, mixer)
    rhythmControllerOut = sndobj.SndRTIO(2, sndobj.SND_OUTPUT)
    rhythmControllerSoundThread = sndobj.SndThread()
    
    rhythmControllerTempo = 120 #Default tempo
    rhythmControllerTimeStepLength = computeTimeStepLength(rhythmControllerTempo)
    
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
    
    # Computes and returns the time in seconds that a time step will last at a given tempo
    # One time step is always equal to the length on one sixteenth note at the given tempo
    @staticmethod
    def computeTimeStepLength(self, tempo):
        return 1.0 / float((tempo * 4))

