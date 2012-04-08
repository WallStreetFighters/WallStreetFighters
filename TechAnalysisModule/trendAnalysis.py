# -*- coding: utf-8 -*-
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

def trend(a, trendVuln = trendVul):
    """Na podstawie wskaznika kierunkowego prostej wyznaczamy trend"""
    angle = arctan(a)
    angle = angle*(180.0/pi)
    if (angle > -trendVuln and angle < trendVuln):
            return 0 # horyzontalny
    if (angle > trendVuln and angle < 90):
            return 1 # rosnacy
    if (angle <-trendVuln and angle > -90):
            return -1 # malejacy

def linearFun(x1, y1, x2, y2):
    a = (y2 - y1)*1.0/(x2 - x1)
    b = y1 - a*x1
    return a,b

def evalueteFun(a, b, x):
    return a*x + b

def linearFun(array):
    if array.size < 2:
        return 0, 0
    return linearFun(0, array[0], 1, array[1])

def aInRect(array):
    """Sprawdzamy czy punkty w tablicy naleza do prostej +/- rectVul"""
    array = asarray(map(lambda x: x[0], array))
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
        
def myMin(array):
    min = [array[0][0], array[0][1]]
    for i in range(len(array)):
        if array[i][0] < min[0]:
            min = [array[i][0], array[i][1]]
    return min

def myMax(array):
    max = [array[0][0], array[0][1]]
    for i in range(len(array)):
        if array[i][0] > max[0]:
            max = [array[i][0], array[i][1]]
    return max

def findMaxMin(array, factor=div):
    """Znajdujemy linie wsparcia i oporu"""
    z = divideArray(asarray(array), factor)
    x = asarray(map(myMin, z))
    x2 = asarray(map(myMax, z))
    for i in reversed(range(len(x))):
#        print i
        y = asarray(list(combinations(x, i+1)))
        z = map(aInRect, y)
        if max(z) == 1:
            sup = y[z.index(1)]
            break
    for i in reversed(range(len(x2))):
#        print i
        y = asarray(list(combinations(x2, i+1)))
        z = map(aInRect, y)
        if max(z) == 1:
            res = y[z.index(1)]
            break
    return sup, res    
    
def getChannelLines(array, a = 3, b = 4):
    """Wylicza """
    q = map(lambda x, y: [x, y], array, range(len(array)))
    size = len(array)
    if size < 9:
        return findMaxMin(q, 4)
    else:
        return findMaxMin(q[a*size/b:])

#a = [random.randint(0, 100) for i in range(160)]
#print a
#a = arange(40)
#print getChannelLines(a)
def convertValuesToHeadAndShoulders(values, volumine, maxVal, maxVol):
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
    return headAndShoulders(leftArmVal, headVal, rightArmVal,
    leftArmVol, headVol, rightArmVol, maxLeftArmVal, maxLeftArmVol, maxHeadVal,
    maxHeadVol, maxRightArmVol, maxRightArmVal, maxVal, maxVol)
    
def headAndShoulders(leftArmVal, headVal, rightArmVal, leftArmVol, headVol, rightArmVol, maxLeftArmVal, maxLeftArmVol, maxHeadVal,
    maxHeadVol, maxRightArmVol, maxRightArmVal, maxVal, maxVol):
    # print "leftArmVal", leftArmVal
    #   print "headVal", headVal
    #   print "rightArmVal", rightArmVal
    #   print "leftArmVol", leftArmVol
    #   print  "headVol", headVol
    #   print "rightArmVol", rightArmVol
    #   print "max left arm val",  maxLeftArmVal
    #   print "max head val", maxHeadVal
    #   print "max right arm val", maxRightArmVal
    #   print "max left arm vol", maxLeftArmVol
    #   print "max head vol", maxHeadVol
    #   print "max right arm vol", maxRightArmVol
    #   print "max val", maxVal
    #   print "max vol", maxVol
#    print values, volumine, maxVal, maxVol
    print 'A'
    #Wartosc lewego ramienia < glowy i wartosc wolumenu lewego ramienia ma byc najwieksza
