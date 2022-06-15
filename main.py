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


############## distort

## read and process wav
#f_samples, framerate = read_and_process_wav(file_in, infiniteClip, draw=False)
#f_samples, framerate = read_and_process_wav(file_in, fullwaveRectification)
#f_samples, framerate = read_and_process_wav(file_in, cubicDistortion, control= 1, draw=False)


## write to new wav the proccesed signal
#write_raw(file_out, f_samples, normalise = False, effect="cubic")
#write_raw(file_out, f_samples, normalise = False, effect="cubic", typeB='int32')

#write_to_wav(file_out, f_samples, framerate, effect="cubicDistortion", play=False)



############# echo


## delayul trebuie sa fie pe ritm. De aceea avem nevoie de bpm si de noteDiv
#f_samples, framerate = read_and_process_echo(file_in, feedforward_echo, bpm = 102, noteDiv = 0.5, b = 0.45)
#write_to_wav(file_out, f_samples, framerate, effect="feedforwardecho", play=True)
#write_raw(file_out, f_samples, normalise = False, effect="FFecho", typeB='int16')
#write_raw(file_out, f_samples, normalise = False, effect="FBecho", typeB='int16')


# f_samples, Fs = soundfile.read(file_in)  # Mono signal
# r_samples, _ = soundfile.read(reverb_in)  # Stereo IR

# print(f_samples)
# print("REVERB ")
# print(r_samples[:, 0])

# print("## FIRST CONV ##")
# yLeft = np.convolve(f_samples, r_samples[:, 0])

# for i in range(len(yLeft)):
#     if yLeft[i] > 0 :
#         print(yLeft[i])

# # print("## SECOND CONV ##")
# # yRight = np.convolve(f_samples, r_samples[:, 1])

# # for i in range(len(yRight)):
# #     if yRight[i] > 0 :
# #         print(yRight[i])

# # y = [yLeft, yRight]
# # y = np.array(y)

# # print("## BIG Y ##")

# # for i in range(len(y)):
# #     if y[i] > 0 :
# #         print(y[i])

# yLeft = yLeft * 10000 # mai trebuie si gain

# write_raw(file_out, yLeft, effect="reverb_conv")
# print("## WRITING WAV ##")
# write_to_wav(file_out, yLeft, Fs, effect="reverb_conv", play=False)



############# delay buffers

#x = np.append(np.array([1, -1, 2, -2]), np.zeros([6]))
# x = np.append(np.array([1, -1, 2, -2]), np.array([7,7,7,7,7,7]))
# out = linearBuffer(x, 5) 
        ### nu te gandi ca aduce zerourile alea 6.
        ### mai intai incepe ca fiind zero cu primele 5 valori
        ### deci obligatoriu primele 5 valori sunt zero
        #### si se termina outul ca ai zis doar N valori. 
        #### deci e fiiix o siftare la dreapta cu blen pozitii




# x = np.append(np.array([1, 1, 1, 1, 1]), np.array([2,2,2,2,2]))
# out = firdelayBuffer(x, 5, 1)
# print(out) 
# mai intai pornesc valorile de 1 si dupa urmeaza cele de 2 adunate cu cele de 1 ( delayul )
#...imagineazati ca ele ies din dreapta esantioanele.


#### buffer liniar melodie
# f_samples, Fs = soundfile.read(file_in)  # Mono signal
# out_samples = firdelayBuffer(x=f_samples, fs=Fs, bpm=105, noteDiv=0.5, fbGain=0.75)  # cred ca trebui sa dau delay in secunde si sa convertesc in samples
# out_samples = out_samples * 10000 # gain
# print(out_samples)
# write_raw(file_out, out_samples, Fs, effect="firdelayBufffer")
####


### buffer circular
# x = np.append(np.array([1,-1,2,-2,3]), [7,7,7,7,7])
# buffer = np.zeros(4)
# delay = 4

# N = len(x)
# out = np.zeros(N)

# for n in range(N):
#     out[n] = circularBuffer(x[n], buffer, delay, n)

# print("## This is X ##")
# print(x)
# print("## This is out")
# print(out) ## aceeasi siftare cu 4 pozitii la dreapta doar ca mai eficienta

### buffer circular melodie

# x, Fs = soundfile.read(file_in) 
# print(x) ### da clar mi l normalizeaza ca sunt cu 0.0008 valorile
# delay = tempo_to_samples(Fs, 104, 0.5)
# buffer = np.zeros(delay)

# N = len(x)
# out = np.zeros(N)

# for n in range(N):
#     out[n] = circularechoBuffer(x[n], buffer, delay, n, 0.75)

# out = out * 10000 ## gain
# x = x*10000 ## gain ( poate sampleaudio ala il normalizeaza )

# write_raw(filename = file_out, f_samples = out, effect="echoCircular")
# write_raw(filename = file_out, f_samples = x, effect="original")




############# vibrato effect ##########


# x, Fs = soundfile.read(file_in) # Input signal
# Ts = 1/Fs
# N = len(x)

# # Initialize the delay buffer
# maxDelay = 1000  # Samples
# buffer = np.zeros([maxDelay])

# # LFO parameters
# t = np.arange(0, N) * Ts
# rate = 4  # Frequency of LFO in Hz
# depth = 75  # Range of samples of delay

# # Initialize output signal
# out = np.zeros([N])

# # aici e fix ca la circular buffer. Iei pe rand esantion cu esantion
# for n in range(N):
#     out[n], buffer = vibratoEffect(x[n], buffer, Fs, n, depth, rate)
#     if n == 70:
#         out[n], buffer = vibratoEffect(x[n], buffer, Fs, n, depth, rate)


# out = out * 10000
# write_raw(filename = file_out, f_samples = out, effect = "vibrato")

################ fractional delay

# linearInterpolationDelay()

########## chorus effect ####


# x, Fs = soundfile.read(file_in)
# Ts = 1/Fs

# maxDelay = int(np.ceil(0.05*Fs))  # Maximum delay of 50 ms
# buffer = np.zeros(maxDelay)

# rate = 0.6  # Hz (frequency of LFO)
# depth = 5  # Milliseconds (amplitude of LFO)
# predelay = 30  # Milliseconds (offset of LFO)

# wet = 50  # Percent wet (dry = 100 - wet)

# # Initialize output signal
# N = len(x)
# out = np.zeros(N)

# for n in range(N):
#     # Use chorusEffect function
#     out[n], buffer = chorusEffect(x[n], buffer, Fs, n, depth, rate, predelay, wet)

# out = out * 10000
# write_raw(filename = file_out, f_samples = out, effect = "chorus")
