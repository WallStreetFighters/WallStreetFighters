# -*- coding: utf-8 -*-

import sys
import operator
from PyQt4 import QtGui, QtCore
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
        
        # set horizontal header properties
        hh = self.tabA.indexListView.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.tabA.indexListView.resizeColumnsToContents()

        self.idicatorsLabel = QtGui.QLabel('Indicators:',self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.idicatorsLabel)
        #check box dla wskaźnika momentum
        self.tabA.momentumCheckBox = QtGui.QCheckBox("Momentum",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.momentumCheckBox)
        #check box dla ROC
        self.tabA.rocCheckBox = QtGui.QCheckBox("ROC",self.tabA.optionsFrame)
        self.tabA.optionsLayout.addWidget(self.tabA.rocCheckBox)
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
            chart = Chart(self.tabA)
            self.tabA.chartsLayout.addWidget(chart)
            chart.rmVolumeBars()
            chart.addVolumeBars()

        
            
            

        
       

        
