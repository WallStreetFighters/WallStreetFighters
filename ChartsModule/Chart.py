 # coding: utf-8
__author__="Andrzej Smoliński"
__date__ ="$2012-02-23 19:00:48$"

import datetime
import random
import matplotlib.dates as mdates
import numpy as np
import TechAnalysisModule.oscylatory as oscillators
import TechAnalysisModule.srednie as averages
import TechAnalysisModule.indexy as indexes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.finance import candlestick
from matplotlib.patches import Rectangle
from PyQt4 import QtGui
from matplotlib.lines import Line2D


class ChartData:
    """Ta klasa służy mi jako pomost pomiędzy tym, czego potrzebuje wykres, a tym
    co daje mi FinancialObject Marcina"""     
    
    def __init__(self, finObj, start=None, end=None, step='monthly'):
        #odwracamy tabelę, bo getArray() zwraca ją od dupy strony
        if(start==None):
            start=datetime.datetime.strptime(finObj.getArray(step)['date'][-1],"%Y-%m-%d")
        if(end==None):
            end=datetime.datetime.strptime(finObj.getArray(step)['date'][0],"%Y-%m-%d")        
        indexes=finObj.getIndex(start.date(),end.date(),step)
        #potrzebujemy też pełnej tabeli do obliczania wskaźników
        self.fullArray=finObj.getArray(step)[::-1]
        dataArray=finObj.getArray(step)[indexes[1]:indexes[0]:-1]        
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
            time=mdates.date2num(self.date[i])
            open=self.open[i]
            close=self.close[i]
            high=self.high[i]
            low=self.low[i]
            self.quotes.append((time, open, close, high, low))
    
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
        return oscillators.momentum(np.array(array), duration)
    
    def RSI(self, duration=10):
        array=self.getEarlierValues(duration)        
        return oscillators.RSI(np.array(array), duration)
    
    def CCI(self, duration=10):
        highs=np.array(self.getEarlierValues(duration-1,'high'))
        lows=np.array(self.getEarlierValues(duration-1,'low'))
        closes=np.array(self.getEarlierValues(duration-1,'close'))        
        return oscillators.CCI(closes,lows,highs,duration)        
    
    def ROC(self, duration=10):
        array=self.getEarlierValues(duration)
        return oscillators.ROC(np.array(array), duration)
    
    def williams(self, duration=10):
        highs=np.array(self.getEarlierValues(duration-3,'high'))
        lows=np.array(self.getEarlierValues(duration-3,'low'))
        closes=np.array(self.getEarlierValues(duration-3,'close'))        
        return oscillators.williamsOscilator(highs,lows,closes,duration)
    
    def SMA(self, duration=20):        
        array=self.getEarlierValues(len(self.close))
        return averages.movingAverage(np.array(array),duration,1)
    
    def WMA(self, duration=20):
        array=self.getEarlierValues(len(self.close))
        return averages.movingAverage(np.array(array),duration,2)
    
    def EMA(self, duration=20):
        array=self.getEarlierValues(len(self.close))
        return averages.movingAverage(np.array(array),duration,3)
    
    def bollingerUpper(self, duration=20):
        array=self.getEarlierValues(len(self.close))
        print len(array)
        print len(averages.bollingerBands(np.array(array),duration,2,2))
        return averages.bollingerBands(np.array(array),duration,1,2)
    
    def bollingerLower(self, duration=20):
        array=self.getEarlierValues(len(self.close))        
        return averages.bollingerBands(np.array(array),duration,2,2)
    
    

