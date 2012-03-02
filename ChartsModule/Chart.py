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
    pass

class Chart(FigureCanvas):
    """Klasa (widget Qt) odpowiedzialna za rysowanie wykresu"""
    
    #configuration - jakaś tablica wyrażająca, które wskaźniki chcemy rysować etc.
    #data - obiekt przechowujący dane
    #fig - rysowany wykres (obiekt klasy Figure)    
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        """Konstruktor. Domyślnie rozmiar to 800x600 pixli."""        
        
        #generujemy jakieś testowe dane    
        self.data=Data()
        self.data.close=[]
        self.data.date=[]
        self.data.volume=[]
        date = datetime.datetime(2010, 12, 01)        
        step = datetime.timedelta(days=1)
        for i in range(100):
            self.data.date.append(date)
            self.data.close.append(random.random())
            self.data.volume.append(random.random())
            date+=step
        
        self.configuration=['mainline','volume']
        self.fig = Figure(figsize=(width, height), dpi=dpi)        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)             
    
    def setConfiguration(self, configuration):        
        self.configuration=configuration
        pass
    
    def setData(self, data):
        """Ustawiamy model danych, który ma reprezentować wykres. Zakładam, że
            będzie istnieć jedna klasa, z której będę mógł pobrać dane podstawowe
            oraz wszystkie wskaźniki dla tych danych"""
        self.data=data            
        
    def drawPlot(self):
        """Tu się będzie odbywać właściwe rysowanie całości"""                
        #główny wykres        
        self.drawMainPlot()            
        #wskaźniki
        self.drawSecPlot()                
    
    def drawMainPlot(self):
        """Rysowanie głównego wykresu (tzn. kurs w czasie)"""
        rect=[0.05, 0.45, 0.9, 0.45]     #lewo, dół, szer, wys
        ax=self.mainPlot=self.fig.add_axes(rect)        
        if 'mainline' in self.configuration:
            ax.plot(self.data.date,self.data.close,'b-')
        elif 'mainpoint' in self.configuration:
            ax.plot(self.data.date,self.data.close,'b.')
        elif 'maincandle' in self.configuration:
            pass
        else:
            ax.clear()                    
        if('volume' in self.configuration):
            self.drawVolumeBars()
        else:
            self.formatDateAxis(ax)            
    
    def drawVolumeBars(self):
        """Rysowanie wykresu wolumenu"""
        rect=[0.05, 0.35, 0.9, 0.1]
        ax=self.fig.add_axes(rect, sharex=self.mainPlot)
        ax.vlines(self.data.date,0,self.data.volume)                    
        for label in ax.get_yticklabels():
            label.set_visible(False)        
        for label in self.mainPlot.get_xticklabels():
            label.set_visible(False)
        self.formatDateAxis(ax)
        pass
        
    def drawSecPlot(self):
        pass

    def formatDateAxis(self,ax):
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in ax.get_xticklabels():
            label.set_size(8)
            label.set_rotation(30)
            label.set_horizontalalignment('right')