#    if maxLeftArmVal > maxHeadVal  or maxRightArmVal > maxHeadVal or maxLeftArmVol < maxHeadVol or maxLeftArmVol < maxRightArmVol:
    if maxLeftArmVal > maxHeadVal  or maxRightArmVal > maxHeadVal or maxHeadVol > maxLeftArmVol or maxHeadVol > maxRightArmVol:
        return 0
    print 'B'
    #wartosc prawego ramienia nie moze zbyt odbiegac od wartosci lewego
    if maxRightArmVal > 1.2 * maxLeftArmVal or maxRightArmVal < 0.8*maxLeftArmVal:
        return 0
    print 'C'
    #wolumin na formacji ma byc malejacy, a conajmniej nie rosnacy
    a, b = regression(leftArmVol+headVol + rightArmVol)
#    if (trend(a) > -1):
    trend = trend(a)
    if (trend(a) > 0):
        return 0
    result = (1.0*maxHeadVal/maxVal + 1.0*maxLeftArmVol/maxVol)/2.0
    if trend > -1:
        result = result * 0.8
    print 'D'
    #wykreslamy linie szyi
    leftArmVal = list(leftArmVal)
    rightArmVal = list(rightArmVal)
    minLeftArmVal = min(leftArmVal[leftArmVal.index(maxLeftArmVal):]) #min z prawej strony max lewego ramienia
    rightArmPeek = rightArmVal.index(maxRightArmVal)
    minRightArmVal = min(rightArmVal[0:rightArmPeek])                       #min z lewej strony max prawego ramienia
    maxRightArmVol = max(rightArmVal[rightArmPeek:])                        #max wolumin z prawej strony max wartosci ramienia
    #sprawdzamy czy linia szyi zostala przelamana przy wyzszym wolumenie
    rightArmValMin = min(rightArmVal[rightArmPeek:])
    print 'E'
    if rightArmValMin > minRightArmVal:
        return 0
    a, b = linearFun(leftArmVal.index(minLeftArmVal), minLeftArmVal,
            rightArmVal.index(minRightArmVal) + len(headVal), minRightArmVal)
    average = sum(rightArmVol)
    if (rightArmValMin >= evaluateFun(a, b, leftArmVal.index(rightArmValMin)) and ):
        return 0
    
    return (1.0*maxHeadVal/maxVal + 1.0*maxLeftArmVol/maxVol)/2    

def smartLookForHeadAndShoulders(values, volumine):
    """Szukamy formacji glowy i ramion"""
    values = asarray(values)
    volumine = asarray(volumine)
    maxVal = max(values)
    maxVol = max(volumine)
    val = asarray(list(combinations(divideArray(values, 5), 3)))
    vol = asarray(list(combinations(divideArray(volumine, 5), 3)))
    z = map(lambda x, y: convertValuesToHeadAndShoulders(val, vol, maxVal, maxVol), val, vol)
    if max(z) > 0:
        return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return 0

def lookForHeadAndShoulders(values, volumine):
    """Szukamy formacji glowy i ramion"""
    values = asarray(values)
    volumine = asarray(volumine)
    maxVal = max(values)
    maxVol = max(volumine)
    val = asarray(divideArray(values, 5))
    vol = asarray(divideArray(volumine, 5))
    z = [0 for i in (range(len(val) - 1))]
    for i in range(len(val) - 3):
        leftArmVal = val[i]
        leftArmVol = vol[i]
        headVal = val[i+1]
        headVol = vol[i+1]
        rightArmVal = val[i+2]
        rightArmVol = vol[i+2]
        maxLeftArmVal = max(leftArmVal)
        maxLeftArmVol = max(leftArmVol)
        maxHeadVal = max(headVal)
        maxHeadVol = max(headVol)
        maxRightArmVol = max(rightArmVol)
        maxRightArmVal = max(rightArmVal)
        z[i] = headAndShoulders(leftArmVal, headVal, rightArmVal,
        leftArmVol, headVol, rightArmVol,
        maxLeftArmVal, maxLeftArmVol, maxHeadVal,
        maxHeadVol, maxRightArmVol, maxRightArmVal, maxVal, maxVol)
    
    if max(z) > 0:
        print "znaleziono", z
        return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return 0


    
def reversedHeadAndShoulders(values, volumine, maxVal, maxVol):
#    print len(values), len(volumine)
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
    values = asarray(values)
    volumine = asarray(volumine)
    minVal = min(values)
    maxVol = max(volumine)
    val = asarray(list(combinations(divideArray(values, div), 3)))
    vol = asarray(list(combinations(divideArray(volumine, div), 3)))
    z = map(lambda x, y: reversedHeadAndShoulders(val, vol, minVal, maxVol), val, vol)
    if max(z) > 0:
      return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return 0


    
