 # coding: utf-8
__author__="Andrzej Smoliński"
__date__ ="$2012-02-23 19:00:48$"

import datetime
import random
import matplotlib.dates as mdates
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4 import QtGui

class Data:
    """To w założeniu będzie jakaś zewnętrzna klasa, z której będe pobierał dane
    stworzyłem pustą tylko po to żeby się nie sypało przy odwołaniach do niej"""
    def __init__(self):
        self.close=[]
        self.date=[]
        self.volume=[]        
        self.indicTest=[]        
        self.oscTest=np.sin(0.25*np.arange(100))       
        self.ticker="XYZ"
        date = datetime.datetime(2010, 12, 01)        
        step = datetime.timedelta(days=1)
        #step = datetime.timedelta(hours=1)
        for i in range(100):
            self.date.append(date)
            self.close.append(random.random())
            self.volume.append(random.random())            
            self.indicTest.append(random.random())
            date+=step                

class Chart(FigureCanvas):
    """Klasa (widget Qt) odpowiedzialna za rysowanie wykresu. Zgodnie z tym, co zasugerował
    Paweł, na jednym wykresie wyświetlam jeden wskaźnik i jeden oscylator, a jak ktoś
    będzie chciał więcej, to kliknie sobie jakiś guzik, który mu pootwiera kilka wykresów
    w nowym oknie."""
    
    data = None  #obiekt przechowujący dane
    
    fig = None #rysowany wykres (tzn. obiekt klasy Figure)
    mainPlot = None #główny wykres (punktowy, liniowy, świecowy)        
    volumeBars = None #wykres wolumenu
    oscPlot = None #wykres oscylatora
    
    mainType = None #typ głównego wykresu
    oscType = None #typ oscylatora (RSI, momentum, ...)
    mainIndicator = None #typ wskaźnika rysowany dodatkowo na głównym wykresie (średnia krocząca, ...)
    
    #margines (pionowy i poziomy oraz maksymalna wysokość/szerokość wykresu)
    margin, maxSize = 0.05, 0.9     
    #wysokość wolumenu i wykresu oscylatora
    volHeight, oscHeight = 0.1, 0.15    
    
    def __init__(self, parent=None, data=Data(), width=8, height=6, dpi=100):
        """Konstruktor. Tworzy domyślny wykres (liniowy z wolumenem, bez wskaźników)
        dla podanych danych. Domyślny rozmiar to 800x600 pixli"""                        
        
        self.data=data
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
           
    def setData(self, data):
        """Ustawiamy model danych, który ma reprezentować wykres. Zakładam, że
            będzie istnieć jedna klasa, z której będę mógł pobrać dane podstawowe
            oraz wszystkie wskaźniki dla tych danych"""
        self.data=data
        #w zaleznosci od horyzontu czasoweg formatujemy osie czasu        
        self.updatePlot()
        
    def setMainType(self, type):
        """Ustawiamy typ głównego wykresu ('point','line','candle','none')"""
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
        ax=self.mainPlot                
        ax.clear()
        if self.mainType=='line' :
            ax.plot(self.data.date,self.data.close,'b-',label=self.data.ticker)
        elif self.mainType=='point':
            ax.plot(self.data.date,self.data.close,'b.',label=self.data.ticker)
        elif self.mainType=='candle':
            self.drawCandlePlot()
        else:            
            return
        if self.mainIndicator != None:
            self.updateMainIndicator()       
        #legenda
        leg = ax.legend(loc='best', fancybox=True)
        leg.get_frame().set_alpha(0.5)
        self.formatDateAxis(self.mainPlot)
    
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
        
    def updateVolumeBars(self):
        """Odświeża rysowanie wolumenu"""
        self.volumeBars.vlines(self.data.date,0,self.data.volume)
        self.formatDateAxis(self.volumeBars)
        
    def drawCandlePlot(self):
        """To będzie wyświetlać (wkrótce) główny wykres jako świecowy"""
        pass
    
    def setMainIndicator(self, type):
        """Ustawiamy, jaki wskaźnik chcemy wyświetlać na głównym wykresie"""
        self.mainIndicator=type        
        self.updateMainPlot()
    
    def updateMainIndicator(self):
        """Odrysowuje wskaźnik na głównym wykresie"""
        ax=self.mainPlot
        type=self.mainIndicator
        ax.hold(True) #hold on
        if type=='Test':
            indicValues=self.data.indicTest
        elif type=='SMA':
            pass        
        # ....  
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
        if type == 'Test':
            oscData=self.data.oscTest
        elif type == 'RSI':
            pass        
        # ..... 
        else:
            ax.hold(False)
            return
        ax.plot(self.data.date,oscData,'g-',label=type)
        #legenda
        leg = ax.legend(loc='best', fancybox=True)
        leg.get_frame().set_alpha(0.5)
        self.formatDateAxis(self.oscPlot)
        

    def formatDateAxis(self,ax):
        """Formatuje etykiety osi czasu"""
        mindate=self.data.date[0].date()
        maxdate=self.data.date[-1].date()
        #dwie pozyższe linie to PROWIZORKA, korzystam ze zwykłej listy a nie numPy array
        #jeśli horyzont czasowy jest krótszy niż 7 dni, wyświetlamy z godzinami
        if((maxdate-mindate).days < 7):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in ax.get_xticklabels():
            label.set_size(8)            
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
        elif self.volumeBars.get_visible():
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
            
def getBoundsAsRect(axes):
    """Funkcja pomocnicza do pobrania wymiarów wykresu w formie prostokąta,
        tzn. tablicy."""
    bounds=axes.get_position().get_points()
    left=bounds[0][0]
    bottom=bounds[0][1]
    width=bounds[1][0]-left
    height=bounds[1][0]-bottom
    return [left, bottom, width, height]