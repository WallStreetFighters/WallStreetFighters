# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
from CompareChart import CompareChart
from TechAnalysisModule.candles import *
import WallStreetFighters.DataParserModule.dataParser as parser
import sys
import os
import datetime
import time

formation=None

class ApplicationWindow(QtGui.QMainWindow):
    """Klasa demonstrująca jak przykładowo można osadzić wykres w Qt."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        parser.loadData()         

        finObj1 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[50][1],
        parser.STOCK_LIST[50][0],'stock',parser.STOCK_LIST[50][3])         
        finObj1.updateArchive('daily')         
        chart = Chart(self.main_widget,finObj1)
        chart.setData(finObj1,datetime.datetime(2009,10,1),datetime.datetime(2010,2,1),'daily')                
        chart.setScaleType('log')
        chart.setMainType('candlestick')        
        l.addWidget(chart)                                      
        form1=findCandleFormations(chart.data.open,chart.data.high,chart.data.low,chart.data.close,'falling')
        form2=findCandleFormations(chart.data.open,chart.data.high,chart.data.low,chart.data.close,'rising')
        print form1
        print form2
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)            
        self.setWindowTitle("Wykresik")
        self.show()
        for formation in form1+form2:
            chart.drawLine(formation[1],chart.data.low[formation[1]],
                            formation[2],chart.data.low[formation[1]])                        
        
qApp = QtGui.QApplication(sys.argv)
print os.getcwd()
os.chdir("..") #zmieniamy katalog roboczy żeby pliki .wsf się ładowały

aw = ApplicationWindow()
sys.exit(qApp.exec_())




