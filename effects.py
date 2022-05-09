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



################### echo effects  #### vezi care era faza cu convolutia. Poate pe aia o poti optimiza !!!


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
        


    