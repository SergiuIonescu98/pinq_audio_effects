import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plot
import simpleaudio as sa
import struct
import wave

#### independent de secunde
def playNote_16b(note, Fs):

    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note)) # a normalizat relativ la nota maxima ( nota maxima va fi 1 acum)
                                                    # dupa a inmultit cu 2^15 - 1 ( astfel nota maxima va fi 16 biti maxim)
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, Fs) # audio_data, num channels, bytes_per_sample ( lungimea unui esantion am zis ca e 16 biti), FS
    # Wait for playback to finish before exiting
    play_obj.wait_done()


def plotSignal(t, signal, title="Proccesed Signal"):
    
    plot.plot(t, signal)
    plot.title(title)
    plot.xlabel('Time')
    plot.ylabel('Amplitude')
    plot.show()



#############################################


def _struct_format(sample_width, nb_samples):
    #return {1:"%db", 2:"<%dh", 4:"<%dl"}[sample_width] % nb_samples
    return {1:"%db", 2:"<%dh", 4:"<%dl"}[sample_width] % nb_samples

def read_samples(wave_file):
    frame_data = wave_file.readframes(wave_file.getnframes())
    if frame_data:
        sample_width = wave_file.getsampwidth()
        nb_samples = len(frame_data) // sample_width
        format = {1:"%db", 2:"<%dh", 4:"<%dl"}[sample_width] % nb_samples
        return struct.unpack(format, frame_data)
    else:
        return ()

def write_samples(wave_file, samples, sample_width):
    format = _struct_format(sample_width, len(samples))
    frame_data = struct.pack(format, *samples)
    wave_file.writeframes(frame_data)
    return wave_file


################ WAV READ AND WRITE ##############



def read_and_process_wav(filename, function_process, draw=False):
    
    print("### READING AND PROCESSING WAV ###")

    f = wave.open(filename)
    f_samples = read_samples(f)
    f_samples= np.array(f_samples)

    ## calculating time vector for drawing ##
    t = 0
    if draw == True :
        seconds = (len(f_samples)//f.getframerate())
        print("These are the seconds", seconds)
        t = np.linspace(0, seconds, len(f_samples), False)
    
    a = 0.2
    f_samples = function_process(t, f_samples, a, draw)
    #f_samples = function_process(t, f_samples, draw)
    
    return (f_samples, f.getframerate())



def write_to_wav(filename, f_samples, framerate, effect="", play= False):

    print("### WRITING TO WAV ###")

    filename = str(filename) + "_" + effect
    obj = wave.open(filename, 'w')
    obj.setnchannels(2)
    obj.setsampwidth(2)
    obj.setframerate(framerate)

    obj = write_samples(obj, f_samples, 2)

    # for i in range(len(f_samples)):
    #     value = f_samples[i]
    #     data = struct.pack('<h', value)
    #     obj.writeframesraw(data)

    obj.close()
    
    if play == True :
        play_wav(filename)


def play_wav(filename):

    print("### PLAYING WAV ###")

    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing