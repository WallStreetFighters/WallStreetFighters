# -*- coding: utf-8 -*-

import sys
import datetime
import operator
import threading
import time
import os
from PyQt4 import QtGui, QtCore
from TabA import TabA
import cPickle
import GUIModule.RSSgui as RSSgui
from GUIModule.home import Home 
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
        os.chdir("../WallStreetFighters/DataParserModule")
        dataParser.loadData()
	FILE = open("../GUIModule/data.wsf", 'r')
	dataParser.loadHistory(FILE)
	FILE.close()


        # inicjujemy model danych dla Index
        self._indexModel = self.ListModel(list=dataParser.INDEX_LIST)
        self.indexModel = QtGui.QSortFilterProxyModel()
        self.indexModel.setSourceModel(self._indexModel)
        self.indexModel.setFilterCaseSensitivity(0)
        self.indexModel.setDynamicSortFilter(True)
        # inicjujemy model danych dla Stock
        self._stockModel = self.ListModel(list=dataParser.STOCK_LIST)
        self.stockModel = QtGui.QSortFilterProxyModel()
        self.stockModel.setSourceModel(self._stockModel)
        self.stockModel.setFilterCaseSensitivity(0)
        self.stockModel.setDynamicSortFilter(True)
        # inicjujemy model danych dla Forex
        self._forexModel = self.ListModel(list=dataParser.FOREX_LIST)
        self.forexModel = QtGui.QSortFilterProxyModel()
        self.forexModel.setSourceModel(self._forexModel)
        self.forexModel.setFilterCaseSensitivity(0)
        self.forexModel.setDynamicSortFilter(True)
        # inicjujemy model danych dla Resources
        self._resourceModel = self.ListModel(list=dataParser.RESOURCE_LIST)
        self.resourceModel = QtGui.QSortFilterProxyModel()
        self.resourceModel.setSourceModel(self._resourceModel)
        self.resourceModel.setFilterCaseSensitivity(0)
        self.resourceModel.setDynamicSortFilter(True)
        # inicjujemy model danych dla Bond
        self._bondModel = self.ListModel(list=dataParser.BOND_LIST)
        self.bondModel = QtGui.QSortFilterProxyModel()
        self.bondModel.setSourceModel(self._bondModel)
        self.bondModel.setFilterCaseSensitivity(0)
        self.bondModel.setDynamicSortFilter(True)
        # model danych dla Futures
        self._futuresModel = self.ListModel(list = dataParser.FUTURES_LIST)
        self.futuresModel = QtGui.QSortFilterProxyModel()
        self.futuresModel.setSourceModel(self._futuresModel)
        self.futuresModel.setFilterCaseSensitivity(0)
        self.futuresModel.setDynamicSortFilter(True)
        
        """home """
	File = open("../GUIModule/save.wsf", 'r')
	valueList = cPickle.load(File)
	self.home = Home(valueList[0],valueList[1],valueList[3],valueList[2])       
	self.tabs.addTab(self.home,"Home")
        self.rssWidget = RSSgui.RSSWidget(self.home)
        self.home.rssLayout.addWidget(self.rssWidget)
	self.home.startUpdating()

        """Search"""
	self.tabA = TabA(None,self.indexModel,self.stockModel,self.forexModel,self.bondModel,self.resourceModel,self.futuresModel)
        self.tabs.addTab(self.tabA,"Search")
        
        self.tabA.indexListView.doubleClicked.connect(self.newIndexTab)
        self.tabA.stockListView.doubleClicked.connect(self.newStockTab)
        self.tabA.forexListView.doubleClicked.connect(self.newForexTab)
        self.tabA.bondListView.doubleClicked.connect(self.newBondTab)
        self.tabA.resourceListView.doubleClicked.connect(self.newResourceTab)
        self.tabA.futuresListView.doubleClicked.connect(self.newFuturesTab)
        self.tabA.compareButton.clicked.connect(self.compare)

        self.tabA.nasdaqButton.pressed.connect(self.nasdaqFiltre)
        self.tabA.nyseButton.pressed.connect(self.nyseFiltre)
        self.tabA.wigButton.pressed.connect(self.wigFiltre)
        self.tabA.wig20Button.pressed.connect(self.wig20Filtre)
        self.tabA.amexButton.pressed.connect(self.amexFiltre)
        self.tabA.allButton.pressed.connect(self.allFiltre)

        self.tabA.filterLineEdit.textChanged.connect(self.bigFiltre)

        
        """ teraz otwieramy zakładki z historii"""
        tabHistoryFile = open('tabHistory.wsf','rb')
        tabHistoryList = cPickle.load(tabHistoryFile)
        for tabSettings in tabHistoryList:
            if not isinstance(tabSettings['index'],list): #przywracanie taba z pojedynczym instrumentem
                if tabSettings['finObjType'] == 'index':
                    qModelIndex =  self.indexModel.index(tabSettings['index'],0)
                    nameTab = str(qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0])
                    print "oto : " + nameTab
                    self.newIndexTab(qModelIndex ,nameTab,tabSettings)
                if tabSettings['finObjType'] == 'stock':
                    qModelIndex =  self.stockModel.index(tabSettings['index'],0)
                    nameTab = str(qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0])
                    print "oto : " + nameTab
                    self.newStockTab(qModelIndex ,nameTab,tabSettings)
                if tabSettings['finObjType'] == 'forex':
                    qModelIndex =  self.forexModel.index(tabSettings['index'],0)
                    nameTab = str(qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0])
                    print "oto : " + nameTab
                    self.newForexTab(qModelIndex ,nameTab,tabSettings)
                if tabSettings['finObjType'] == 'bond':
                    qModelIndex =  self.bondModel.index(tabSettings['index'],0)
                    nameTab = str(qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0])
                    print "oto : " + nameTab
                    self.newBondTab(qModelIndex ,nameTab,tabSettings)
                if tabSettings['finObjType'] == 'resources':
                    qModelIndex =  self.resourceModel.index(tabSettings['index'],0)
                    nameTab = str(qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0])
                    print "oto : " + nameTab
                    self.newResourceTab(qModelIndex ,nameTab,tabSettings)
                if tabSettings['finObjType'] == 'futures':
                    qModelIndex =  self.futuresModel.index(tabSettings['index'],0)
                    nameTab = str(qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0])
                    print "oto : " + nameTab
                    self.newFuturesTab(qModelIndex ,nameTab,tabSettings)
            else:  # porównywanie chart
                pass
                              

        
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
           
	""" koniec ustawiania Zakładek"""

	self.tabs.tabCloseRequested.connect(self.closeTab)
	
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralWidget)

				
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)        
        
    def compare(self):
        pageIndex = self.tabA.listsToolBox.currentIndex()
        if pageIndex == 0:
            qModelIndex = self.tabA.indexListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newIndexTab(qModelIndex,"Indices' comparison")
        if pageIndex == 1:
            qModelIndex = self.tabA.stockListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newStockTab(qModelIndex,"Stocks' comparison")
        if pageIndex == 2:
            qModelIndex = self.tabA.forexListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newForexTab(qModelIndex,"Forex comparison")
        if pageIndex == 3:
            qModelIndex = self.tabA.bondListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newBondTab(qModelIndex,"Bonds' comparison")
        if pageIndex == 4:
            qModelIndex = self.tabA.resourceListView.selectedIndexes()
            qModelIndex = map(lambda i: qModelIndex[i],filter(lambda i: i%2 == 0,range(len(qModelIndex))))
            self.newResourceTab(qModelIndex,"Resources' comparison")
        
    #metody otwierajace nowe zakladki po podwójnym kliknięciu
    def newIndexTab(self,qModelIndex,nameTab = None,settings = None):
        if settings == None:
            settings = self.settings()
        self.tabA1 = TabA('index',qModelIndex = qModelIndex,settings = settings,listName = "index",showLists = False)
        if not nameTab:
            nameTab = self.tabA.indexListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def newStockTab(self,qModelIndex,nameTab = None,settings = None):
        if settings == None:
            settings = self.settings()
        self.tabA1 = TabA('stock',qModelIndex = qModelIndex,settings = settings,listName = "stock",showLists = False)
        if not nameTab:
            nameTab = self.tabA.stockListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))
    def newForexTab(self,qModelIndex,nameTab = None,settings = None):
        if settings == None:
            settings = self.settings()
        self.tabA1 = TabA('forex',qModelIndex = qModelIndex,settings = settings,listName = "forex",showLists = False)
        if not nameTab:
            nameTab = self.tabA.forexListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def newBondTab(self,qModelIndex,nameTab = None,settings = None):
        if settings == None:
            settings = self.settings()
        self.tabA1 = TabA('bond',qModelIndex = qModelIndex,settings = settings,listName = "bond",showLists = False)
        if not nameTab:
            nameTab = self.tabA.bondListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))

    def newResourceTab(self,qModelIndex,nameTab = None,settings = None):
        if settings == None:
            settings = self.settings()
        self.tabA1 = TabA('resources',qModelIndex = qModelIndex,settings = settings,listName = "resource",showLists = False)
        if not nameTab:
            nameTab = self.tabA.resourceListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))
    def newFuturesTab(self,qModelIndex,nameTab = None,settings = None):
        if settings == None:
            settings = self.settings()
        self.tabA1 = TabA('futures',qModelIndex = qModelIndex,settings = settings,listName = "futures",showLists = False)
        if not nameTab:
            nameTab = self.tabA.futuresListView.currentIndex().data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        self.tabs.setCurrentIndex(self.tabs.addTab(self.tabA1,nameTab))


    def settings(self):
        #funkcja pobiera aktualnie zaznaczone opcje z tabA
        dateStart = self.tabA.startDateEdit.date()  # początek daty
        start = datetime.datetime(dateStart.year(),dateStart.month(),dateStart.day())
        
        dateEnd = self.tabA.endDateEdit.date()     # koniec daty
        end = datetime.datetime(dateEnd.year(),dateEnd.month(),dateEnd.day())
        indicator = []
        if self.tabA.smaCheckBox.isChecked():
            indicator.append("SMA")
        if self.tabA.wmaCheckBox.isChecked():
            indicator.append("WMA")
        if self.tabA.emaCheckBox.isChecked():
            indicator.append("EMA")
        if self.tabA.bollingerCheckBox.isChecked():
            indicator.append("bollinger")
        oscilator = ''
        if self.tabA.momentumCheckBox.isChecked():
            oscilator = "momentum"
        elif self.tabA.cciCheckBox.isChecked():
            oscilator = "CCI"
        elif self.tabA.rocCheckBox.isChecked():
            oscilator = "ROC"
        elif self.tabA.rsiCheckBox.isChecked():
            oscilator = "RSI"
        elif self.tabA.williamsCheckBox.isChecked():
            oscilator = "williams"
        #step
        step = self.tabA.stepComboBox.currentText()
        #scale
        if self.tabA.logRadioButton.isChecked():
            scale = 'log'
        else:
            scale = 'linear'
        #chartType
        chartType = self.tabA.chartTypeComboBox.currentText()
        hideVolumen =self.tabA.volumenCheckBox.isChecked() 
        #painting
        painting = self.tabA.paintCheckBox.isChecked()
        #draw trend
        drawTrend = self.tabA.drawTrendCheckBox.isChecked()
        #line width
        lineWidth = self.tabA.lineWidthSpinBox.value()
        
        t = {"start":start,"end":end,"indicator":indicator,"step":step,
             "chartType":chartType,"hideVolumen":hideVolumen,
             "painting":painting,"scale":scale,"oscilator":oscilator,"drawTrend":drawTrend,'lineWidth':lineWidth}
        return t
    def closeTab(self,i):
        if i != 0 and i!=1:

            self.tabs.removeTab(i)

    def bigFiltre(self,text):

        self.stockModel.setFilterRole(33)
        self.stockModel.setFilterRegExp(text)

        self.indexModel.setFilterRole(33)
        self.indexModel.setFilterRegExp(text)
        
        self.forexModel.setFilterRole(33)
        self.forexModel.setFilterRegExp(text)

        self.resourceModel.setFilterRole(33)
        self.resourceModel.setFilterRegExp(text)
        
        self.bondModel.setFilterRole(33)
        self.bondModel.setFilterRegExp(text)
        
        self.futuresModel.setFilterRole(33)
        self.futuresModel.setFilterRegExp(text)

    def nasdaqFiltre(self):
        self.stockModel.setFilterRole(32)
        self.stockModel.setFilterRegExp("NASDAQ")
    def nyseFiltre(self):
        self.stockModel.setFilterRole(32)
        self.stockModel.setFilterRegExp("NYSE")
    def wigFiltre(self):
        self.stockModel.setFilterRole(32)
        self.stockModel.setFilterRegExp("WIG")
    def amexFiltre(self):
        self.stockModel.setFilterRole(32)
        self.stockModel.setFilterRegExp("AMEX")
    def wig20Filtre(self):
        self.stockModel.setFilterRole(32)
        self.stockModel.setFilterRegExp("WIG20")
    def allFiltre(self):
        self.stockModel.setFilterRole(32)
        self.stockModel.setFilterRegExp("")

            
    """ Modele przechowywania listy dla poszczególnych instrumentów finansowych"""    
    class ListModel(QtCore.QAbstractTableModel):
        def __init__(self,list, parent = None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self.list = list
            k = 0 
            for li in list:
                li.append(k)
                k+=1
            self.headerdata = ['symbol', 'name', '']
        def mainIndex(self):
            return 3

        
        def rowCount(self, parent):
            return len(self.list)
        def columnCount(self,parent):
            return 2
        def headerData(self, col, orientation, role):
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self.headerdata[col])
            return QtCore.QVariant()
        
        def showHideRows(self, name):
            rowCount = len(self.list)

            for row in range(rowCount):
                if self.index(row, 0).data(QtCore.Qt.WhatsThisRole).toStringList()[-2] == 'name':
                    self.setRowHidden(row, False)
                else:
                    self.setRowHidden(row,True)

        
        def data(self, index, role):
            if not index.isValid():
                return QtCore.QVariant()
            elif role == QtCore.Qt.WhatsThisRole:
                return self.list[index.row()]
            elif role != QtCore.Qt.DisplayRole and role != 32 and role!= 33 :
                return QtCore.QVariant()


            if role == 32:
                return self.list[index.row()][3]
            if role == 33:
                return self.list[index.row()][0] + ' ' + self.list[index.row()][1]+' '+ self.list[index.row()][3]
                
            return QtCore.QVariant(self.list[index.row()][index.column()])
                                        #if index.column() == 2:
                #return QtCore.QVariant(self.list[index.row()][index.column()+2])
        
        def sort(self, Ncol, order):
            """Sort table by given column number.
            """
            self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
            self.list = sorted(self.list, key=operator.itemgetter(Ncol))        
            if order == QtCore.Qt.DescendingOrder:
                self.list.reverse()
            self.emit(QtCore.SIGNAL("layoutChanged()"))
