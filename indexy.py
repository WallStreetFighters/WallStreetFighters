from numpy import *

def expotentialAverage(array):
        result = 0
        divisor = 0
        factor = 2.0/(array.size+1)
        for i in range(array.size):
                result += array[i]*((1-factor)**(array.size-i-1))
                divisor += (1-factor)**(array.size-i-1)
        result /= divisor
        return result

# array - tablica z wartosciami cen zamkniec itp, duration - czas trwania liczonej sredniej krokowej
# Zwraca tablice jednowymiarowa z wartosciami sredniej krokowej dla przedzialu [size/2,size-1], aby obliczyc wartosci tablica wejsciowa musi byc 2x wieksza od zakresu(duration)
# modes : 1-SMA(simple moving average), 2-WMA(weighted moving average), 3-EMA(expotential moving average) 
def movingAverage(array,duration,mode):
        values = zeros(array.size/2)
        size = array.size
        j = 0
        for i in range(size/2,size):
                tempTable = array[i-duration+1:i+1]
                if mode == 1:
                        values[j] = simpleArthmeticAverage(tempTable)
                if mode == 2:
                        values[j] = weightedAverage(tempTable)
                if mode == 3:
                        values[j] = expotentialAverage(tempTable)
                j += 1
        return values

# Nalezy przekazac tablice ilosci spadajacych i wzrastajacych spolek.
# Kazdy indeks odpowiada jednemu dniu. 
def adLine(advances, declines):
        size = advances.size
        values = zeros(size)
        for i in range(0,size):
                netAdvance = advances[i]-declines[i]
                if i==0:
                        values[i] = netAdvance
                else:
                        values[i] = values[i-1] + netAdvance
        return values

# Minimalne przekazane tablice musza miec conajmmniej 40 wartosci.
# Wersja nieprzetestowana
def mcClellanOscillator(advances,declines):
        size = advances.size
        values = zeros(size)
        ratioAdjusted = zeros(size)
        for i in range(0,size):
                ratioAdjusted[i] = advances[i]-declines[i]
        result19 = movingAverage(ratioAdjusted,19,3)
        result39 = movingAverage(ratioAdjusted,39,3)
        return result19-result39
                
                
                
