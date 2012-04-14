# -*- coding: utf-8 -*-
from numpy import *
from itertools import *
from random import *
import matplotlib.dates as mdates
import math
 
trendVul = 5
rectVul = 0.03
hsVul = 0.1
div = 8
hsDiv = 12
hsDiff = 0.03

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

def regression(values):
    """Wyznaczamy prosta ktora najlepiej przybliza wykres - y = ax + b"""
    A = vstack([arange(len(values)), ones(len(values))]).T
    a,b = linalg.lstsq(A,values)[0]
    return a,b

def optimizedTrend(values):
    minV = min(values)
    maxV = max(values)
    size = len(values)
    index = []
    val = []
    for i in range(size):
        val = val + [(values[i] - minV)*1.0/(maxV - minV)]
        index = index + [i*1.0/size]
    index = asarray(index)
    A = vstack([index, ones(len(val))]).T
    a,b = linalg.lstsq(A,val)[0]
    return trend(a)
    
# x = [1] + [1 for i in range(90)]
# x = x + [2 for i in range()]
# print "x = ", x
# print "\n", optimizedTrend(x)
# print "\n"
# x = [1 + randint(1, 10)/100.0 for i in range(365)]
# x = x + [1.1]
# print x
# print optimizedTrend(x)

    
def linearFun(x1, y1, x2, y2):
    a = (y2 - y1)*1.0/(x2 - x1)
    b = y1 - a*x1
    return a,b

def evaluateFun(a, b, x):
    return a*x + b

def linearFunFromArray(array):
    if array.size < 2:
        return 0, 0
    return linearFun(0, array[0], 1, array[1])

def lineFrom2Points(x1,y1,x2,y2):
    """Zwraca współczynniki a,b prostej przechodzącej przez 2 dane punkty"""
    a=(y2-y1)/(x2-x1)
    b=y1-a*x1
    return (a,b)

def aInRect(array):
    """Sprawdzamy czy punkty w tablicy naleza do prostej +/- rectVul"""
    array = asarray(map(lambda x: x[0], array))
    a, b = linearFunFromArray(array)
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
    maxHeadVol, maxRightArmVal, maxRightArmVol, maxVal, maxVol, prev = []):
    
    
    if len(prev):
        if optimizedTrend(prev) == -1:
            return 0, [0, 0, 0, 0]     #trend jest rosnacy, nie bedzie zmiany trendu
 #   print 'A'
    #Wartosc lewego ramienia < glowy i wartosc wolumenu lewego ramienia ma byc najwieksza
#    if maxLeftArmVal > maxHeadVal  or maxRightArmVal > maxHeadVal or maxLeftArmVol < maxHeadVol or maxLeftArmVol < maxRightArmVol:
    if maxLeftArmVal > (1-hsDiff)*maxHeadVal  or maxRightArmVal > (1-hsDiff)*maxHeadVal: 
        return 0, [0, 0, 0, 0]
    mHVol = maxHeadVol
    mLVol = maxLeftArmVol
    mRVol = maxRightArmVol
 #   print 'B'
    #wartosc prawego ramienia nie moze zbyt odbiegac od wartosci lewego
    if maxRightArmVal > (1+hsVul) * maxLeftArmVal or maxRightArmVal < (1-hsVul)*maxLeftArmVal:
        return 0, [0, 0, 0, 0]
#    print 'C'
    #wolumin na formacji ma byc malejacy, a conajmniej nie rosnacy
    volTrend = optimizedTrend(leftArmVol+headVol + rightArmVol)
    if (volTrend > 0):
        return 0, [0, 0, 0, 0]
    result = (1.0*maxHeadVal/maxVal + 1.0*maxLeftArmVol/maxVol)/2.0
    if volTrend > -1:
        result = result * 0.8
    print 'D'
    #wykreslamy linie szyi
    leftArmVal = list(leftArmVal)
    rightArmVal = list(rightArmVal)
    minLeftArmVal = min(leftArmVal[leftArmVal.index(maxLeftArmVal):]) #min z prawej strony max lewego ramienia
    rightArmPeek = rightArmVal.index(maxRightArmVal)
    if rightArmPeek == 0:
        return 0, [0, 0, 0, 0]
    minRightArmVal = min(rightArmVal[0:rightArmPeek])                       #min z lewej strony max prawego ramienia
    maxRightArmVol = max(rightArmVol[rightArmPeek:])                        #max wolumin z prawej strony max wartosci ramienia
    #sprawdzamy czy linia szyi zostala przelamana przy wyzszym wolumenie
    rightArmValMin = min(rightArmVal[rightArmPeek:])
    rightArmMaxVol = max(rightArmVol[0:rightArmPeek])
    print 'E'
    if rightArmValMin > minRightArmVal:
        return 0, [0, 0, 0, 0]
    diff = len(leftArmVal) + len(headVal)
    a, b = linearFun(leftArmVal.index(minLeftArmVal), minLeftArmVal,
             rightArmVal.index(minRightArmVal) + diff, minRightArmVal)
    
    if (trend(a) == 1):
        return 0, [0, 0, 0, 0]
        
    print "Czy przelamano linie szyi?"
    
    if (rightArmValMin >= evaluateFun(a, b, diff + rightArmVal.index(rightArmValMin)) and rightArmMaxVol < maxRightArmVol):
        return 0, [0, 0, 0, 0]
    
    if maxHeadVol > maxLeftArmVol or maxHeadVol > maxRightArmVol:
        result = result *0.5
    
    return result, [leftArmVal.index(minLeftArmVal), minLeftArmVal,
                    len(rightArmVal) + diff, evaluateFun(a, b, len(rightArmVal) + diff)]    

def smartLookForHeadAndShoulders(values, volumine):
    """Szukamy formacji glowy i ramion"""
    print "Szukamy formacji glowy i ramion"
    values = asarray(values)
    volumine = asarray(volumine)
    maxVal = max(values)
    maxVol = max(volumine)
    for i in reversed(range(5, div+1)):
        val = asarray(list(combinations(divideArray(values, i), 3)))
        vol = asarray(list(combinations(divideArray(volumine, i), 3)))
        z = map(lambda x, y: convertValuesToHeadAndShoulders(x, y, maxVal, maxVol), val, vol)
        print "z = ", z
        if max(z) > 0:
            return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return [0], [0]

def lookForHeadAndShoulders(values, volumine):
    """Szukamy formacji glowy i ramion"""
    print "Szukamy formacji glowy i ramion"
    if (len(values) < 15):
        return [0, 0, 0, 0]
    values = asarray(values)
    volumine = asarray(volumine)
    maxVal = max(values)
    maxVol = max(volumine)
    
    for j in reversed(range(div, min(2*hsDiv, len(values)))):
        val = list(divideArray(values, j))
        vol = list(divideArray(volumine, j))
        z = [0 for i in (range(len(val) - 1))]
        neckLine = [[0, 0, 0, 0] for i in (range(len(val) - 1))]
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
            maxRightArmVal = max(rightArmVal)
            maxRightArmVol = max(rightArmVol)
            prev = []
            if (i > 0):
                prev = val[i - 1]
            z[i], neckLine[i] = headAndShoulders(leftArmVal, headVal, rightArmVal, leftArmVol,
                                                headVol, rightArmVol, maxLeftArmVal,  maxLeftArmVol,
                                                maxHeadVal, maxHeadVol, maxRightArmVal, maxRightArmVol, maxVal, maxVol, prev)
    
        if max(z) > 0:
            print "znaleziono", z
            index = z.index(max(z))
            diff = sum(map(lambda x: len(x), val[0:index]))
            neckLine[index][0] += diff
            neckLine[index][2] += diff
            return neckLine[index]
    
    print "nie znaleziono"
    return [0, 0, 0, 0]



    
