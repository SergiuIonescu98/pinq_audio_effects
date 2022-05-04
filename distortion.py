import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plot
import simpleaudio as sa


def infiniteClip(t, mysin):

    N = len(mysin)
    distort = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            distort[n] = 1
        else:
            distort[n] = 0

    distort = np.array(distort)
    plot.plot(t, distort)
    plot.title('Distorted Sine wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')
    plot.show()
    
    return distort

def halfwaveRectification(t, mysin):


    N = len(mysin)
    half = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            half[n] = mysin[n]
        else:
            half[n] = 0


    plot.plot(t, half)
    plot.title('Half Sine wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')
    plot.show()
    
    return half



def fullwaveRectification(t, mysin):
    
    N = len(mysin)
    full = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            full[n] = mysin[n]
        else:
            full[n] = -mysin[n]


    plot.plot(t, full)
    plot.title('Full Sine wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')
    plot.show()
    
    return full



# Fs = 44100
# Ts = 1/Fs
# f = 2 # fundamental frequenzy # de cate ori sa apara intr-o secunda
# t = np.arange(0,1, Ts)
# mysin = np.sin(2*np.pi*f*t)


##############################
frequency = 440  # Our played note will be 440 Hz
fs = 44100  # 44100 samples per second
seconds = 3  # Note duration of 3 seconds

# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * fs, False)

# Generate a 440 Hz sine wave
note = np.sin(frequency * t * 2 * np.pi)
note = infiniteClip(t, note)
# Ensure that highest value is in 16-bit range
#audio = note * (2**15 - 1) / np.max(np.abs(note))
# Convert to 16-bit data
#audio = audio.astype(np.int16)
audio = note.astype(np.int16)

# Start playback
play_obj = sa.play_buffer(audio, 1, 2, fs)

# Wait for playback to finish before exiting
play_obj.wait_done()

##############################

# plot.plot(t, mysin)
# plot.title('Original Sine wave')
# plot.xlabel('Time')
# plot.ylabel('Amplitude')
# plot.show()



# distort = infiniteClip(t, mysin)
# half = halfwaveRectification(t, mysin)
# full = fullwaveRectification(t, mysin)