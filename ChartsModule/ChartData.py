# coding: utf-8
__author__="Andrzej Smoliński"
__date__ ="$2012-03-24 12:05:55$"

import datetime
import matplotlib.dates as mdates
import numpy as np
import TechAnalysisModule.oscilators as indicators

class ChartData:
    """Ta klasa służy mi jako pomost pomiędzy tym, czego potrzebuje wykres, a tym
    co daje mi FinancialObject Marcina"""     
    
    def __init__(self, finObj, start=None, end=None, step='monthly'):
        if start>=end:
            self.corrupted=True
            return
        self.step=(step)
        #odwracamy tabelę, bo getArray() zwraca ją od dupy strony
        if(start==None):
            start=datetime.datetime.strptime(finObj.getArray(step)['date'][-1],"%Y-%m-%d")
        if(end==None):
            end=datetime.datetime.strptime(finObj.getArray(step)['date'][0],"%Y-%m-%d")        
        indexes=finObj.getIndex(start.date(),end.date(),step)
        #potrzebujemy też pełnej tabeli do obliczania wskaźników
        self.fullArray=finObj.getArray(step)[::-1]
        dataArray=finObj.getArray(step)[indexes[1]:indexes[0]:-1]
        if(len(self.fullArray)==0 or len(dataArray)==0):
            self.corrupted=True
            return
        self.name=finObj.name
        self.open=dataArray['open'].tolist()
        self.close=dataArray['close'].tolist()
        self.low=dataArray['low'].tolist()
        self.high=dataArray['high'].tolist()
        self.volume=dataArray['open'].tolist()        
        self.date = []                    
        for date in dataArray['date']:
            self.date.append(datetime.datetime.strptime(date,"%Y-%m-%d"))        
        #dane w formacie dla candlesticka
        self.quotes=[]
        for i in range(len(dataArray)):
            time=float(i)
            open=self.open[i]
            close=self.close[i]
            high=self.high[i]
            low=self.low[i]
            self.quotes.append((time, open, close, high, low))
        self.corrupted=False
    
    def getEarlierValues(self, length, type='close'):
        """Funkcja używana do wskaźników, które potrzebują wartości z okresu
        wcześniejszego niż dany okres (czyli chyba do wszystkich). Jeśli wcześniejsze
        wartości istnieją, są one pobierane z tablicy self.fullArray. W przeciwnym wypadku
        kopiujemy wartość początkową na wcześniejsze wartości.
        length = ilość dodatkowych wartości, które potrzebujemy"""
        if(type=='open'):
            array=self.open[:]
        elif(type=='close'):
            array=self.open[:]
        elif(type=='high'):
            array=self.high[:]
        elif(type=='low'):
            array=self.low[:]
        else:
            return None
        startIdx=self.fullArray['date'].tolist().index(self.date[0].strftime("%Y-%m-%d"))
        first=array[0]
        if(startIdx-length < 0):
            for i in range (length-startIdx):
                array.insert(0,first)            
            for i in range (startIdx):
                array.insert(0,self.fullArray[type][i])                                
        else:
            for i in range (length):
                array.insert(0,self.fullArray[type][startIdx-length+i])
        return array
    
    def momentum(self, duration=10):
        array=self.getEarlierValues(duration)
        return indicators.momentum(np.array(array), duration)
    
    def RSI(self, duration=10):
        array=self.getEarlierValues(duration)        
        return indicators.RSI(np.array(array), duration)
    
    def CCI(self, duration=10):
        highs=np.array(self.getEarlierValues(duration-1,'high'))
        lows=np.array(self.getEarlierValues(duration-1,'low'))
        closes=np.array(self.getEarlierValues(duration-1,'close'))        
        return indicators.CCI(closes,lows,highs,duration)        
    
    def ROC(self, duration=10):
        array=self.getEarlierValues(duration)
        return indicators.ROC(np.array(array), duration)
    
    def williams(self, duration=10):
        highs=np.array(self.getEarlierValues(duration,'high'))
        lows=np.array(self.getEarlierValues(duration,'low'))
        closes=np.array(self.getEarlierValues(duration,'close'))        
        return indicators.williamsOscilator(highs,lows,closes,duration)
    
    def SMA(self, duration=20):        
        array=self.getEarlierValues(len(self.close))        
        return indicators.movingAverage(np.array(array),duration,1)
    
    def WMA(self, duration=20):
        array=self.getEarlierValues(len(self.close))
        return indicators.movingAverage(np.array(array),duration,2)
    
    def EMA(self, duration=20):
        array=self.getEarlierValues(len(self.close))
        return indicators.movingAverage(np.array(array),duration,3)
    
    def bollingerUpper(self, duration=20):
        array=self.getEarlierValues(len(self.close))
        print len(array)
        print len(indicators.bollingerBands(np.array(array),duration,2,2))
        return indicators.bollingerBands(np.array(array),duration,1,2)
    
    def bollingerLower(self, duration=20):
        array=self.getEarlierValues(len(self.close))        
        return indicators.bollingerBands(np.array(array),duration,2,2)    
