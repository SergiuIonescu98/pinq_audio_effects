from utils import *

## sunt independete de FS. Fs doar influenteaza cate puncte pe secunda.
## sau in cazul unui numpy array doar numarul total de valori din array


################ distortotion ################

def infiniteClip(t, mysin, draw = False):

    N = len(mysin)
    distort = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            #distort[n] = 1
            distort[n] = 2**15 - 1 
        else:
            distort[n] = 0

    distort = np.array(distort)

    if draw == True :
        plotSignal(t, distort, "Infinite Clip")
        
    return distort

def halfwaveRectification(t, mysin, draw = False):


    N = len(mysin)
    half = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            half[n] = mysin[n]
        else:
            half[n] = 0

    half = np.array(half)

    if draw == True :
        plotSignal(t, half, "Half Wave Rect")
    
    return half



def fullwaveRectification(t, mysin, draw = False):
    
    N = len(mysin)
    full = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            full[n] = mysin[n]
        else:
            full[n] = -mysin[n]
    
    full = np.array(full)

    if draw == True:
        plotSignal(t, full, "Full Wave Rect")
    
    return full


def cubicDistortion(t, mysin, a, draw = False):

    N = len(mysin)
    cubic = [x-x for x in range(N)]

    print("## Starting signal processing : ##")
    print("THIS IS a ", a)

    for n in range(N):

        cubic[n] = mysin[n] - ((mysin[n]**3)/3)*a # mai mare de int16 si strica
        
        ## micsoram gainul
        #cubic[n] = cubic[n] / 5
    
    print("## Ending Signal Processing ##")
    cubic = np.array(cubic)
    print(cubic)

    if draw == True:
        plotSignal(t, cubic, "Cubic Distort")
    
    return cubic

# def piecewiseOverdrive(t, mysin, draw = False):

#     N = len(mysin)
#     overdrive = 

## bitreduction ??  nu prea e interesant algoritmul


### poate faci efecte paralelel ceva mai complex ca sa poti optimiza ??



################### echo effects  ######################## 
# vezi care era faza cu convolutia. Poate pe aia o poti optimiza !!!


# timeS -> timpul in secunde,msecunde etc
# fs -> f esantionare
# unit -> sec, ms, us etc
def seconds_to_samples(fs, timeS, unit='sec'):
    
    # convert to seconds
    if unit == 'ms': # ms to s
        timeS = timeS/1000
    
    timeSamples = int(timeS * fs) # iti returneaza esantionul la acea secunda prin aproximare.
    return timeSamples

# bpm -> beats per minute. Cat de repede canta cred
# noteDiv -> cat de mult dureaza o nota
def tempo_to_samples(fs, bpm, noteDiv):

    bps = bpm / 60 # beats per second
    secPerBeat = 1/bps
    timeSec = noteDiv * secPerBeat # practiv am convertit bpm to seconds tinand cont de noteDiv si bpm

    timeSamples = int(timeSec*fs)
    return timeSamples



def feedforward_echo(tempo_param, b, x):
    
    fs = tempo_param[0]
    bpm = tempo_param[1]
    noteDiv = tempo_param[2]
    
    d = tempo_to_samples(fs, bpm, noteDiv)  ## asa calculam cate secunde va avea delayul.

    N = len(x)
    y = np.zeros([N, 1])

    for n in range(N):

        if n < d + 1:
            y[n] = x[n]
        else:
            y[n] = x[n] + b * x[n-d]

    return  y


def feedback_echo(tempo_param, a, x):

    fs = tempo_param[0]
    bpm = tempo_param[1]
    noteDiv = tempo_param[2]

    d = tempo_to_samples(fs, bpm, noteDiv)
    a = -0.75

    N = len(x)
    y = np.zeros([N,1])

    for n in range(N):

        if n < d + 1:
            y[n] = x[n]
        else:
            y[n] = x[n] + (-a) * y[n-d]  # y va deveni cred din ce in ce mai mic


    return y

def myConv():
    print("This is my conv")



####################### DELAY BUFFERS #############################
        


