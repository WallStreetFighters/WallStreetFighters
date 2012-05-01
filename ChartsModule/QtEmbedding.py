# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
from CompareChart import CompareChart
from LightweightChart import LightweightChart
from TechAnalysisModule.candles import *
from TechAnalysisModule.trendAnalysis import *
from TechAnalysisModule.oscilators import *
import WallStreetFighters.DataParserModule.dataParser as parser
import sys
import os
import datetime
import time

class ApplicationWindow(QtGui.QMainWindow):
    """Klasa demonstrująca jak przykładowo można osadzić wykres w Qt."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        parser.loadData()         
        finObj1 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[71][1],
        parser.STOCK_LIST[71][0],'stock',parser.STOCK_LIST[71][3])         
        finObj1.updateArchive('daily')         
        chart = Chart(self.main_widget,finObj1)                
        chart.setData(finObj1,datetime.datetime(2008,11,1),datetime.datetime(2011,3,22),'daily')                                   
        l.addWidget(chart)                             
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)            
        self.setWindowTitle("Wykresik")        
        self.show()        
        chart.setMainType('candlestick')
        

class ApplicationWindow1(QtGui.QMainWindow):
    """Klasa demonstrująca jak przykładowo można osadzić wykres w Qt."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        parser.loadData()         
        print "ściągam";
        zajebisteDane=parser.getAdvDecInPeriodOfTime(datetime.date(2003,7,10),datetime.date(2004,2,2),'NYSE')
        print "ściągłem";
        dates=zajebisteDane['date']
        values=adLine(zajebisteDane['adv'], zajebisteDane['dec'])
        #values=mcClellanOscillator(zajebisteDane['adv'], zajebisteDane['dec'])        
        #values=TRIN(zajebisteDane['adv'], zajebisteDane['dec'], zajebisteDane['advv'], zajebisteDane['decv'])
        print "rysuje";
        zajebistyWykres = LightweightChart(self.main_widget,dates,values,'A/D line')                        
        l.addWidget(zajebistyWykres)                        
        print "narysłem";
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)                
        self.show()

        
qApp = QtGui.QApplication(sys.argv)
print os.getcwd()
os.chdir("..") #zmieniamy katalog roboczy żeby pliki .wsf się ładowały

aw = ApplicationWindow()
sys.exit(qApp.exec_())




