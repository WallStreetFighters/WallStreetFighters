from numpy import *
from itertools import *
import matplotlib.dates as mdates
import math

trendVul = 5
rectVul = 0.03
div = 8

def regression(values):
    """Wyznaczamy prosta ktora najlepiej przybliza wykres - y = ax + b"""
    A = vstack([arange(len(values)), ones(len(values))]).T
    a,b = linalg.lstsq(A,values)[0]
    return a,b

def trend(a):
    """Na podstawie wskaznika kierunkowego prostej wyznaczamy trend"""
    angle = arctan(a)
    angle = angle*(180.0/pi)
    if (angle > -trendVul and angle < trendVul):
            return 0 # horyzontalny
    if (angle > trendVul and angle < 90):
            return 1 # rosnacy
    if (angle <-trendVul and angle > -90):
            return -1 # malejacy

def aInRect(array):
    """Sprawdzamy czy punkty w tablicy naleza do prostej +/- rectVul"""
    if array.size < 2:
        return 0
    a = (array[1]-array[0])*1.0
    b = array[0]
    for i in range(2,array.size):
            y = a*i+b
            if y > (1+rectVul)*array[i] or y < (1-rectVul)*array[i]:
                    return 0
    return 1       

def divideArray(array, factor):
    """Dzielimy tablice na #factor tablic, kazda podtablica ma tyle samo elem oprocz ostatniej"""
    factor = factor
    length = ceil(len(array)*1.0/factor)
    res = []
    for i in range(factor - 1):
        res = res + list([array[i*length:(i+1)*length]])
    return asarray(res + list([array[length*(factor - 1):]]))
        
def findMaxMin(array):
    """Znajdujemy linie wsparcia i oporu"""
    z = divideArray(array, div)
    x = asarray(map(lambda x: min(x), z))
    x2 = asarray(map(lambda x: max(x), z))
    print x
    for i in reversed(range(x.size)):
        print i
        y = asarray(list(combinations(x, i+1)))
        z = map(aInRect, y)
        if max(z) == 1:
            sup = y[z.index(max(z))]
            break
    for i in reversed(range(x.size)):
        print i
        y = asarray(list(combinations(x2, i+1)))
        z = map(aInRect, y)
        if max(z) == 1:
            res = y[z.index(max(z))]
            break
    return sup, res    
