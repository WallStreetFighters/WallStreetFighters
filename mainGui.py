# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from GUIModule.Tab import AbstractTab
from ChartsModule.Chart import Chart

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

        #tab A
	self.tabA = AbstractTab()
        self.tabA.setObjectName("tabA")
        #slot  wyswietlanie wykresu
        self.tabA.chartButton.clicked.connect(self.paintChart)
        self.tabs.addTab(self.tabA,"tabA")
        
        # tab B
        self.tabB = AbstractTab()
        self.tabB.setObjectName("tabB")
        
        self.tabs.addTab(self.tabB,"tabB")
        # tab C
        self.tabC = AbstractTab()
        self.tabC.setObjectName("tabC")
        
        self.tabs.addTab(self.tabC,"tabC")
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
    def paintChart(self):
            chart = Chart(self.tabA)
            self.tabA.chartsLayout.addWidget(chart)
            chart.rmVolumeBars()
            chart.addVolumeBars()
            
            

        
       

        