def reversedHeadAndShoulders(leftArmVal, headVal, rightArmVal, leftArmVol, headVol, rightArmVol, minLeftArmVal, maxLeftArmVol, minHeadVal,
        maxHeadVol, minRightArmVal, maxRightArmVol, minVal, maxVol, prev = []):

    if len(prev):
        if optimizedTrend(prev) == 1:
            return 0, [0, 0, 0, 0]

    mHVol = maxHeadVol
    mLVol = maxLeftArmVol
    mRVol = maxRightArmVol
#    print 'A'
    #Wartosc lewego ramienia > glowy i wartosc wolumenu glowy ma byc najmniejsza
    if minLeftArmVal < (1 + hsDiff)*minHeadVal  or minRightArmVal < (1+hsDiff)*minHeadVal:
        return 0, [0, 0, 0, 0]
#    print 'B'
    #wartosc prawego ramienia nie moze zbyt odbiegac od wartosci lewego
    if minRightArmVal > (1+hsVul) * minLeftArmVal or minRightArmVal < (1-hsVul)*minLeftArmVal:
        return 0, [0, 0, 0, 0]
#    print 'C'
    #wolumin na formacji ma byc niemalejacy
    volTrend = optimizedTrend(leftArmVol+headVol + rightArmVol)
    if (volTrend > 0):
        return 0, [0, 0, 0, 0]
    result = (1.0*minHeadVal/minVal + 1.0*maxLeftArmVol/maxVol)/2
    if volTrend < 0:
        result = result * 0.8
    print 'D'
    #wykreslamy linie szyi
    leftArmVal = list(leftArmVal)
    rightArmVal = list(rightArmVal)
    maxLeftArmVal = max(leftArmVal[leftArmVal.index(minLeftArmVal):])        #max z prawej strony min lewego ramienia
    rightArmPeek = rightArmVal.index(minRightArmVal)
    if rightArmPeek == 0:
        return 0, [0, 0, 0, 0]
    
    maxRightArmVal = max(rightArmVal[0:rightArmPeek])                       #max z lewej strony min prawego ramienia
    maxRightArmVol = max(rightArmVol[rightArmPeek:])                        #max wolumin z prawej strony min wartosci ramienia
    #sprawdzamy czy linia szyi zostala przelamana przy wyzszym wolumenie
    rightArmValMax = max(rightArmVal[rightArmPeek:])
    rightArmMaxVol = max(rightArmVol[0:rightArmPeek])
    print 'E'
    if  maxRightArmVal > rightArmValMax:
        return 0, [0, 0, 0, 0]
    
    diff = len(leftArmVal) + len(headVal)
    a, b = linearFun(leftArmVal.index(maxLeftArmVal), maxLeftArmVal,
            rightArmVal.index(maxRightArmVal) + diff, maxRightArmVal)
    if (trend(a) == -1):
        return 0, [0, 0, 0, 0]
    
    print "Czy przelamano linie szyi?"
    if (rightArmValMax <= evaluateFun(a, b, rightArmVal.index(rightArmValMax) + diff) and rightArmMaxVol < maxRightArmVol):
        return 0, [0, 0, 0, 0]
        
    if (maxLeftArmVol < maxHeadVol or maxRightArmVol < maxHeadVol):
        result = result * 0.5
    return result, [leftArmVal.index(maxLeftArmVal), maxLeftArmVal,
                    len(rightArmVal) + diff, evaluateFun(a, b, len(rightArmVal) + diff)] 
  
def smartLookForReversedHeadAndShoulders(values, volumine):
    """Szukamy odwroconej formacji glowy i ramion"""
    print "Szukamy odwroconej formacji glowy i ramion"
    values = asarray(values)
    volumine = asarray(volumine)
    minVal = min(values)
    maxVol = max(volumine)
    for i in reversed(range(4, div+1)):
        val = asarray(list(combinations(divideArray(values, i), 3)))
        vol = asarray(list(combinations(divideArray(volumine, i), 3)))
        z = map(lambda x, y: reversedHeadAndShoulders(x, y, minVal, maxVol), val, vol)
        print "z = ", z
        if max(z) > 0:
          return val[z.index(max(z))], vol[z.index(max(z))]
    print "nie znaleziono"
    return [0], [0]

