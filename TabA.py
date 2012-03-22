# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore
from GUIModule.Tab import *
import datetime
from ChartsModule.Chart import Chart
import DataParserModule.dataParser as dataParser

class TabA(QtGui.QWidget):
    def __init__(self,indexModel=None,stockModel=None,forexModel=None):
        self.indexModel = indexModel
        self.stockModel = stockModel
        self.forexModel = forexModel
        QtGui.QWidget.__init__(self)
        self.initUi()
        """tab A wskaźniki i oscylatory"""
    def initUi(self):
        
        
	#wywołujemy metodę z modułu GUIModule.Tab
        #która tworzy podstawowe elementy GUI
        tabUi(self)
        
	self.hasChart = False #sprawdzenie czy istnieje 
	self.currentChart = ""
	self.chart = None
	self.finObj = None
	
        self.setObjectName("tabA")

        #ustawiamy modele danych 
        self.indexListView.setModel(self.indexModel)
        self.stockListView.setModel(self.stockModel)
        self.forexListView.setModel(self.forexModel)
        
        
        self.idicatorsLabel = QtGui.QLabel('Indicators:',self.optionsFrame)
        self.optionsLayout.addWidget(self.idicatorsLabel,0,4,1,1)
        #check box dla wskaźnika momentum
        self.momentumCheckBox = QtGui.QCheckBox("Momentum",self.optionsFrame)
        self.optionsLayout.addWidget(self.momentumCheckBox,1,6,1,1)
        #check box dla ROC
        self.rocCheckBox = QtGui.QCheckBox("ROC",self.optionsFrame)
        self.optionsLayout.addWidget(self.rocCheckBox,1,4,1,1)
        #check box dla SMA
        self.smaCheckBox = QtGui.QCheckBox("SMA",self.optionsFrame)
        self.optionsLayout.addWidget(self.smaCheckBox,2,4,1,1)
        #check box dla EMA
        self.emaCheckBox = QtGui.QCheckBox("EMA",self.optionsFrame)
        self.optionsLayout.addWidget(self.emaCheckBox,0,5,1,1)
        #check box dla CCI
        self.cciCheckBox = QtGui.QCheckBox("CCI",self.optionsFrame)
        self.optionsLayout.addWidget(self.cciCheckBox,1,5,1,1)
        #check box dla RSI
        self.rsiCheckBox = QtGui.QCheckBox("RSI",self.optionsFrame)
        self.optionsLayout.addWidget(self.rsiCheckBox,2,5,1,1)
        #check box dla Williams Oscilator
        self.williamsOscilatorCheckBox = QtGui.QCheckBox("Williams Oscilator",self.optionsFrame)
        self.optionsLayout.addWidget(self.williamsOscilatorCheckBox,0,6,1,1)    
        #(przyciski dodajemy na sam koniec okna)wyswietlanie wykresu
        self.optionsLayout.addWidget(addChartButton(self),0,7,3,4)

        self.indexListView.pressed.connect(self.selectRow)
        self.stockListView.pressed.connect(self.selectRowStock)
        self.chartButton.clicked.connect(self.paintChart)
        

    def paintChart(self):
        
        pageIndex = self.listsToolBox.currentIndex() #sprawdzamy z jakiej listy korzystamy
        dateStart = self.startDateEdit.date()  # początek daty
        start = datetime.datetime(dateStart.year(),dateStart.month(),dateStart.day())
        
        dateEnd = self.endDateEdit.date()     # koniec daty
        end = datetime.datetime(dateEnd.year(),dateEnd.month(),dateEnd.day())
        indicator = 'momentum'
        if self.momentumCheckBox.isChecked():
            indicator = "momentum"
        elif self.smaCheckBox.isChecked():
            indicator = "SMA"
        elif self.emaCheckBox.isChecked():
            indicator = "EMA"
        #step
        step = self.stepComboBox.currentText()

        #chartType
        chartType = self.chartTypeComboBox.currentText()
        hideVolumen =self.volumenCheckBox.isChecked() 
        #painting
        painting = self.paintCheckBox.isChecked()

       
        
        # Jeśli wybrano instrument Index
        if pageIndex == 0:
            if self.hasChart == False:
                
                indexes = self.indexListView.selectedIndexes()
                index= indexes[0].row()
                self.currnetChart = indexes[0].row()
            
                self.finObj = dataParser.createWithCurrentValueFromYahoo(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3])
                self.finObj.updateArchive()
                self.chart = Chart(self, self.finObj)
                self.chartsLayout.addWidget(self.chart)
                self.hasChart = True
                self.currentChart = self.indexListView.currentIndex().data(QtCore.Qt.DisplayRole).toString()
            elif self.currentChart != self.indexListView.currentIndex().data(QtCore.Qt.DisplayRole).toString(): 
                
                self.chartsLayout.removeWidget(self.chart)
                indexes = self.indexListView.selectedIndexes()
                index= indexes[0].row()
                self.currnetChart = indexes[0].row()
                self.finObj = dataParser.createWithCurrentValueFromYahoo(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3])
                self.finObj.updateArchive()
                self.chart = Chart(self, self.finObj)
                self.chartsLayout.addWidget(self.chart)
                self.hasChart = True
                self.currentChart =self.indexListView.currentIndex().data(QtCore.Qt.DisplayRole).toString()

            self.chart.setOscPlot(indicator)
            self.chart.setDrawingMode(painting)
            self.chart.setData(self.finObj,start,end,step)
            self.chart.setMainType(chartType)
            if hideVolumen:
                self.chart.rmVolumeBars()
            
        # Jeśli wybrano instrument Stock
        if pageIndex == 1:
            if self.hasChart == False:
                print "jestem w pierwszy chart"
                indexes = self.stockListView.selectedIndexes()
                index= indexes[0].row()
                self.currnetChart = indexes[0].row()
            
                self.finObj = dataParser.createWithCurrentValueFromYahoo(dataParser.STOCK_LIST[index][1],dataParser.STOCK_LIST[index][0],'stock',dataParser.STOCK_LIST[index][3])
                self.finObj.updateArchive()
                self.chart = Chart(self, self.finObj)
                self.chartsLayout.addWidget(self.chart)
                self.hasChart = True
                self.currentChart = self.stockListView.currentIndex().data(QtCore.Qt.DisplayRole).toString()
            elif self.currentChart != self.stockListView.currentIndex().data(QtCore.Qt.DisplayRole).toString(): 
                print "jestem w inny chart"
                self.chartsLayout.removeWidget(self.chart)
                indexes = self.stockListView.selectedIndexes()
                index= indexes[0].row()
                self.currnetChart = indexes[0].row()
                
                self.finObj = dataParser.createWithCurrentValueFromYahoo(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3])
                self.finObj.updateArchive()
                self.chart = Chart(self, self.finObj)
                self.chartsLayout.addWidget(self.chart)
                self.hasChart = True
                self.currentChart =self.stockListView.currentIndex().data(QtCore.Qt.DisplayRole).toString()

            self.chart.setOscPlot(indicator)
            self.chart.setDrawingMode(painting)
            self.chart.setData(self.finObj,start,end,step)
            self.chart.setMainType(chartType)
            if hideVolumen:
                self.chart.rmVolumeBars()

    def selectRow(self):
        self.indexListView.selectRow(self.indexListView.currentIndex().row())
    def selectRowStock(self):
        self.stockListView.selectRow(self.stockListView.currentIndex().row())
        
