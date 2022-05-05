from utils import *
from effects import *

Fs = 44100
Ts = 1/Fs
#f = 2 # fundamental frequenzy # de cate ori sa apara intr-o secunda
f = 440
seconds = 3
t = np.linspace(0, seconds, seconds * Fs, False) # iti creeaza "secunde * Fs " puncte pe care le imparte in secunde spatii
mysin = np.sin(2*np.pi*f*t)
plotSignal(t, mysin, "Original Sine Wave")

note = infiniteClip(t, mysin, True)
#note = halfwaveRectification(t, mysin)
#note = fullwaveRectification(t, mysin)
playNote_16b(note, Fs)