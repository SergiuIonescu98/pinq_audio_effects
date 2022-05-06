from utils import *
from effects import *

############## sine test ################

# Fs = 44100
# Ts = 1/Fs
# #f = 2 # fundamental frequenzy # de cate ori sa apara intr-o secunda
# f = 440
# seconds = 200
# t = np.linspace(0, seconds, seconds * Fs, False) # iti creeaza "secunde * Fs " puncte pe care le imparte in secunde spatii
# mysin = np.sin(2*np.pi*f*t)
# # plotSignal(t, mysin, "Original Sine Wave")

# note = infiniteClip(t, mysin, True)
# #note = halfwaveRectification(t, mysin)
# #note = fullwaveRectification(t, mysin)
# # playNote_16b(note, Fs)


################ guitar test #################################
file_in = '/home/ionesc_s/Projects/fpga_music/dry_guitar2.wav'
file_out = 'out.wav'

## read and process wav
f_samples, framerate = read_and_process_wav(file_in, halfwaveRectification, draw=True)
# f_samples, framerate = read_and_process_wav(filename, fullwaveRectification)

## write to new wav the proccesed signal
write_to_wav(file_out, f_samples, framerate, effect="halfwaveRectification", play=True)




