from multiprocessing.context import SpawnContext
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
# noteDiv -> cat de mult dureaza o nota, cat de mult iei din BEAT. A cata parte din beat ( un intreg , jumate etc ?)
def tempo_to_samples(fs, bpm, noteDiv):

    bps = bpm / 60 # beats per second
    print("This is the bps", bps);

    secPerBeat = 1/bps
    timeSec = noteDiv * secPerBeat # practiv am convertit bpm to seconds tinand cont de noteDiv si bpm
    print("TIME SEC ", timeSec)
    timeSamples = int(timeSec*fs)
    return timeSamples



def feedforward_echo(tempo_param, b, x):
    
    fs = tempo_param[0]
    bpm = tempo_param[1]
    noteDiv = tempo_param[2]
    
    d = tempo_to_samples(fs, bpm, noteDiv)  ## asa calculam cate secunde va avea delayul.
    print("## TEMPO VAL ##", d)
    
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

    print(buffer)
    for n in range(N):

        out[n] = buffer[-1] # ultimul element din buffer vine primul la iesire
                            # sau buffer[delay] in cazul in care buffer e mai mare
        buffer = np.append(x[n], buffer[0:-1]) # shiftare la dreapta
        ## buffer[0:-1] toate elementele mai putin ultimul
        #print(buffer)

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


## n e index curent din semnal
## N mae e lungime buffer

def vibratoEffect(x, buffer, Fs, n, depth, rate):
    # Calculate lfo(low freq osc) for current sample
    #print("## CALLING VIBRATO EFFECT ###")
    
    t = n/Fs
    lfo = (depth/2) * np.sin(2 * np.pi * rate * t) + depth ## iti returneaza o singura valoarea
    ## ptr ca t nu e un vector. Ci e un moment de timp ce variaza dupa frecveta de esantionare. n/Fs
    
    #print("## LFO VALUE ##")
    #print(lfo)
    
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
                                    ### acel n-lfo poate fi interpretat
                                    ### cati indecsi vrei sa dai in spate
                                    ### cat de intarziat sa fie semnalul
    #print("#####")
    #print(fracDelay)
    #print("#####")
    
    intDelay = int(np.floor(fracDelay))  # Fractional delay indices---cat sa fie delayul. Indexul de iesire cum ar fi
    frac = fracDelay - intDelay ## cat la suta ne aproiem de urmatorul delay fata de cel normal

    nextSamp = np.mod(intDelay, N) - 1  # Next index in circular buffer
    # face combinatie liniara intre indexul curent de iesire si indexul urmator
    out = (1-frac) * buffer[intDelay-1] + frac * buffer[nextSamp]
    
    
    ################################################
    # Store the current output in appropriate index
    buffer[indexC] = x

    return out, buffer

####### iar de fapt fractional delay nu inseamna decat cum variezi trecerea de n la n + 1- . BA NuUU
####### cat de mare sa fie ponderea n+fract. 
##### alta e filosofia. TU ai un delay care variaza. Dar tu vrei ca el sa varieze uniform
#### nu doar sa treaca de la un delay de n la n+1 dupa n+2. Vrei un delay fin. el tot creste. Poate si pana la infinit
#### ca el sa creasca fin vom lua si delayuri intre n-uri. Dar ce valori scoatem ptr valori intre indecsi ?
#### si aici vine fractional delay care calculeaza valorea interpolata ( ca pana la urma orice fractie poate fi intre 2 intregi)
#### si lfo de fapt imi face delayuri 75 +- 32 inclusiv valorile intre cele intregi. Si fractional interp
### ma ajuta sa le calculez.
### bun si inainte cu un circular buffer normal...memorai la fiecare iteratie din semnalul tau de intrare bufferul nou
### faceai for si fiecare iteratie bagai ceva in buffer si scoteai pe alt index ( delayul )
### dar acum ai tot o singura iteratie. Insa n am inteles cum scoti ? Ca acum delayul e un sinus. Nu pare a fi un for in for
### pai da. Pentru ca de fapt acel sinus...variaza in timp dupa ce t ii dau eu. si t-ul e raportat la esantion adica timp
### variind delayul de fapt variaza frecventa. Exista o demonstratatie

## SI GATAAAA cu efectele momentan ( poate mai paralelizezi ceva efecte paralele )
## vezi dupa asa ca idee generala cum faci audio-in audio-out in fpga
## vezi ce inseamna imbunatatiri in python
## vezi cum a facut aia alg A*
## vezi cum faci cu HDMI doar asa ca si plan ca sa nu te arunci degeaba


def linearInterpolationDelay():

    x = np.append(1, np.zeros(9))  # Horizontal for displaying in command window

    fracDelay = 3.2  # Fractional delay length in samples
    intDelay = int(np.floor(fracDelay))  # Round down to get the previous (3)
    frac = fracDelay - intDelay  # Find the fractional amount (0.2)

    buffer = np.zeros(5)  # len(buffer) >= ceil(fracDelay)
    N = len(x)

    out = np.zeros(N)

    # Series Fractional Delay
    for n in range(N):
        out[n] = (1-frac) * buffer[intDelay-1] + frac * buffer[intDelay]
        buffer = np.append(x[n], buffer[0:-1])
        # buffer[1:] = buffer[0:-1]
        # buffer[0] = x[n]

    # Compare the input and output signals
    np.disp(['The orig. input signal was: ', str(x)])
    np.disp(['The final output signal is: ', str(out)])


#################

def chorusEffect(x, buffer, Fs, n, depth, rate, predelay, wet):
    # Calculate time in seconds for current sample
    t = n/Fs
    lfoMS = depth * np.sin(2 * np.pi * rate * t) + predelay
    lfoSamples = (lfoMS/1000) * Fs

    # Wet/dry mix
    mixPercent = wet  # 0 = only dry, 100 = only wet
    mix = mixPercent/100

    fracDelay = lfoSamples
    intDelay = int(np.floor(fracDelay))
    frac = fracDelay - intDelay

    # Store dry and wet signals
    drySig = x
    wetSig = (1-frac) * buffer[intDelay-1] + frac * buffer[intDelay]

    # Blend parallel paths
    out = (1-mix) * drySig + mix * wetSig

    # Linear buffer implemented
    buffer = np.append(x, buffer[0:-1])
    # buffer[1:] = buffer[0:-1]
    # buffer[0] = x

    return out, buffer

# cu delay variat in paralel de maxim 50 ms creeaza un efect de cor
# ptr ca in cor nimeni nu canta perfect..exista mini shiftari de pitch