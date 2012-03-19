# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
import WallStreetFighters.DataParserModule.dataParser as parser
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

        finObj = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[2][1],
        parser.STOCK_LIST[2][0],'stock',parser.STOCK_LIST[2][3]) 
        finObj.updateArchive() 
        chart = Chart(self.main_widget, finObj)                
        l.addWidget(chart)                        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        chart.setOscPlot('RSI')
        chart.setDrawingMode(True)
        #50% spadku jednego dnia - fajnie wskaźniki głupieją :)
        chart.setData(finObj,datetime.datetime(2005,2,1),datetime.datetime(2005,4,1),'daily') 
        chart.setMainIndicator('bollinger')
        chart.setMainType('candlestick')                        
        
qApp = QtGui.QApplication(sys.argv)
os.chdir("../DataParserModule") #zmieniamy katalog roboczy żeby pliki .wsf się ładowały

aw = ApplicationWindow()
aw.setWindowTitle("Wykresik")
aw.show()
sys.exit(qApp.exec_())




