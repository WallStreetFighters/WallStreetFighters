 # coding: utf-8
__author__="Andrzej Smoliński"
__date__ ="$2012-02-23 19:00:48$"

import datetime
import random
import matplotlib.dates as mdates
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
        date = datetime.datetime(2010, 12, 01)        
        step = datetime.timedelta(days=1)
        #step = datetime.timedelta(hours=1)
        for i in range(100):
            self.date.append(date)
            self.close.append(random.random())
            self.volume.append(random.random())
            date+=step                

class Chart(FigureCanvas):
    """Klasa (widget Qt) odpowiedzialna za rysowanie wykresu"""
    
    data = None  #obiekt przechowujący dane
    fig = None #rysowany wykres (tzn. obiekt klasy Figure)
    mainPlot = None #główny wykres (punktowy, liniowy, świecowy)    
    mainType = None #typ głównego wykresu
    volumeBars = None #wykres wolumenu
    #secPlots = None tablica przechowująca (max 3, choć to do ustelenia) wykresy wskaźników
    
    #margines (pionowy i poziomy oraz maksymalna wysokość/szerokość wykresu)
    margin, maxSize = 0.05, 0.9     
    #wysokość wolumenu i wykresów dolnych
    volHeight, secHeight = 0.1, 0.15    
    
    def __init__(self, parent=None, data=Data(), width=8, height=6, dpi=100):
        """Konstruktor. Tworzy domyślny wykres (liniowy z wolumenem, bez wskaźników)
        dla podanych danych. Domyślny rozmiar to 800x600 pixli"""                        
        
        self.data=data
        self.mainType='line'
        self.withVolume=True
        self.secPlots=[]
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
        self.updatePlot()
        
    def setMainType(self, type):
        """Ustawiamy typ głównego wykresu ('point','line','candle','none')"""
        self.mainType=type
        self.updateMainPlot()
        
    def updatePlot(self):
        """Odświeża wszystkie wykresy"""
        self.updateMainPlot()
        self.updateVolumeBars()
        #tu będzie jeszcze odświeżenie wskaźników
        pass
    
    def addMainPlot(self):
        """Rysowanie głównego wykresu (tzn. kurs w czasie)"""                                            
        bounds=[self.margin, self.margin, self.maxSize, self.maxSize]
        self.mainPlot=self.fig.add_axes(bounds)                
        self.formatDateAxis(self.mainPlot)        
        self.updateMainPlot()
    
    def updateMainPlot(self):
        ax=self.mainPlot
        if self.mainType=='line' :
            ax.plot(self.data.date,self.data.close,'b-')
        elif self.mainType=='point':
            ax.plot(self.data.date,self.data.close,'b.')
        elif self.mainType=='candle':
            self.drawCandlePlot()
        else:
            ax.clear()
    
    def addVolumeBars(self):
        """Rysowanie wykresu wolumenu"""
        #najpierw kurczymy główny wykres
        bounds=getBoundsAsRect(self.mainPlot)
        self.mainPlot.set_position([bounds[0],bounds[1]+self.volHeight,
                                    bounds[2],bounds[3]-self.volHeight])
        volBounds=[self.margin, self.margin , 
                    self.maxSize , self.volHeight]
        self.volumeBars=self.fig.add_axes(volBounds, sharex=self.mainPlot)                    
        #usuwamy etykiety y dla wolumenu (zakomentujcie, to zobaczycie czemu)
        for label in self.volumeBars.get_yticklabels():
            label.set_visible(False)                    
        #usuwamy etykiety pod głównym wykresem (żeby były tylko pod wolumenem)
        for label in self.mainPlot.get_xticklabels():
            label.set_visible(False)
        self.formatDateAxis(self.volumeBars)           
        self.updateVolumeBars()
        self.volumeBars.set_visible(True)
    
    def rmVolumeBars(self):
        """Usuwa wykres wolumenu"""
        if self.volumeBars==None:
            return
        self.volumeBars.set_visible(False)
        bounds=getBoundsAsRect(self.mainPlot)
        self.mainPlot.set_position([bounds[0],bounds[1]-self.volHeight,
                                    bounds[2],bounds[3]+self.volHeight])        
        
    def updateVolumeBars(self):
        """Odświeża rysowanie wolumenu"""
        self.volumeBars.vlines(self.data.date,0,self.data.volume)
        
    def drawCandlePlot(self):
        """To będzie wyświetlać (wkrótce) główny wykres jako świecowy"""
        pass
    
    def setSecPlot(self, i, type):
        """Wyświetla na i-tej pozycji pod głównym wykresem wykres poboczny danego typu"""
        pass
    
    def rmSecPlot(self, i):
        """Usuwa i-ty z wykresów pobocznych"""
        pass

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
            #label.set_rotation(30)
            label.set_horizontalalignment('center')            
            
def getBoundsAsRect(axes):
    """Funkcja pomocnicza do pobrania wymiarów wykresu w formie prostokąta,
        tzn. tablicy."""
    bounds=axes.get_position().get_points()
    left=bounds[0][0]
    bottom=bounds[0][1]
    width=bounds[1][0]-left
    height=bounds[1][0]-bottom
    return [left, bottom, width, height]