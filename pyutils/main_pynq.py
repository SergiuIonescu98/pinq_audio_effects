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


def main_pynq(options_effect="infinitClip", options_file="long"):

        
        print("#### Selected effect #### ", options_effect)
        print("#### Selected file dim #### ", options_file)

        ##############################

        file_in = ''
        if  options_file == "short":
                file_in = 'Audio Files/AcGtr_short.wav'
        elif  options_file == "long":
                file_in = 'Audio Files/AcGtr.wav'
        print("#### Selected file dim #### " ,file_in)

        file_out = 'out'
        #reverb_in = 'Audio Files/reverbIR.wav'
        reverb_in = 'Audio Files/reverbIR_short.wav'



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
                if options_effect == "reverb":
                        all_bytes = memory.read(conv_size)
                else:
                        all_bytes = memory.read(melody_size)
                #print("Data after IPC ", all_bytes) # reads the 8 bytes.
                print("")

                ## convert 2 bytes back to samples
                proccesed_music = []
                i = 0

                if options_effect == "reverb":
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
        write_to_wav(file_out, proccesed_music, my_fs, effect=options_effect, play=False)