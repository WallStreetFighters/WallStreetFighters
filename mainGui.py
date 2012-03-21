# -*- coding: utf-8 -*-

import sys
import datetime
import operator
import os
from PyQt4 import QtGui, QtCore
from TabA import TabA
import GUIModule.RSSgui as RSSgui
#from GUIModule.Tab import AbstractTab
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

        #tabs - przechowywanie zakładek
	self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.tabs = QtGui.QTabWidget(self.centralWidget)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 980, 640))
        self.tabs.setObjectName("Tabs")
        self.tabs.setTabsClosable(True)

        #załadowanie List
        dataParser.loadData()

        # inicjujemy model danych dla Index
        self.indexModel = self.ListModel(list=dataParser.INDEX_LIST)
        # inicjujemy model danych dla Stock
        self.stockModel = self.ListModel(list=dataParser.STOCK_LIST)
        # inicjujemy model danych dla Forex
        self.forexModel = self.ListModel(list=dataParser.FOREX_LIST)

        """tab A wskaźniki i oscylatory"""
	self.tabA = TabA(self.indexModel,self.stockModel,self.forexModel)
        self.tabs.addTab(self.tabA,"tabA")
        """koniec tab A """
        
        """ tab B
        self.tabB = AbstractTab()
        self.tabB.setObjectName("tabB")

        #przycisk wyswietlanie wykresu (przyciski dodajemy na sam koniec okna)
        self.tabB.optionsLayout.addWidget(self.tabB.addChartButton(),0,4,3,4)
        self.tabs.addTab(self.tabB,"tabB")
        koniec tab B"""

        """ tabC
        self.tabC = AbstractTab()
        self.tabC.setObjectName("tabC")
        self.tabs.addTab(self.tabC,"tabC")
        self.tabC.optionsLayout.addWidget(self.tabC.addChartButton(),0,7,3,4)
        self.tabs.addTab(self.tabC,"tabC")
        
        Koniec tabC"""
        
        """ Rss tab"""
        self.RSSTab = QtGui.QWidget()
        self.tabs.addTab(self.RSSTab,"RSS")
        self.rssWidget = RSSgui.RSSWidget(self.RSSTab)
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
            
           

        
            
            

        
       

        
