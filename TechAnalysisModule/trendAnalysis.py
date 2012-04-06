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
            
def getChannelLines(array):
    """Wylicza """
    if len(array) < 9:
        return findMaxMin(array, 4)
    else:
        return findMaxMin(array[3*len(array)/4:])

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
    factor = min(factor, len(array))
    length = floor(len(array)*1.0/factor)
    res = []
    for i in range(factor - 1):
        res = res + list([array[i*length:(i+1)*length]])
    return list(res + list([array[length*(factor - 1):]]))
        
def findMaxMin(array, factor=div):
    """Znajdujemy linie wsparcia i oporu"""
    z = divideArray(asarray(array), factor)
    print "tablica podtablic ", z
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
    return array, sup, res    
    
def headAndShoulders(values, volumine, maxVal, maxVol):
    print len(values), len(volumine)
    if len(values) != 3 or len(volumine) != 3:
        return 0
    leftArmVal = list(values[0])
    headVal = list(values[1])
    rightArmVal = list(values[2])
    leftArmVol = list(volumine[0])
    headVol = list(volumine[1])
    rightArmVol = list(volumine[2])
    maxLeftArmVal = max(leftArmVal)
    maxLeftArmVol = max(leftArmVol)
    maxHeadVal = max(headVal)
    maxHeadVol = max(headVol)
    maxRightArmVol = max(rightArmVol)
    maxRightArmVal = max(rightArmVal)
    print 'A'
    #Wartosc lewego ramienia < glowy i wartosc wolumenu lewego ramienia ma byc najwieksza
    if maxLeftArmVal > maxHeadVal  or maxRightArmVal > maxHeadVal or maxLeftArmVol < maxHeadVol or maxLeftArmVol < maxRightArmVol:
        return 0
    print 'B'
    #wartosc prawego ramienia nie moze zbyt odbiegac od wartosci lewego
    if maxRightArmVal > 1.2 * maxLeftArmVal or maxRightArmVal < 0.8*maxLeftArmVal:
        return 0
    print 'C'
    #wolumin na formacji ma byc malejacy
    a, b = regression(leftArmVol+headVol + rightArmVol)
    if (trend(a) > -1):
        return 0
    print 'D'
    #wykreslamy linie szyi
    minLeftArmVal = min(leftArmVal[leftArmVal.index(maxLeftArmVal):]) #min z prawej strony max lewego ramienia
    minHeadVal = min(headVal[headVal.index(maxHeadVal):])
    return (1.0*maxHeadVal/maxVal + 1.0*maxLeftArmVol/maxVol)/2    

def lookForHeadAndShoulders(values, volumine):
    """Szukamy formacji glowy i ramion"""
    maxVal = max(values)
    maxVol = max(volumine)
    val = asarray(list(combinations(divideArray(values, div), 3)))
    vol = asarray(list(combinations(divideArray(volumine, div), 3)))
    z = map(lambda x, y: headAndShoulders(val, vol, maxVal, maxVol), val, vol)
    if max(z) > 0:
        return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return 0
    
def reversedHeadAndShoulders(values, volumine, maxVal, maxVol):
    print len(values), len(volumine)
    if len(values) != 3 or len(volumine) != 3:
        return 0
    leftArmVal = list(values[0])
    headVal = list(values[1])
    rightArmVal = list(values[2])
    leftArmVol = list(volumine[0])
    headVol = list(volumine[1])
    rightArmVol = list(volumine[2])
    minLeftArmVal = min(leftArmVal)
    maxLeftArmVol = max(leftArmVol)
    minHeadVal = min(headVal)
    maxHeadVol = max(headVol)
    maxRightArmVol = max(rightArmVol)
    minRightArmVal = min(rightArmVal)
    print 'A'
    #Wartosc lewego ramienia > glowy i wartosc wolumenu lewego ramienia ma byc najwieksza
    if minLeftArmVal < minHeadVal  or minRightArmVal < minHeadVal or maxLeftArmVol < maxHeadVol or maxLeftArmVol < maxRightArmVol:
        return 0
    print 'B'
    #wartosc prawego ramienia nie moze zbyt odbiegac od wartosci lewego
    if minRightArmVal > 1.2 * minLeftArmVal or minRightArmVal < 0.8*minLeftArmVal:
        return 0
    print 'C'
    #wolumin na formacji ma byc rosnacy
    a, b = regression(leftArmVol+headVol + rightArmVol)
    if (trend(a) < 1):
        return 0
    print 'D'
    #wykreslamy linie szyi
    maxLeftArmVal = max(leftArmVal[leftArmVal.index(minLeftArmVal):]) #min z prawej strony max lewego ramienia
    maxHeadVal = max(headVal[headVal.index(minHeadVal):])
    #to nie dokonca prawda wolumin w prawym ramieniu moze byc najwiekszy globalnie bo tam juz moze dojsc do wybicia z linii szyi
    return (1.0*minHeadVal/minVal + 1.0*maxLeftArmVol/maxVol)/2

def lookForReversedHeadAndShoulders(values, volumine):
    """Szukamy odwroconej formacji glowy i ramion"""
    minVal = min(values)
    maxVol = max(volumine)
    val = asarray(list(combinations(divideArray(values, div), 3)))
    vol = asarray(list(combinations(divideArray(volumine, div), 3)))
    z = map(lambda x, y: reversedHeadAndShoulders(val, vol, minVal, maxVol), val, vol)
    if max(z) > 0:
      return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return 0
    
print findMaxMin(arange(10))
    
#values = [[1, 2, 10], [1, 2, 20], [1, 2, 12]]
#values = asarray(values)
#volumin = [[1, 2, 10], [1, 1, 1], [1, 1, 1]]
#volumin = asarray(volumin)
#print values
#print volumin
#print headAndShoulders(values, volumin, 21, 10)
#lookForHeadAndShoulders(arange(10), arange(10))
#lookForReversedHeadAndShoulders(arange(10), arange(10))