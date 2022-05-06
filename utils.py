import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plot
import simpleaudio as sa
import struct


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





def _struct_format(sample_width, nb_samples):
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