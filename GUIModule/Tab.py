# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore

def tabUi(self,showLists=True):
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        """Każdą zakładkę dzielimy jak na razie na 3 obszary: opcje,
        listy , wykresy """
        
        """Ramka przechowujaca listy"""
        self.listsFrame = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
        QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listsFrame.sizePolicy().hasHeightForWidth())
        self.listsFrame.setSizePolicy(sizePolicy)
        # ustawimy maksymalna szerokosc kolumny na 350
        self.listsFrame.setMaximumSize(QtCore.QSize(400, 16777215))
        self.listsFrame.setMinimumSize(QtCore.QSize(350, 0))
        self.listsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.listsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.listsFrame.setLineWidth(3)
        

        #ustawiamy zarządce rozkładu vertical
        self.listsLayout = QtGui.QVBoxLayout(self.listsFrame)
        # Tool Box przechowujący listy
        self.listsToolBox = QtGui.QToolBox(self.listsFrame)

        #Index
        self.indexPage = QtGui.QWidget(self.listsFrame)
        self.indexPageLayout = QtGui.QHBoxLayout(self.indexPage)
        self.listsToolBox.addItem(self.indexPage, "Index")
        self.indexListView = QtGui.QTableView(self.listsFrame)
        self.indexListView.setAlternatingRowColors(True)
        self.indexListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.indexListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableStyle(self,self.indexListView) #ustawiamy styl tabeli
        self.indexPageLayout.addWidget(self.indexListView)
        

        #Stock
        self.stockPage = QtGui.QWidget(self.listsFrame)
        self.stockPageLayout = QtGui.QHBoxLayout(self.stockPage)
        self.listsToolBox.addItem(self.stockPage , "Stock")
        self.stockListView = QtGui.QTableView(self.listsFrame)
        self.stockListView.setAlternatingRowColors(True)
        self.stockListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.stockListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableStyle(self,self.stockListView)#ustawiamy styl tabeli
        self.stockPageLayout.addWidget(self.stockListView)

        #forex
        self.forexPage = QtGui.QWidget(self.listsFrame)
        self.forexPageLayout = QtGui.QHBoxLayout(self.forexPage)
        self.listsToolBox.addItem(self.forexPage, "Forex")
        self.forexListView = QtGui.QTableView(self.listsFrame)
        self.forexListView.setAlternatingRowColors(True)
        self.forexListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.forexListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableStyle(self,self.forexListView)#ustawiamy styl tabeli
        self.forexPageLayout.addWidget(self.forexListView)

        #Bond
        self.bondPage = QtGui.QWidget(self.listsFrame)
        self.bondPageLayout = QtGui.QHBoxLayout(self.bondPage)
        self.listsToolBox.addItem(self.bondPage, "Bond")
        self.bondListView = QtGui.QTableView(self.listsFrame)
        self.bondListView.setAlternatingRowColors(True)
        self.bondListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.bondListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableStyle(self,self.bondListView)
        self.bondPageLayout.addWidget(self.bondListView)


        #Commodity
        self.commodityPage = QtGui.QWidget(self.listsFrame)
        self.commodityPageLayout = QtGui.QHBoxLayout(self.commodityPage)
        self.listsToolBox.addItem(self.commodityPage, "Commodity")
        self.commodityListView = QtGui.QTableView(self.listsFrame)
        self.commodityListView.setAlternatingRowColors(True)
        self.commodityListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.commodityListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableStyle(self,self.commodityListView)
        self.commodityPageLayout.addWidget(self.commodityListView)

        #Futures contract
        self.futuresContractPage = QtGui.QWidget(self.listsFrame)
        self.futuresContractPageLayout = QtGui.QHBoxLayout(self.futuresContractPage)
        self.listsToolBox.addItem(self.futuresContractPage, "Futures Contract")
        self.futuresContractListView = QtGui.QTableView(self.listsFrame)
        self.futuresContractListView.setAlternatingRowColors(True)
        self.futuresContractListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.futuresContractListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableStyle(self,self.futuresContractListView)
        self.futuresContractPageLayout.addWidget(self.futuresContractListView)
        
        self.listsLayout.addWidget(self.listsToolBox)
                # koniec Tool Box
        if showLists:
            self.horizontalLayout.addWidget(self.listsFrame)
        # koniec ramki przechowywyjącej listy
        

        """Ramka przechowujaca opcjie i wykres"""
        self.optionsAndChartsFrame = QtGui.QFrame(self)
        # ustawimy maksymalna szerokosc kolumny na 350
        #self.optionsAndChartsFrame.setMaximumSize(QtCore.QSize(1600, 16777215))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.optionsAndChartsFrame.sizePolicy().hasHeightForWidth())
        self.optionsAndChartsFrame.setSizePolicy(sizePolicy)
        self.optionsAndChartsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.optionsAndChartsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(self.optionsAndChartsFrame)

        """Ramka przechowujaca wykresy"""
        self.chartsFrame = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.chartsFrame.sizePolicy().hasHeightForWidth())
        self.chartsFrame.setSizePolicy(sizePolicy)
        self.chartsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.chartsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.chartsFrame.setLineWidth(3)
        #ustawiamy zarządce rozkładu vertical
        self.chartsLayout = QtGui.QVBoxLayout(self.chartsFrame)
        self.verticalLayout.addWidget(self.chartsFrame)

        """Ramka przechowujaca opcje"""
        self.optionsFrame = QtGui.QFrame(self)
        # ustawimy maksymalna wysokosc na 120
        self.optionsFrame.setMaximumSize(QtCore.QSize(16777215, 120))
        self.optionsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.optionsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.optionsFrame.setLineWidth(3)
        #ustawiamy zarządce rozkładu Grid
        self.optionsLayout = QtGui.QGridLayout(self.optionsFrame)
        
        #pola do wprowadzania okresu
        self.label = QtGui.QLabel('Range:',self.optionsFrame) 
        self.optionsLayout.addWidget(self.label,0,0,1,1)
        self.startDateEdit = QtGui.QDateEdit(self.optionsFrame)
        self.startDateEdit.setDate(QtCore.QDate.currentDate().addDays(-18))
        self.startDateEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))
        self.optionsLayout.addWidget(self.startDateEdit,1,0,1,1)

        self.endDateEdit = QtGui.QDateEdit(self.optionsFrame)
        self.endDateEdit.setDate(QtCore.QDate.currentDate().addDays(-5))
        self.endDateEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))
        self.optionsLayout.addWidget(self.endDateEdit,2,0,1,1)
        #koniec pola do wprowadzania okresu
	self.verticalLayout.addWidget(self.optionsFrame)

        #dodajemy ramke zawierajaca wykres i opcje do tab
        self.horizontalLayout.addWidget(self.optionsAndChartsFrame)

