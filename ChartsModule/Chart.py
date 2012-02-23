__author__="Andrzej Smoliński"
__date__ ="$2012-02-23 19:00:48$"

import numpy as np
import matplotlib.pyplot as plt

class Chart(FigureCanvas):
    """Klasa (widget Qt) odpowiedzialna za rysowanie wykresu"""
    
    configuration #jakaś tablica wyrażająca, które wskaźniki chcemy rysować etc.
    data #obiekt przechowujący dane
    
    def __init__(self):
        pass
    
    def setConfiguration(self, configuration):        
        pass
    
    def setData(self, data):
        """Ustawiamy model danych, który ma reprezentować wykres. Zakładam, że
            będzie istnieć jedna klasa, z której będę mógł pobrać dane podstawowe
            oraz wszystkie wskaźniki dla tych danych"""
        pass
        
    def drawPlot(self):
        """Tu się będzie odbywać właściwe rysowanie całości"""
        pass
    
    def drawMainPlot(self):
        """Rysowanie głównego wykresu (tzn. kurs w czasie)"""
        pass
    
    def drawVolumeBars(self):
        """Rysowanie wykresu wolumenu"""
        pass