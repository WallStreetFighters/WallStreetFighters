from numpy import *
from itertools import *
import matplotlib.dates as mdates
import math

trendVul = 5
rectVul = 0.03

def regresion(values,numDates):
        #numDates = mdates.date2num(dates)
        A = vstack([numDates, ones(len(numDates))]).T
        a,b = linalg.lstsq(A,values)[0]
        return a,b

def trend(a):
        angle = arctan(a)
        angle = angle*(180.0/pi)
        if (angle > -trendVul and angle < trendVul):
                return 0 # horyzontalny
        if (angle > trendVul and angle < 90):
                return 1 # rosnacy
        if (angle <-trendVul and angle > -90):
                return -1 # malejacy

def aInRect(array):
        a = (array[1]-array[0])*1.0
        b = array[0]
        for i in range(2,array.size):
                y = a*i+b
                if y > (1+rectVul)*array[i] or y < (1-rectVul)*array[i]:
                        return 0
        return 1       

def findMaxMin(array):
        size = array.size
        a1 = array[0:size/5]
        a2 = array[size/5:2*size/5]
        a3 = array[2*size/5:3*size/5]
        a4 = array[3*size/5:4*size/5]
        a5 = array[4*size/5:size]
        min1 = a1.min()
        min2 = a2.min()
        min3 = a3.min()
        min4 = a4.min()
        min5 = a5.min()
        max1 = a1.max()
        max2 = a2.max()
        max3 = a3.max()
        max4 = a4.max()
        max5 = a5.max()
        x = [min1, min2, min3, min4, min5]
        x = asarray(x)
        for i in reversed(range(x.size)):
            y = asarray(list(combinations(x, i)))
            z = map(aInRect, asarray(list(combinations(x, i))))
            if max(z) == 1:
                return y[z.index(max(z))]
        