def linearBuffer(x, blen):

    buffer = np.zeros(blen) 
                            ## bufferul poate fi mai mare ca delayul, dar mai e nevoie
                            ## de o variabila delay ca sa stii de unde citesti 
    N = np.size(x)
    out = np.zeros([N])

    for n in range(N):

        out[n] = buffer[-1] # ultimul element din buffer vine primul la iesire
                            # sau buffer[delay] in cazul in care buffer e mai mare
        buffer = np.append(x[n], buffer[0:-1]) # shiftare la dreapta

    np.disp(['The original signal was: ', str(x)])
    np.disp(['The final output signal is: ', str(out)])

    return out

def firdelayBuffer(x, fs, bpm, noteDiv, fbGain):

    delay = tempo_to_samples(fs, bpm, noteDiv)
    buffer = np.zeros(delay)
    
    N = np.size(x)
    out = np.zeros([N])

    for n in range(N):
        out[n] = x[n]+ fbGain*buffer[-1]
        buffer = np.append(x[n], buffer[0:-1])

    return out


def circularBuffer(x_sample, buffer, delay, index):

    len_b = len(buffer)

    indexC = ((index) % len_b) # calculeaza indexC curent unde adaugi
    indexD = ((index - delay) % len_b) # calculeaza indexD curent pe unde ies valori

    # print("##")
    # print("Index C ", indexC)
    # print("Index D ", indexD)
    # print("##\n")

    y_sample = buffer[indexD]
    buffer[indexC] = x_sample ## stocheaza in indexC curent valoarea curenta de la X

    return y_sample


def circularechoBuffer(x_sample, buffer, delay, index, fbGain):

    len_b = len(buffer)

    indexC = ((index) % len_b) # calculeaza indexC curent unde adaugi
    indexD = ((index - delay) % len_b) # calculeaza indexD curent pe unde ies valori

    # print("##")
    # print("Index C ", indexC)
    # print("Index D ", indexD)
    # print("##\n")

    y_sample = fbGain*buffer[indexD] + x_sample # aduni aici ca sa fie ecou
    buffer[indexC] = x_sample ## stocheaza in indexC curent valoarea curenta de la X

    return y_sample


################################# vibrato Effect ########



def vibratoEffect(x, buffer, Fs, n, depth, rate):
    # Calculate lfo(low freq osc) for current sample
    t = n/Fs
    lfo = (depth/2) * np.sin(2 * np.pi * rate * t) + depth
    # depth = amplitutde of lfo -> how wide the range of pitches are changed
    # rate = freq of lfo -> how fast the pitch change
    # pitch = freq ? ( pitch senzatia subiectiva de frecevnta )

    # Determine indexes for circular buffer
    N = len(buffer)
    indexC = np.mod(n, N)  # Current index in circular buffer


    ######################################
    # fractional delay with interpolation 
    # circular buffer getting out the sample

    fracDelay = np.mod(n-lfo, N)    # Delay index in circular buffer 
                                    ### aici e folosit LFO
                                    ### LFO e folosit in selectia de INDEX din BUFFER

    intDelay = int(np.floor(fracDelay))  # Fractional delay indices
    frac = fracDelay - intDelay

    nextSamp = np.mod(intDelay, N) - 1  # Next index in circular buffer
    # face combinatie liniara intre indexul curent de iesire si indexul urmator
    out = (1-frac) * buffer[intDelay-1] + frac * buffer[nextSamp]
    
    
    ################################################
    # Store the current output in appropriate index
    buffer[indexC] = x

    return out, buffer


## trebuie sa inteleg mai bine fractional delay....atata tot. La fel e si cu chorus
## SI GATAAAA cu efectele momentan ( poate mai paralelizezi ceva efecte paralele )
## vezi dupa asa ca idee generala cum faci audio-in audio-out in fpga
## vezi ce inseamna imbunatatiri in python
## vezi cum a facut aia alg A*
## vezi cum faci cu HDMI doar asa ca si plan ca sa nu te arunci degeaba