def addChartButton(self):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(6)

        # Step combo box
        self.stepLabel = QtGui.QLabel('Step',self.optionsFrame)#label Step
        self.gridLayout.addWidget(self.stepLabel,0,0,1,1)
        self.stepComboBox = QtGui.QComboBox(self.optionsFrame)
        self.stepComboBox.addItem('daily')
        self.stepComboBox.addItem('weekly')
        self.stepComboBox.addItem('monthly')
        self.gridLayout.addWidget(self.stepComboBox,1,0,1,1)
        # chartType comboBox
        self.chartTypeLabel = QtGui.QLabel('Chart Type',self.optionsFrame)#label Chart Type
        self.gridLayout.addWidget(self.chartTypeLabel,0,1,1,1)
        self.chartTypeComboBox = QtGui.QComboBox(self.optionsFrame)
        self.chartTypeComboBox.addItem('line')
        self.chartTypeComboBox.addItem('point')
        self.chartTypeComboBox.addItem('candlestick')
        self.gridLayout.addWidget(self.chartTypeComboBox,1,1,1,1)
        # Scale Type
        self.scaleTypeLabel = QtGui.QLabel('Scale',self.optionsFrame)
        self.gridLayout.addWidget(self.scaleTypeLabel,0,2,1,1)
        self.linearRadioButton = QtGui.QRadioButton('linear',self.optionsFrame)
        self.gridLayout.addWidget(self.linearRadioButton,1,2,1,1)
        self.logRadioButton = QtGui.QRadioButton('log',self.optionsFrame)
        self.gridLayout.addWidget(self.logRadioButton,2,2,1,1)
        #wyłaczenie voluminu
        self.volumenCheckBox = QtGui.QCheckBox('Hide Volumen',self.optionsFrame)
        self.gridLayout.addWidget(self.volumenCheckBox,0,3,1,1)
        #wlacznie możliwości rysowania na wykeresie
        self.paintCheckBox = QtGui.QCheckBox('Enable painting',self.optionsFrame)
        self.gridLayout.addWidget(self.paintCheckBox,1,3,1,1)
        #przycisk rysowania wykresu
        self.chartButton = QtGui.QPushButton('Chart',self.optionsFrame)
        self.chartButton.resize(self.chartButton.sizeHint())
        self.gridLayout.addWidget(self.chartButton,2,3,1,1)
	#Spacer
        #self.spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, 		QtGui.QSizePolicy.Expanding)
        #self.gridLayout.addItem(self.spacer,0,5,1,3)
        return self.frame
       
def tableStyle(self,table):
        # hide grid
        table.setShowGrid(False)
        # set the font
        font = QtGui.QFont("Courier New", 10)
        table.setFont(font)
        # hide vertical header
        vh = table.verticalHeader()
        vh.setVisible(False)
        # set column width to fit contents
        table.resizeColumnsToContents()
        # set horizontal header properties
        hh = table.horizontalHeader()
        hh.setStretchLastSection(True)
        
        # enable sorting
        table.setSortingEnabled(True)


        
                
        
        
         
    