#print findMaxMin(arange(1000))

# Tutaj zaczalem pisac formacje prostokatna

# Przekazujemy tablice z wartosciami i teraz poczynajac od najmniejszej,
# funkcja szuka linii wsparcia, minimalnie 3 wartosci
def findMinLine(array):
    size = array.size
    arraySorted = sort(array)
    sizeSorted = arraySorted.size
    numberOfSimilarValues = 0
    for i in range(0,sizeSorted):
        temp = arraySorted[i]
        for j in range(0,size):
            if array[j] == temp:
                numberOfSimilarValues +=1
        if numberOfSimilarValues <2:
            numberOfSimilarValues = 0
        else:
            z = 0
            resultTable = zeros(numberOfSimilarValues)
            indexTable = zeros(numberOfSimilarValues)
            for k in range(0,size):
                if array[k] == temp:
                    resultTable[z] = temp
                    indexTable[z] = k
                    z += 1
            return resultTable,indexTable
    return 0

# Jak wyzej tylko szuka linii oporu
def findMaxLine(array):
    size = array.size
    arraySorted = sort(a)
    arraySorted = arraySorted[ : :-1]
    sizeSorted = arraySorted.size
    numberOfSimilarValues = 0
    for i in range(0,sizeSorted):
        temp = arraySorted[i]
        for j in range(0,size):
            if array[j] == temp:
                numberOfSimilarValues +=1
        if numberOfSimilarValues <2:
            numberOfSimilarValues = 0
        else:
            z = 0
            resultTable = zeros(numberOfSimilarValues)
            indexTable = zeros(numberOfSimilarValues)
            for k in range(0,size):
                if array[k] == temp:
                    resultTable[z] = temp
                    indexTable[z] = k
                    z += 1
            return resultTable,indexTable
    return array([-1]),array([-1]) 
    
    
    
    #Glupi sposob ale musze jakos sprawdzic w nizszej funkcji czy w ogole jest formacja


# Co jest jeszcze do zrobienia :
# - Zwiekszenie ilosci punktow wsparcia i oporu, bo narazie znajduje przy 2
# - Jaka wrazliwosc na odchylenia punkow bo jest poki co zerowa
# - Chyba powinien szukac formacji na kilku zbiorach
def findRectFormation(array):
    resMin,indMin = findMinLine(array)
    resMax,indMax = findMaxLine(array)
    if (resMin[0] == -1 or indMin[0] == -1) or (resMax[0] == -1 or indMax[0] == -1):
        print "Nie odnalazlem formacji prostokata"
        return 0
    if indMin.min() > indMax.min():
        # Wtedy sprawdzamy czy kontynuacja trendu spadkowego
        globalMin = indMax.min()
        globalMax = indMin.max()
        if array[globalMin-1] > array[globalMin] and array[globalMax] > array[globalMax+1]:
            print "Wykrylem formacje prostokatna trendu spadkowego na indeksach ktore zwracam :"
            return globalMin,globalMax
        else:
            print "Formacja prostokata nie wskazuje na kontynuacje trendu spadkowego"
            return 0
    else:
        # Sprawdzamy czy kontynuacja trendu wzrostowego
        globalMin = indMin.min()
        globalMax = indMax.max()
        if array[globalMin] > array[globalMin-1] and array[globalMax+1] > array[globalMax]:
            print "Wykrylem formacje prostokatna trendu wzrostowego na indeksach ktore zwracam :"
            return globalMin,globalMax
        else:
            print "Formacja prostokata nie wskazuje na kontynuacje trendu wzrostowego"
            return 0
        
    
#values = [[1, 2, 10], [1, 2, 20], [1, 2, 12]]
#values = asarray(values)
#volumin = [[1, 2, 10], [1, 1, 1], [1, 1, 1]]
#volumin = asarray(volumin)
#print values
#print volumin
#print headAndShoulders(values, volumin, 21, 10)
#lookForHeadAndShoulders(arange(10), arange(10))
#lookForReversedHeadAndShoulders(arange(10), arange(10))
