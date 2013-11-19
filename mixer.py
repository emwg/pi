import sndobj
import time

tab = sndobj.HarmTable()
osc1 = sndobj.Oscili(tab, 1, 10000)
osc2 = sndobj.Oscili(tab, 1, 10000)
mod = sndobj.Oscili(tab, 44, 200)
out1 = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
out2 = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
#out3 = sndobj.SndRTIO(1, sndobj.SND_OUTPUT)
delay = sndobj.DelayLine(1, osc2)
mixer = sndobj.Mixer()


mod.SetFreq(1)
osc1.SetFreq(440, mod)
osc2.SetFreq(540, mod)
mixer.AddObj(osc1)
#mixer.AddObj(osc2)
#mixer.AddObj(delay)
out1.SetOutput(1, mixer)
#out2.SetOutput(1, osc2)
#out3.SetOutput(1, delay)

thread = sndobj.SndThread()
thread.AddObj(mod)
thread.AddObj(osc1)
thread.AddObj(osc2)
thread.AddObj(delay)
thread.AddObj(mixer)
thread.AddObj(out1, sndobj.SNDIO_OUT)
thread.AddObj(out2, sndobj.SNDIO_OUT)
#thread.AddObj(out3, sndobj.SNDIO_OUT)

thread.ProcOn()
for i in range(30):
    mod.SetFreq(i)
    time.sleep(0.1)
for i in range(30, 1, -1):
    mod.SetFreq(i)
    time.sleep(0.1)
thread.ProcOff()
