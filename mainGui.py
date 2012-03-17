# -*- coding: utf-8 -*-

import sys
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

        """tab A wskaźniki i oscylatory""" 
	self.tabA = AbstractTab()
        self.tabA.setObjectName("tabA")

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

        """l"""
        #self.loadLists()
    def paintChart(self):
            chart = Chart(self.tabA)
            self.tabA.chartsLayout.addWidget(chart)
            chart.rmVolumeBars()
            chart.addVolumeBars()

    """ przykładowo dodaje liste w przyszłości inna forma listy"""
    def loadLists(self):
        dataParser.loadData()
        for l in dataParser.STOCK_LIST:
            item = QtGui.QListWidgetItem()
            item.setText(l[1])
            self.tabA.stockListView.addItem(item)
        
            
            

        
       

        
