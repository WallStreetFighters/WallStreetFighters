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

def linearFun(array):
    if array.size < 2:
        return 0, 0
    a = (array[1]-array[0])*1.0
    b = array[0]
    return a,b

def aInRect(array):
    """Sprawdzamy czy punkty w tablicy naleza do prostej +/- rectVul"""
    a, b = linearFun(array)
    if a == 0:
        return 0
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

    
def headAndShoulders(values, volumine):
    if values.size != 3 or volumine.size != 3:
        return
    leftArmVal = values[0]
    headVal = values[1]
    rightArmVal = values[2]
    leftArmVol = volumine[0]
    headVol = volumine[1]
    rightArmVol = volumine[2]
    maxLeftArmVal = max(leftArmVal)
    maxLeftArmVol = max(leftArmVol)
    maxHeadVal = max(headVal)
    maxHeadVol = max(headVol)
    maxRightArmVol = max(rightArmVol)
    maxRightArmVal = max(rightArmVal)

    #Wartosc lewego ramienia < glowy i wartosc wolumenu lewego ramienia ma byc najwieksza
    if maxLeftArmVal > maxHeadVal  or maxRightArmVal > maxHeadVal or maxLeftArmVol < maxHeadVol or maxLeftArmVol < maxRightArmVol:
        return 0

    #wartosc prawego ramienia nie moze zbyt odbiegac od wartosci lewego
    if maxRightArmVal > 1.1 * maxLeftArmVal or maxRightArmVal < 0.9*maxLeftArmVal:
        return 0

    #wolumin na formacji ma byc malejacy
    if (trend(regression(list(leftArmVol)+list(headVol)+list(rightArmVol))) > -1):
        return 0
    
    #wykreslamy linie szyi
    minLeftArmVal = min(leftArmVal[leftArmVal.index(maxLeftArmVal):]) #min z prawej strony max lewego ramienia
    minHeadVal = min(headVal[headVal.index(maxHeadVal):])
    return 1    

def lookForHeadAndShoulders(values, volumine):
    """Szukamy formacji glowy i ramion"""
    val = asarray(list(combinations(divideArray(values, div), 3)))
    vol = asarray(list(combinations(divideArray(volumine, div), 3)))
    map(headAndShoulders)
    
def headAndShouldersReversed(array):
    """Szukamy odwroconej formacji glowy i ramion"""
    return
    
    
values = [1, 2, 10, 1, 2, 20, 1, 2, 12]
values = asarray(values)
volumin = [1, 2, 10, 1, 1, 1, 1, 1, 1]
volumin = asarray(volumin)
print values
print volumin
print lookForHeadAndShoulders(values, volumin)
