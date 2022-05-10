import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plot
import simpleaudio as sa
import struct
import wave
import soundfile
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


# control = [ 0 1 ]

def read_and_process_wav(filename, function_process=None, control = -1, draw=False):
    
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
    
    
    if function_process != None:
        if control >= 0 :
            a = control
            f_samples = function_process(t, f_samples, a, draw)
        elif control == -1:
            f_samples = function_process(t, f_samples, draw)

    
    
    return (f_samples, f.getframerate())




def write_raw(filename, f_samples, normalise = False, effect="", typeB='int16'):
    print("### WRITING RAW FILE ###")

    raw_samples = f_samples
    
    if normalise == True:
        print("## Normalising ##")
        raw_samples = normalise_16b(raw_samples)

    filename = str(filename) + "_" + effect + ".raw"
    raw_samples.astype(typeB).tofile(filename) # cred ca daca vrei pe 16 trebuie sa si normalizezi
                                               # si cred ca mai e si din cauza inregistrarii. foarte posibil
                                               # daca ai int ul prea mic canta de 2 ori mai lent . 
                                               # dacai ai int ul mai mare canta de 2 ori mai repede pentru ca va considera
                                               # 2 esantioane de 16 ca fiind unul singur de 32.


def write_to_wav(filename, f_samples, framerate, effect="", play= False):

    print("### WRITING TO WAV ###")

    filename = str(filename) + "_" + effect + ".wav"
    obj = wave.open(filename, 'w')
    obj.setnchannels(2)
    obj.setsampwidth(2)
    obj.setframerate(framerate)
    f_samples = normalise_16b(f_samples)
    
    obj = write_samples(obj, f_samples, 2)
    obj.close()
    
    if play == True :
        play_wav(filename)


def play_wav(filename):

    print("### PLAYING WAV ###")

    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


def normalise_16b(f_samples): ## Este esentiala in cazul in care ai esantioane peste 32 de biti.

    ### MUUUUCH BETTER this way ### Parte din gajait e si din cauza normalizarii cred.
    #max_sample = np.max(np.abs(f_samples))
    for i in range(len(f_samples)): 
        if f_samples[i] > 2**15 - 1:
            f_samples[i] = 2**15 - 1
            #f_samples[i] = f_samples[i] * (2**15 - 1) / max_sample
    ################################
    # f_samples = f_samples * (2**15 - 1) / np.max(np.abs(f_samples)) ### !! very important. Daca ai pe 32 iti strica prea mult.
    
    #########################################################################
    
    f_samples = f_samples.astype(np.int16)
    return f_samples




###############################################

def read_and_process_echo(filename, function_process, bpm, noteDiv, b):
    
    print("### READING AND PROCESSING WAV ###")

    f = wave.open(filename)
    f_samples = read_samples(f)
    f_samples= np.array(f_samples)

    ## calculating time vector for drawing ##
    f_samples = function_process([f.getframerate(), bpm, noteDiv], b, f_samples)
    
    return (f_samples, f.getframerate())