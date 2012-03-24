# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
from CompareChart import CompareChart
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

        finObj1 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[2][1],
        parser.STOCK_LIST[2][0],'stock',parser.STOCK_LIST[2][3]) 
        finObj2 = parser.createWithCurrentValueFromYahoo(parser.STOCK_LIST[6][1],
        parser.STOCK_LIST[6][0],'stock',parser.STOCK_LIST[6][3]) 
        finObj1.updateArchive() 
        finObj2.updateArchive() 
        chart = CompareChart(self.main_widget, finObj1, finObj2)                
        chart.setData(finObj1,finObj2,datetime.datetime(2011,8,1),datetime.datetime(2012,3,1),'daily')
        l.addWidget(chart)                        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)                
        
qApp = QtGui.QApplication(sys.argv)
os.chdir("../DataParserModule") #zmieniamy katalog roboczy żeby pliki .wsf się ładowały

aw = ApplicationWindow()
aw.setWindowTitle("Wykresik")
aw.show()
sys.exit(qApp.exec_())