def lookForReversedHeadAndShoulders(values, volumine):
    """Szukamy odwroconej formacji glowy i ramion"""
    print "Szukamy odwroconej formacji glowy i ramion"
    if (len(values) < 15):
         return [0, 0, 0, 0]
    values = asarray(values)
    volumine = asarray(volumine)
    minVal = min(values)
    maxVol = max(volumine)

    for j in reversed(range(div, min(2*hsDiv, len(values)))):
        val = list(divideArray(values, j))
        vol = list(divideArray(volumine, j))
        z = [0 for i in (range(len(val) - 1))]
        neckLine = [[0, 0, 0, 0] for i in (range(len(val) - 1))]
        print "\nsprawdzamy ", j
        for i in range(len(val) - 3):
            leftArmVal = val[i]
            leftArmVol = vol[i]
            headVal = val[i+1]
            headVol = vol[i+1]
            rightArmVal = val[i+2]
            rightArmVol = vol[i+2]
            minLeftArmVal = min(leftArmVal)
            maxLeftArmVol = max(leftArmVol)
            minHeadVal = min(headVal)
            maxHeadVol = max(headVol)
            maxRightArmVol = max(rightArmVol)
            minRightArmVal = min(rightArmVal)
            prev = []
            if (i > 0):
                prev = val[i - 1]
            z[i], neckLine[i] = reversedHeadAndShoulders(leftArmVal, headVal, rightArmVal,
                                                        leftArmVol, headVol, rightArmVol,
                                                        minLeftArmVal, maxLeftArmVol, minHeadVal,
                                                        maxHeadVol, minRightArmVal, maxRightArmVol,
                                                        minVal, maxVol, prev)
        if max(z) > 0:
            print "znaleziono", z
            index = z.index(max(z))
            diff = sum(map(lambda x: len(x), val[0:index]))
            neckLine[index][0] += diff
            neckLine[index][2] += diff
            return neckLine[index]

    print "nie znaleziono", z
    return [0, 0, 0, 0]
   
def findWedge(values):  
    """Znajdujemy formację klina. Generalnie sprowadza się to do tego samego co trend,
    tylko sprawdzamy czy linie kanału są zbieżne.
    Interpretacja: 
    klin zwyżkujący zapowiada odwrócenie trendu wzrostowego lub kontynuację spadkowego
    klin zniżkujący -  na odwrót"""    
    dataPart, sup, res = getChannelLines(values)    
    diff = len(values) - len(dataPart)        
    supx0,supy0,supx1,supy1 = dataPart.index(sup[0]) + diff, sup[0], dataPart.index(sup[len(sup)-1])+diff, sup[len(sup)-1]
    resx0,resy0,resx1,resy1 = dataPart.index(res[0]) + diff, res[0], dataPart.index(res[len(res)-1])+diff, res[len(res)-1]
    supLine=lineFrom2Points(supx0,supy0,supx1,supy1)
    resLine=lineFrom2Points(resx0,resy0,resx1,resy1)    
    supAngle = arctan(supLine[0])*(180.0/pi)
    resAngle = arctan(resLine[0])*(180.0/pi)
    print "supAngle: ", supAngle, "resAngle: ", resAngle
    #klin zwyżkujący
    if resAngle>trendVul and supAngle>resAngle:
        return ('rising_wedge',(resx0,resy0,resx1,resy1),(supx0,supy0,supx1,supy1))
    #klin zniżkujący
    elif supAngle < -trendVul and resAngle<supAngle:
        return ('falling_wedge',(resx0,resy0,resx1,resy1),(supx0,supy0,supx1,supy1))    
    return None    
   
#print findMaxMin(arange(1000))
#lookForHeadAndShoulders(arange(100), arange(100))
#lookForReversedHeadAndShoulders(arange(100), arange(100)) 

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
