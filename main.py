from utils import *
from effects import *

############## sine test ################

# Fs = 44100
# Ts = 1/Fs
# #f = 2 # fundamental frequenzy # de cate ori sa apara intr-o secunda
# f = 440
# seconds = 3
# t = np.linspace(0, seconds, seconds * Fs, False) # iti creeaza "secunde * Fs " puncte pe care le imparte in secunde spatii
# mysin = np.sin(2*np.pi*f*t)
# plotSignal(t, mysin, "Original Sine Wave")

# #note = infiniteClip(t, mysin, True)
# #note = halfwaveRectification(t, mysin)
# #note = fullwaveRectification(t, mysin)
# note = cubicDistortion(t, mysin, a = 1, draw=True)  # a [0  1]
# playNote_16b(note, Fs)


################ guitar test #################################
#file_in = 'dry_guitar2.wav'
file_in = 'Audio Files/AcGtr.wav'
file_out = 'out'

reverb_in = 'Audio Files/reverbIR.wav'

## read and process wav
#f_samples, framerate = read_and_process_wav(file_in, infiniteClip, draw=False)
#f_samples, framerate = read_and_process_wav(file_in, fullwaveRectification)
#f_samples, framerate = read_and_process_wav(file_in, cubicDistortion, control= 1, draw=False)


## write to new wav the proccesed signal
#write_raw(file_out, f_samples, normalise = False, effect="cubic")
#write_raw(file_out, f_samples, normalise = False, effect="cubic", typeB='int32')

#write_to_wav(file_out, f_samples, framerate, effect="cubicDistortion", play=False)


## delayul trebuie sa fie pe ritm. De aceea avem nevoie de bpm si de noteDiv
#f_samples, framerate = read_and_process_echo(file_in, feedforward_echo, bpm = 102, noteDiv = 0.5, b = 0.45)
#write_to_wav(file_out, f_samples, framerate, effect="feedforwardecho", play=True)
#write_raw(file_out, f_samples, normalise = False, effect="FFecho", typeB='int16')
#write_raw(file_out, f_samples, normalise = False, effect="FBecho", typeB='int16')


f_samples, Fs = soundfile.read(file_in)  # Mono signal
r_samples, _ = soundfile.read(reverb_in)  # Stereo IR

print(f_samples)
print("REVERB ")
print(r_samples[:, 0])

print("## FIRST CONV ##")
yLeft = np.convolve(f_samples, r_samples[:, 0])

for i in range(len(yLeft)):
    if yLeft[i] > 0 :
        print(yLeft[i])

# print("## SECOND CONV ##")
# yRight = np.convolve(f_samples, r_samples[:, 1])

# for i in range(len(yRight)):
#     if yRight[i] > 0 :
#         print(yRight[i])

# y = [yLeft, yRight]
# y = np.array(y)

# print("## BIG Y ##")

# for i in range(len(y)):
#     if y[i] > 0 :
#         print(y[i])

yLeft = yLeft * 10000 # mai trebuie si gain

write_raw(file_out, yLeft, Fs, effect="reverb_conv")




