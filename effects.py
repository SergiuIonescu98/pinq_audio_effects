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

        #cubic[n] = np.int16(mysin[n] - a*(1/3)*(mysin[n]**3))
        cubic[n] = np.int16(mysin[n] - (mysin[n]**3)//3)
        #cubic[n] = np.int16(mysin[n])
    
    print("## Ending Signal Processing ##")
    cubic = np.array(cubic)

    if draw == True:
        plotSignal(t, cubic, "Cubic Distort")
    
    return cubic

# def piecewiseOverdrive(t, mysin, draw = False):

#     N = len(mysin)
#     overdrive = 

## bitreduction ??
