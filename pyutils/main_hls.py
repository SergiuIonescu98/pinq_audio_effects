from click import option
from utils import *
from effects import *
import sysv_ipc
import time
import sys
import scipy.io.wavfile as wf
import argparse

INF = 0
HALF = 1
FULL = 2

ECHO_FWD = 3
ECHO_FBK = 4

BUFFER_ECHO = 5
REVERB = 6

### parser
parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')

parser.add_argument("effect", default="infinitClip", nargs="?", type=str,
                    help="Effect to be proccesed")
parser.add_argument("--file",
                    help=f"File dimension")

options = parser.parse_args()
print("#### Selected effect #### " ,options.effect)
print("#### Selected file dim #### " ,options.file)

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

file_in = ''
if options.file == "short":
        file_in = 'Audio Files/AcGtr_short.wav'
elif options.file == "long":
        file_in = 'Audio Files/AcGtr.wav'
print("#### Selected file dim #### " ,file_in)

file_out = 'out'
#reverb_in = 'Audio Files/reverbIR.wav'
reverb_in = 'Audio Files/reverbIR_short.wav'

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
# f_samples, framerate = read_and_process_echo(file_in, feedforward_echo, bpm = 102, noteDiv = 0.5, b = 0.45)
# #write_to_wav(file_out, f_samples, framerate, effect="feedforwardecho", play=False)
# write_raw(file_out, f_samples, normalise = False, effect="FFecho", typeB='int16')
# print(f_samples)
#write_raw(file_out, f_samples, normalise = False, effect="FBecho", typeB='int16')


# f_samples, Fs = soundfile.read(file_in)  # Mono signal
# r_samples, _ = soundfile.read(reverb_in)  # Stereo IR

# data0 = r_samples[:, 0]
# print("REVERB ", len(data0))
# np.savetxt("reverb_short.txt", data0, fmt='%1.18f')

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

# x = np.append(np.array([1, -1, 2, -2]), np.zeros([6]))
# x = np.append(np.array([1, -1, 2, -2]), np.array([7,7,7,7,7,7]))
# out = linearBuffer(x, 5) 
        ## nu te gandi ca aduce zerourile alea 6.
        ## mai intai incepe ca fiind zero cu primele 5 valori
        ## deci obligatoriu primele 5 valori sunt zero
        ### si se termina outul ca ai zis doar N valori. 
        ### deci e fiiix o siftare la dreapta cu blen pozitii




# x = np.append(np.array([1, 1, 1, 1, 1]), np.array([2,2,2,2,2]))
# out = firdelayBuffer(x, 5, 1)
# print(out) 
# mai intai pornesc valorile de 1 si dupa urmeaza cele de 2 adunate cu cele de 1 ( delayul )
#...imagineazati ca ele ies din dreapta esantioanele.


#### buffer liniar melodie
# f_samples, Fs = soundfile.read(file_in)  # Mono signal
# out_samples = firdelayBuffer(x=f_samples, fs=Fs, bpm=105, noteDiv=0.5, fbGain=0.75)  # cred ca trebui sa dau delay in secunde si sa convertesc in samples
# out_samples = out_samples * 10000 # gain
# #print(out_samples)
# write_raw(file_out, out_samples, Fs, effect="firdelayBufffer")
# write_to_wav(file_out, out_samples, Fs, effect="firdelayBuffer")
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
# write_to_wav(filename= file_out, f_samples = out, framerate=Fs, effect="echoCircular" )




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
# write_to_wav(filename = file_out, f_samples=out, framerate=Fs, effect = "vibrato")

################ fractional delay

#linearInterpolationDelay()

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
# write_to_wav(filename = file_out, f_samples=out, framerate=Fs, effect = "chorus")




####### inter process comunication #########

# read samples
f = wave.open(file_in)
my_fs = f.getframerate()
my_music = read_samples(f)
my_music = list(my_music)
my_music[0] = 0 ## flag

conv_size = 136199
# convert samples to 2 bytes list
melody_size = sys.getsizeof(my_music)

print("# SAMPLE RATE OF MELODY IS " + str(my_fs) + " " + str(len(my_music)))
print("# SIZE OF MELODY is " + str(melody_size) + " bytes")
bstring = b''
for i in range(len(my_music)):
        my_music[i] = my_music[i].to_bytes(2, 'little', signed=True)
        bstring = bstring + my_music[i]
print("# SIZE OF BYTESTRING is " + str(sys.getsizeof(bstring)) + " bytes")

#print(bstring)

try:
        memory = sysv_ipc.SharedMemory(sysv_ipc.IPC_PRIVATE, sysv_ipc.IPC_CREX, 0o666, 2**20)
        first_byte = memory.read()[0] # converts the first byte to a 8 bit integer. And interprets as a string literal
                                      # prima oara este spatiu. Care in ascii e 32
        print("SHM key is: ", memory.id, ": First byte is: ", first_byte)

        ## write data to memory
        #print("Data to be writen to memory ", bstring)
        memory.write(bstring)
        #print("\nInitial bytes in memory ",memory.read(8)) # reads the first 8 bytes.
        
        print("## INITIAL FLAG ", memory.read(1)[0])
        ## wait for the C program to end
        while memory.read(1)[0] == 0:
                time.sleep(0.0001)
        print("# THE CONTENTS OF THE FIRST BYTE HAVE CHANGED ")
        
        ## read procces data
        if options.effect == "reverb":
                all_bytes = memory.read(conv_size)
        else:
                all_bytes = memory.read(melody_size)
        #print("Data after IPC ", all_bytes) # reads the 8 bytes.
        print("")

        ## convert 2 bytes back to samples
        proccesed_music = []
        i = 0

        if options.effect == "reverb":
                signal_len = conv_size-1
        else:
                signal_len = len(bstring)

        while i < signal_len: 
                byte1 = all_bytes[i].to_bytes(1, 'big')
                byte2 = all_bytes[i+1].to_bytes(1, 'big') # converteste in int cand acceszi cu []
                proccesed_music.append(int.from_bytes(byte1 + byte2, byteorder='little', signed=True))
                i+=2

        memory.remove()

except sysv_ipc.ExistentialError:
        print("Memory segment already exists!")

## write to wav proccesed music
#print("## AFTER PROCCESD MUSIC ##")
#print(proccesed_music)
proccesed_music= np.array(proccesed_music)
#write_raw(file_out, proccesed_music, normalise=False, effect="reverb", typeB='int16')
write_to_wav(file_out, proccesed_music, my_fs, effect=options.effect, play=False)