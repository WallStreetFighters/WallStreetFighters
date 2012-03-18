# -*- coding: utf-8 -*-

import sys
import datetime
import operator
import os
from PyQt4 import QtGui, QtCore
import GUIModule.RSSgui as RSSgui
from GUIModule.Tab import AbstractTab
from ChartsModule.Chart import Chart
import DataParserModule.dataParser as dataParser

class GuiMainWindow(object):
    """Klasa odpowiedzialna za GUI głownego okna aplikacji"""
    def setupGui(self,MainWindow):
        """ustawianie komponetów GUI"""
        MainWindow.setObjectName("WallStreetFighters")
        MainWindow.resize(1000,700)

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

	"""Każde okno zakłaki tworzymy poprzez stworzenie obiektu klasy
	AbstractTab z modułu Tab w której zdefiniowane są wspólne komponenty
	dla każdej zakładki.
	AbstractTab.optionsFrame
            AbstractTab.optionsFrame.chartButton
	"""
        #tabs - przechowywanie zakładek
	self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.tabs = QtGui.QTabWidget(self.centralWidget)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 980, 640))
        self.tabs.setObjectName("Tabs")

        #załadowanie List
        dataParser.loadData()

        # inicjujemy model danych dla Index
        indexModel = self.ListModel(list=dataParser.INDEX_LIST)
        # inicjujemy model danych dla Stock
        stockModel = self.ListModel(list=dataParser.STOCK_LIST)
        # inicjujemy model danych dla Forex
        forexModel = self.ListModel(list=dataParser.FOREX_LIST)

        """tab A wskaźniki i oscylatory"""
        
	self.tabA = AbstractTab()
        self.tabA.setObjectName("tabA")

        #ustawiamy modele danych 
        self.tabA.indexListView.setModel(indexModel)
        self.tabA.stockListView.setModel(stockModel)
        self.tabA.forexListView.setModel(forexModel)
        
        
        self.idicatorsLabel = QtGui.QLabel('Indicators:',self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.idicatorsLabel)
        #check box dla wskaźnika momentum
        self.tabA.momentumCheckBox = QtGui.QCheckBox("Momentum",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.momentumCheckBox)
        #check box dla ROC
        self.tabA.rocCheckBox = QtGui.QCheckBox("ROC",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.rocCheckBox)
        #check box dla SMA
        self.tabA.smaCheckBox = QtGui.QCheckBox("SMA",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.smaCheckBox)
        #check box dla EMA
        self.tabA.emaCheckBox = QtGui.QCheckBox("EMA",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.emaCheckBox)
        #check box dla CCI
        self.tabA.cciCheckBox = QtGui.QCheckBox("CCI",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.cciCheckBox)
        #check box dla RSI
        self.tabA.rsiCheckBox = QtGui.QCheckBox("RSI",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.rsiCheckBox)
        #check box dla Williams Oscilator
        self.tabA.williamsOscilatorCheckBox = QtGui.QCheckBox("Williams Oscilator",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.williamsOscilatorCheckBox)    
        #(przyciski dodajemy na sam koniec okna)wyswietlanie wykresu
        self.tabA.addChartButton()
        self.tabA.chartButton.clicked.connect(self.paintChart)
        self.tabs.addTab(self.tabA,"tabA")
        """koniec tab A """
        
        """ tab B"""
        self.tabB = AbstractTab()
        self.tabB.setObjectName("tabB")

        #przycisk wyswietlanie wykresu (przyciski dodajemy na sam koniec okna)
        self.tabB.addChartButton()
        
        
        self.tabs.addTab(self.tabB,"tabB")
        
        self.tabs.addTab(self.tabB,"tabB")
        """ koniec tab B"""

        """" tabC """
        self.tabC = AbstractTab()
        self.tabC.setObjectName("tabC")
        self.tabs.addTab(self.tabC,"tabC")
        self.tabC.addChartButton()
        self.tabs.addTab(self.tabC,"tabC")
        
        """Koniec tabC"""
        """ Rss tab"""
        self.RSSTab = QtGui.QWidget()
        self.tabs.addTab(self.RSSTab,"RSS")
        self.rssWidget = RSSgui.RSSWidget(self.RSSTab)
        self.tabB.chartsLayout.addWidget(self.rssWidget)
        self.verticalLayout2 = QtGui.QVBoxLayout(self.RSSTab)
        self.verticalLayout2.addWidget(self.rssWidget)
    
	""" koniec ustawiania Zakładek"""

	
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralWidget)

				
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

      

    """ Modele przechowywania listy dla poszczególnych instrumentów finansowych"""
    class ListModel(QtCore.QAbstractTableModel):
        def __init__(self,list, parent = None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self.list = list
            self.headerdata = ['symbol', 'name', '']
            print len(self.list)
            print len(self.list[0])            
        
        def rowCount(self, parent):
            return len(self.list)
        def columnCount(self,parent):
            return 2
        def headerData(self, col, orientation, role):
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self.headerdata[col])
            return QtCore.QVariant()
        
        def data(self, index, role):
            if not index.isValid():
                return QtCore.QVariant()
            elif role != QtCore.Qt.DisplayRole:
                return QtCore.QVariant()
            return QtCore.QVariant(self.list[index.row()][index.column()])
        
        def sort(self, Ncol, order):
            """Sort table by given column number.
            """
            self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
            self.list = sorted(self.list, key=operator.itemgetter(Ncol))        
            if order == QtCore.Qt.DescendingOrder:
                self.list.reverse()
            self.emit(QtCore.SIGNAL("layoutChanged()"))
        

    def paintChart(self):

        self.tabA.chartsLayout.removeWidget(chart)
        pageIndex = self.tabA.listsToolBox.currentIndex() #sprawdzamy z jakiej listy korzystamy
        dateStart = self.tabA.startDateEdit.date()  # początek daty
        start = datetime.datetime(dateStart.year(),dateStart.month(),dateStart.day())
        
        dateEnd = self.tabA.startDateEdit.date()     # koniec daty
        end = datetime.datetime(dateEnd.year(),dateEnd.month(),dateEnd.day())

        indicator = 'momentum'
        if self.tabA.momentumCheckBox.isChecked():
            indicator = "momentum"
        elif self.tabA.smaCheckBox.isChecked():
            indicator = "SMA"
        elif self.tabA.emaCheckBox.isChecked():
            indicator = "EMA"
        #step
        step = self.tabA.stepComboBox.currentText()

        #chartType
        chartType = self.tabA.chartTypeComboBox.currentText()
        hideVolumen =self.tabA.volumenCheckBox.isChecked() 
        #painting
        painting = self.tabA.paintCheckBox.isChecked()
        
        
        # Jeśli wybrano instrument Index
        if pageIndex == 0:
            indexes = self.tabA.indexListView.selectedIndexes()
            index= indexes[0].row()
            finObj = dataParser.createWithCurrentValueFromYahoo(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3])
            finObj.updateArchive()
            chart = Chart(self.tabA, finObj)
            self.tabA.chartsLayout.addWidget(chart)
            chart.setOscPlot('momentum')
            chart.setDrawingMode(True)
            chart.setData(finObj,dateStart,dateEnd,'weekly')
            chart.setMainType('candlestick')        
            chart.setData(finObj)
            chart.setMainIndicator('SMA')
            chart.rmVolumeBars()
            chart.setData(finObj,datetime.datetime(2003,7,10),datetime.datetime(2004,2,2),'daily')
            chart.setMainIndicator('EMA')
        # Jeśli wybrano instrument Stock
        if pageIndex == 1:
            indexes = self.tabA.stockListView.selectedIndexes()
            index= indexes[0].row()
            finObj = dataParser.createWithCurrentValueFromYahoo(dataParser.STOCK_LIST[index][1],dataParser.STOCK_LIST[index][0],'stock',dataParser.STOCK_LIST[index][3])
            finObj.updateArchive()
            chart = Chart(self.tabA, finObj)
            self.tabA.chartsLayout.addWidget(chart)
            chart.setDrawingMode(painting)
            chart.setData(finObj,datetime.datetime(2003,7,10),datetime.datetime(2004,2,2),step)
            chart.setMainType(chartType)
            if hideVolumen:
                chart.rmVolumen()
            
       

        
            
            

        
       

        
