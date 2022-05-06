from utils import *
from effects import *

import pyaudio
import wave

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
# playNote_16b(note, Fs)


################ guitar test ################
filename = '/home/ionesc_s/Projects/fpga_music/dry_guitar2.wav'

chunk = 1024

f = wave.open(filename)
p = pyaudio.PyAudio()
# stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
#                 channels = f.getnchannels(),  
#                 rate = f.getframerate(),  
#                 output = True)


# data = f.readframes(chunk)   # cate esantioane citeste el deodata cred
#                              # si se comporta ca un fisier. Se goleste in timp
# #play stream  
# while data:  
#     stream.write(data)  
#     data = f.readframes(chunk) 

# #stop stream  
# stream.stop_stream()  
# stream.close()  

# #close PyAudio  
# p.terminate() 

###################################################

f_samples = read_samples(f)
print(type(f_samples))
print(type(f_samples[0]))
print(type(f_samples[1]))
f_samples= np.array(f_samples)
f_samples = fullwaveRectification(len(f_samples), f_samples)
print(f_samples)

#print(f_samples)

obj = wave.open('out.wav', 'w')
obj.setnchannels(2)
obj.setsampwidth(2)
obj.setframerate(f.getframerate())

obj = write_samples(obj, f_samples, 2)

# for i in range(len(f_samples)):
#     value = f_samples[i]
#     data = struct.pack('<h', value)
#     obj.writeframesraw(data)

obj.close()
#########################
print("### STARTING TO READ WRITTEN DATA ####")

# obj = wave.open('out.wav')
# stream = p.open(format = p.get_format_from_width(obj.getsampwidth()),  
#                 channels = obj.getnchannels(),  
#                 rate = obj.getframerate(),  
#                 output = True) 

#                 #read data  
# #######
# print(obj.getsampwidth()) # the number of bytes per sample
# print(obj.getnchannels()) # numarul de canale
# print(obj.getframerate()) # asta e FS
# print(obj.getnframes())
# #######

# data = obj.readframes(chunk)
# while data:
#     stream.write(data)
#     data = f.readframes(chunk)

# #stop stream  
# stream.stop_stream()  
# stream.close()  

# #close PyAudio  
# p.terminate()


filename = 'out.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing
