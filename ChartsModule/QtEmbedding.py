# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
from CompareChart import CompareChart
from LightweightChart import LightweightChart
import WallStreetFighters.DataParserModule.dataParser as parser
import TechAnalysisModule.oscilators as indicators
import sys
import os
import datetime

class ApplicationWindow(QtGui.QMainWindow):
    """Klasa demonstrująca jak przykładowo można osadzić wykres w Qt."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        parser.loadData()         

        finObj1 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[2][1],
        parser.STOCK_LIST[2][0],'stock',parser.STOCK_LIST[2][3]) 
        finObj2 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[6][1],
        parser.STOCK_LIST[6][0],'stock',parser.STOCK_LIST[6][3]) 
        finObj3 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[12][1],
        parser.STOCK_LIST[12][0],'stock',parser.STOCK_LIST[12][3]) 
        finObj4 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[16][1],
        parser.STOCK_LIST[16][0],'stock',parser.STOCK_LIST[16][3]) 
        finObj1.updateArchive('daily') 
        finObj2.updateArchive('daily') 
        finObj3.updateArchive('daily')
        finObj4.updateArchive('daily')
        chart = CompareChart(self.main_widget)                
        chart.setData([finObj1, finObj2, finObj3, finObj4],
                    datetime.datetime(2011,8,1),datetime.datetime(2012,3,1),'daily')
        chart.setScaleType('log')
        l.addWidget(chart)                        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)                

class ApplicationWindow1(QtGui.QMainWindow):
    """Klasa demonstrująca jak przykładowo można osadzić wykres w Qt."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        parser.loadData()         
        zajebisteDane=parser.getAdvDecInPeriodOfTime(datetime.date(2003,7,10),datetime.date(2004,2,2),'NYSE')
        dates=zajebisteDane['date']
        values=indicators.adLine(zajebisteDane['adv'], zajebisteDane['dec'])
        #values=indicators.mcClellanOscillator(zajebisteDane['adv'], zajebisteDane['dec'])        
        #values=indicators.TRIN(zajebisteDane['adv'], zajebisteDane['dec'], zajebisteDane['advv'], zajebisteDane['decv'])
        zajebistyWykres = LightweightChart(self.main_widget,dates,values,'A/D line')                        
        l.addWidget(zajebistyWykres)                        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)                
        
qApp = QtGui.QApplication(sys.argv)

os.chdir("..") #zmieniamy katalog roboczy żeby pliki .wsf się ładowały

aw = ApplicationWindow()
aw.setWindowTitle("Wykresik Porównawczy")
aw.show()

aw1 = ApplicationWindow1()
aw1.setWindowTitle("Wykresik Lekki")
aw1.show()
sys.exit(qApp.exec_())




