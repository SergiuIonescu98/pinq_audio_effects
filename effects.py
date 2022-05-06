from utils import *

## sunt independete de FS. Fs doar influenteaza cate puncte pe secunda.
## sau in cazul unui numpy array doar numarul total de valori din array

def infiniteClip(t, mysin, draw = False):

    N = len(mysin)
    distort = [x-x for x in range(N)]
    for n in range(N):

        if mysin[n] >= 0:
            #distort[n] = 1
            distort[n] = 2**15 - 1 ### vezi aici ca se aude cam cu multe armonici
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