class Chart(FigureCanvas):
    """Klasa (widget Qt) odpowiedzialna za rysowanie wykresu. Zgodnie z tym, co zasugerował
    Paweł, na jednym wykresie wyświetlam jeden wskaźnik i jeden oscylator, a jak ktoś
    będzie chciał więcej, to kliknie sobie jakiś guzik, który mu pootwiera kilka wykresów
    w nowym oknie."""
    data = None #obiekt klasy Data przechowujący dane    
    
    fig = None #rysowany wykres (tzn. obiekt klasy Figure)
    mainPlot = None #główny wykres (punktowy, liniowy, świecowy)        
    volumeBars = None #wykres wolumenu
    oscPlot = None #wykres oscylatora    
    additionalLines = [] #lista linii narysowanych na wykresie (przez usera, albo przez wykrycie trendu)    
    
    mainType = None #typ głównego wykresu
    oscType = None #typ oscylatora (RSI, momentum, ...)
    mainIndicator = None #typ wskaźnika rysowany dodatkowo na głównym wykresie (średnia krocząca, ...)
    
    x0, y0 = None,None      #współrzędne początku linii        
    drawingMode = False #zakładam, że możliwość rysowania będzie można włączyć/wyłączyć        
    
    scaleType = 'linear' #rodzaj skali na osi y ('linear' lub 'log')                    
    
    #margines (pionowy i poziomy oraz maksymalna wysokość/szerokość wykresu)
    margin, maxSize = 0.05, 0.9     
    #wysokość wolumenu i wykresu oscylatora
    volHeight, oscHeight = 0.1, 0.15        
    
    def __init__(self, parent, finObj, width=8, height=6, dpi=100):
        """Konstruktor. Tworzy domyślny wykres (liniowy z wolumenem, bez wskaźników)
        dla podanych danych. Domyślny rozmiar to 800x600 pixli"""                        
        self.setData(finObj)
        self.mainType='line'                
        self.fig = Figure(figsize=(width, height), dpi=dpi)        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)        
        self.addMainPlot()
        self.addVolumeBars()                                        
        self.mpl_connect('button_press_event', self.onClick)        
           
    def setData(self, finObj, start=None, end=None, step='monthly'):
        """Ustawiamy model danych, który ma reprezentować wykres. Następnie
        konieczne jest jego ponowne odrysowanie"""        
        self.data=ChartData(finObj, start, end, step)        
        if(self.mainPlot!=None):
            self.updatePlot()
        
    def setMainType(self, type):
        """Ustawiamy typ głównego wykresu ('point','line','candlestick','none')"""
        self.mainType=type
        self.updateMainPlot()
        
    def updatePlot(self):
        """Odświeża wszystkie wykresy"""
        self.updateMainPlot()
        self.updateVolumeBars()
        self.updateOscPlot()        
        pass
    
    def addMainPlot(self):
        """Rysowanie głównego wykresu (tzn. kurs w czasie)"""                                            
        bounds=[self.margin, self.margin, self.maxSize, self.maxSize]
        self.mainPlot=self.fig.add_axes(bounds)                        
        self.updateMainPlot()
    
    def updateMainPlot(self):
        if(self.mainPlot==None):
            return
        ax=self.mainPlot                
        ax.clear()                        
        if self.mainType=='line' :
            ax.plot(self.data.date,self.data.close,'b-',label=self.data.name)
        elif self.mainType=='point':
            ax.plot(self.data.date,self.data.close,'b.',label=self.data.name)
        elif self.mainType=='candlestick':
            self.drawCandlePlot()
        else:            
            return
        if self.mainIndicator != None:
            self.updateMainIndicator()       
        ax.set_xlim(self.data.date[0],self.data.date[-1])
        ax.set_yscale(self.scaleType)
        #legenda
        leg = ax.legend(loc='best', fancybox=True)
        leg.get_frame().set_alpha(0.5)
        self.formatDateAxis(self.mainPlot)        
        self.fixLabels()
    
    def addVolumeBars(self):
        """Dodaje do wykresu wyświetlanie wolumenu."""        
        #tworzymy nowy wykres tylko za pierwszym razem, potem tylko pokazujemy i odświeżamy                
        if(self.volumeBars==None):
            volBounds=[self.margin, self.margin, self.maxSize, self.volHeight]
            self.volumeBars=self.fig.add_axes(volBounds, sharex=self.mainPlot)                    
            #usuwamy etykiety y dla wolumenu (zakomentujcie, to zobaczycie czemu)
            for label in self.volumeBars.get_yticklabels():
                label.set_visible(False)                                               
        self.updateVolumeBars()
        self.volumeBars.set_visible(True)
        self.fixPositions()
        self.fixLabels()
    
    def rmVolumeBars(self):
        """Ukrywa wykres wolumenu"""
        if self.volumeBars==None:
            return
        self.volumeBars.set_visible(False)        
        self.fixPositions()                            
        self.fixLabels()
    
    def setScaleType(self,type):    
        """Ustawia skalę liniową lub logarytmiczną na głównym wykresie.
        TODO dobrać podstawę logarytmu"""
        if(type) not in ['linear','log']:
            return        
        self.scaleType=type
        self.updateMainPlot()
        
    def updateVolumeBars(self):
        """Odświeża rysowanie wolumenu"""
        ax=self.volumeBars
        ax.clear()
        ax.vlines(self.data.date,0,self.data.volume)
        for label in self.volumeBars.get_yticklabels():
            label.set_visible(False)
        ax.set_xlim(self.data.date[0],self.data.date[-1])
        self.formatDateAxis(ax)
        self.fixLabels()
        
    def drawCandlePlot(self):
        """Wyświetla główny wykres w postaci świecowej"""    
        
        """candlestick potrzebuje danych w postaci piątek (time, open, close, high, low). 
        time musi być w postaci numerycznej (ilość dni od 0000-00-00 powiększona  o 1).         
        Atrybut width = szerokość świecy w ułamkach dnia na osi x. Czyli jeśli jedna świeca
        odpowiada za 1 dzień, to ustawiamy jej szerokość na ~0.7 żeby był jakiś margines między nimi"""
        timedelta=mdates.date2num(self.data.date[1])-mdates.date2num(self.data.date[0])        
        lines, patches = candlestick(self.mainPlot,self.data.quotes,
                                    width=0.7*timedelta,colorup='w',colordown='k')                
        #to po to żeby się wyświetlała legenda
        lines[0].set_label(self.data.name) 
        #poniższe dwie linie są po to, żeby wykres wypełniał całą szerokość
        self.mainPlot.xaxis_date()                
        self.mainPlot.autoscale_view()   
        """Ludzie, którzy robili tą bibliotekę byli tak genialni, że uniemożliwili
        stworzenie świec w najbardziej klasycznej postaci, tzn. białe=wzrost, czarne=spadek.
        Wynika to z tego, że prostokąty domyślnie nie mają obramowania i są rysowane POD liniami.
        Poniższy kod to naprawia"""
        for line in lines:                        
            line.set_zorder(line.get_zorder()-2)
        for rect in patches:                                    
            rect.update({'edgecolor':'k','linewidth':0.5})        
    
    def setMainIndicator(self, type):
        """Ustawiamy, jaki wskaźnik chcemy wyświetlać na głównym wykresie"""
        self.mainIndicator=type        
        self.updateMainPlot()
    
    def updateMainIndicator(self):
        """Odrysowuje wskaźnik na głównym wykresie"""
        ax=self.mainPlot
        type=self.mainIndicator
        ax.hold(True) #hold on        
        if type=='SMA':
            indicValues=self.data.SMA()        
        elif type=='WMA':
            indicValues=self.data.WMA()        
        elif type=='EMA':
            indicValues=self.data.EMA()        
        elif type=='bollinger':            
            ax.plot(self.data.date,self.data.bollingerUpper(),'r-',label=type)
            indicValues=self.data.bollingerLower()
        else:
            ax.hold(False)
            return
        ax.plot(self.data.date,indicValues,'r-',label=type)
        ax.hold(False) #hold off        
    
    def setOscPlot(self, type):
        """Dodaje pod głównym wykresem wykres oscylatora danego typu"""
        self.oscType=type                
        if self.oscPlot==None:
            oscBounds=[self.margin, self.margin, self.maxSize, self.oscHeight]
            self.oscPlot=self.fig.add_axes(oscBounds, sharex=self.mainPlot)                                            
        self.updateOscPlot()
        self.oscPlot.set_visible(True)
        self.fixPositions()
        self.fixLabels()
    
    def rmOscPlot(self):
        """Ukrywa wykres oscylatora"""
        if self.oscPlot==None:
            return
        self.oscPlot.set_visible(False)        
        self.fixPositions()                            
        self.fixLabels()
                                    
    def updateOscPlot(self):
        """Odrysowuje wykres oscylatora"""
        if self.oscPlot==None:
            return
        ax=self.oscPlot                
        type=self.oscType
        ax.clear()            
        if type == 'momentum':
            oscData=self.data.momentum()
        elif type == 'CCI':
            oscData=self.data.CCI()
        elif type == 'ROC':
            oscData=self.data.ROC()
        elif type == 'RSI':
            oscData=self.data.RSI()
        elif type == 'williams':
            oscData=self.data.williams()
        else:
            ax.hold(False)
            return
        ax.plot(self.data.date,oscData,'g-',label=type)
        ax.set_xlim(self.data.date[0],self.data.date[-1])
        #legenda
        leg = ax.legend(loc='best', fancybox=True)
        leg.get_frame().set_alpha(0.5)
        self.formatDateAxis(self.oscPlot)
        self.fixLabels()
        

    def formatDateAxis(self,ax):
        """Formatuje etykiety osi czasu"""
        mindate=self.data.date[0].date()
        maxdate=self.data.date[-1].date()        
        #jeśli horyzont czasowy jest krótszy niż 7 dni, wyświetlamy z godzinami
        if((maxdate-mindate).days < 7):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in ax.get_xticklabels():
            label.set_size(7)            
            label.set_horizontalalignment('center')                        
    
    def fixLabels(self):
        """Włącza wyświetlanie etykiet osi czasu pod odpowiednim (tzn. najniższym)
        wykresem, a usuwa w pozostałych"""
        #oscylator jest zawsze na samym dole
        if self.oscPlot!=None and self.oscPlot.get_visible():
            for label in self.mainPlot.get_xticklabels():
                label.set_visible(False)
            for label in self.volumeBars.get_xticklabels():
                label.set_visible(False)
            for label in self.oscPlot.get_xticklabels():
                label.set_visible(True)
        #jeśli nie ma oscylatora to pod wolumenem
        elif self.volumeBars!=None and self.volumeBars.get_visible():
            for label in self.mainPlot.get_xticklabels():
                label.set_visible(False)
            for label in self.volumeBars.get_xticklabels():
                label.set_visible(True)         
        #a jak jest tylko duży wykres to pod nim
        else:
            for label in self.mainPlot.get_xticklabels():
                label.set_visible(True)                        
    
    def fixPositions(self):
        """Dopasowuje wymiary i pozycje wykresów tak żeby zawsze wypełniały całą
        przestrzeń. Główny wykres puchnie albo się kurczy, a wolumen i oscylator 
        przesuwają się w górę lub dół."""
        #na początek wszystko spychamy na sam dół
        mainBounds=[self.margin, self.margin, self.maxSize, self.maxSize]
        volBounds=[self.margin, self.margin, self.maxSize, self.volHeight]
        oscBounds=[self.margin, self.margin, self.maxSize, self.oscHeight]
        #oscylator wypycha wolumen w górę i kurczy maina
        if self.oscPlot!=None and self.oscPlot.get_visible():
            mainBounds[1]+=self.oscHeight
            mainBounds[3]-=self.oscHeight
            volBounds[1]+=self.oscHeight
            self.oscPlot.set_position(oscBounds)
        #wolumen kolejny raz kurczy maina
        if self.volumeBars.get_visible():                    
            mainBounds[1]+=self.volHeight
            mainBounds[3]-=self.volHeight
            self.volumeBars.set_position(volBounds)
        self.mainPlot.set_position(mainBounds)     
    
    def setDrawingMode(self, mode):
        """Włączamy (True) lub wyłączamy (False) tryb rysowania po wykresie"""
        self.drawingMode=mode            
        x0, y0 = None,None
    
    def drawLine(self, x0,y0,x1,y1):
        """Dodaje linię (trend) do wykresu."""
        newLine=Line2D([x0,x1],[y0,y1],color='k')                
        self.mainPlot.add_line(newLine)
        self.additionalLines.append(newLine)
        newLine.figure.draw_artist(newLine)                                        
        self.blit(self.mainPlot.bbox)    #blit to taki redraw
    
    def clearLines(self):
        """Usuwa wszystkie linie narysowane dodatkowo na wykresie (tzn. nie kurs i nie wskaźniki)"""
        for line in self.additionalLines:            
            line.remove()
        self.additionalLines = []
        self.draw()
        self.blit(self.mainPlot.bbox)

    def onClick(self, event):
        """Rysujemy linię pomiędzy dwoma kolejnymi kliknięciami. Później to będzie 
        pewnie mniej biedne (z podglądem na żywo), ale pół dnia siedziałem żeby to
        gówno w ogóle zadziałało."""        
        if self.drawingMode==False:
            return
        if event.button==3: #nie no kurwa, RMB to tutaj button 3 -_-
            self.clearLines()            
        elif event.button==1:
            if self.x0==None or self.y0==None :
                self.x0, self.y0 = event.xdata, event.ydata
                self.firstPoint=True
            else:
                x1, y1 = event.xdata, event.ydata        
                self.drawLine(self.x0,self.y0,x1,y1)                
                self.x0, self.y0 = None,None
            
def getBoundsAsRect(axes):
    """Funkcja pomocnicza do pobrania wymiarów wykresu w formie prostokąta,
        tzn. tablicy."""
    bounds=axes.get_position().get_points()
    left=bounds[0][0]
    bottom=bounds[0][1]
    width=bounds[1][0]-left
    height=bounds[1][0]-bottom
    return [left, bottom, width, height]