# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore
from GUIModule.Tab import *
from GUIModule.Calendar import *
import datetime
import os
from ChartsModule.Chart import Chart
from ChartsModule.CompareChart import CompareChart
import DataParserModule.dataParser as dataParser

class TabA(QtGui.QWidget):
    def __init__(self,indexModel=None,stockModel=None,forexModel=None,bondModel= None,
                 resourceModel = None,futuresModel = None, qModelIndex = None,settings = None,listName=None,showLists = True):
        self.indexModel = indexModel
        self.stockModel = stockModel
        self.forexModel = forexModel
        self.bondModel = bondModel
        self.resourceModel = resourceModel
        self.futuresModel = futuresModel
        self.showLists = showLists
        self.settings = settings
        self.qModelIndex = qModelIndex #lista przy porównywaniu
        self.listName = listName
        self.indicatorList = []
        self.indicatorCheckBoxList = []
        self.oscilatorCheckBoxList = []
        self.oldStart = None
        self.oldEnd = None
        self.oldStep = None
        self.chart =None
        QtGui.QWidget.__init__(self)
        self.initUi()

    def initUi(self):
        
        
	#wywołujemy metodę z modułu GUIModule.Tab
        #która tworzy podstawowe elementy GUI
        tabUi(self,self.showLists)
        
	self.hasChart = False #sprawdzenie czy istnieje 
	self.currentChart = ""
	self.chart = None
	self.finObj = None
	
        self.setObjectName("tabA")

        #ustawiamy modele danych
        if self.showLists:
            self.indexListView.setModel(self.indexModel)
            self.stockListView.setModel(self.stockModel)
            self.forexListView.setModel(self.forexModel)
            self.bondListView.setModel(self.bondModel)
            self.resourceListView.setModel(self.resourceModel)
            self.futuresListView.setModel(self.futuresModel)
        
        if not isinstance( self.qModelIndex,list):
            self.scrollArea = QtGui.QScrollArea(self.optionsFrame)
            self.scrollArea.setWidgetResizable(True)
            self.buttonsFrame = QtGui.QWidget()
            self.buttonsLayout = QtGui.QGridLayout(self.buttonsFrame)
            self.buttonsLayout.setContentsMargins(-1, 0, -1, -1)
            self.idicatorsLabel = QtGui.QLabel('Indicators:',self.optionsFrame)
            self.buttonsLayout.addWidget(self.idicatorsLabel,0,2,1,1)
            
            #check box dla SMA
            self.smaCheckBox = QtGui.QCheckBox("SMA",self.optionsFrame)
            self.buttonsLayout.addWidget(self.smaCheckBox,1,2,1,1)
            self.indicatorCheckBoxList.append(self.smaCheckBox)
            #check box dla WMA
            self.wmaCheckBox = QtGui.QCheckBox("WMA",self.optionsFrame)
            self.buttonsLayout.addWidget(self.wmaCheckBox,2,2,1,1)
            self.indicatorCheckBoxList.append(self.wmaCheckBox)
            #check box dla EMA
            self.emaCheckBox = QtGui.QCheckBox("EMA",self.optionsFrame)
            self.buttonsLayout.addWidget(self.emaCheckBox,3,2,1,1)
            self.indicatorCheckBoxList.append(self.emaCheckBox)
            #check box dla bollinger
            self.bollingerCheckBox = QtGui.QCheckBox("bollinger",self.optionsFrame)
            self.buttonsLayout.addWidget(self.bollingerCheckBox,0,3,1,1)
            self.indicatorCheckBoxList.append(self.bollingerCheckBox)

            self.oscilatorsLabel = QtGui.QLabel('Oscilators:',self.optionsFrame)
            self.buttonsLayout.addWidget(self.oscilatorsLabel,1,3,1,1)
            #check box dla wskaźnika momentum
            self.momentumCheckBox = QtGui.QRadioButton("momentum",self.optionsFrame)
            self.buttonsLayout.addWidget(self.momentumCheckBox,2,3,1,1)
            self.oscilatorCheckBoxList.append(self.momentumCheckBox)
            #check box dla CCI
            self.cciCheckBox = QtGui.QRadioButton("CCI",self.optionsFrame)
            self.buttonsLayout.addWidget(self.cciCheckBox,3,3,1,1)
            self.oscilatorCheckBoxList.append(self.cciCheckBox)
            #check box dla ROC
            self.rocCheckBox = QtGui.QRadioButton("ROC",self.optionsFrame)
            self.buttonsLayout.addWidget(self.rocCheckBox,0,4,1,1)
            self.oscilatorCheckBoxList.append(self.rocCheckBox)
            #check box dla RSI
            self.rsiCheckBox = QtGui.QRadioButton("RSI",self.optionsFrame)
            self.buttonsLayout.addWidget(self.rsiCheckBox,1,4,1,1)
            self.oscilatorCheckBoxList.append(self.rsiCheckBox)
            #check box dla Williams Oscilator
            self.williamsCheckBox = QtGui.QRadioButton("williams",
                                                         self.optionsFrame)
            self.buttonsLayout.addWidget(self.williamsCheckBox,2,4,1,1)
            self.oscilatorCheckBoxList.append(self.williamsCheckBox)

            #horizontal line
            self.line = QtGui.QFrame(self.buttonsFrame)
            self.line.setFrameShape(QtGui.QFrame.HLine)
            self.line.setFrameShadow(QtGui.QFrame.Sunken)
            self.buttonsLayout.addWidget(self.line, 4, 2, 1, 3)


            #check box dla drawTrend
            self.drawTrendCheckBox = QtGui.QCheckBox("drawTrend",self.optionsFrame)
            self.buttonsLayout.addWidget(self.drawTrendCheckBox,5,2,1,1)
            #label dla grubosci lini
            self.lineWidthLabel = QtGui.QLabel("line Width",self)
            self.buttonsLayout.addWidget(self.lineWidthLabel,5,3,1,1)
            #spin box dla grubosci lini
            self.lineWidthSpinBox = QtGui.QDoubleSpinBox(self.optionsFrame)
            self.lineWidthSpinBox.setFrame(True)
            self.lineWidthSpinBox.setReadOnly(False)
            self.lineWidthSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
            self.lineWidthSpinBox.setDecimals(1)
            self.lineWidthSpinBox.setMinimum(0.5)
            self.lineWidthSpinBox.setMaximum(5.0)
            self.lineWidthSpinBox.setSingleStep(0.5)
            self.lineWidthSpinBox.setProperty("value", 1.0)
            self.buttonsLayout.addWidget(self.lineWidthSpinBox,5,4,1,1)            

            self.scrollArea.setWidget(self.buttonsFrame)
            self.optionsLayout.addWidget(self.scrollArea, 0, 1, 4, 4)         
        

        #(przyciski dodajemy na sam koniec okna)wyswietlanie wykresu
        self.optionsLayout.addWidget(addChartButton(self),0,5,4,4)      

        if self.qModelIndex != None:
            if isinstance( self.qModelIndex,list):
                self.paintCompareChart()
                self.compareButton.setEnabled(False)
                self.chartTypeComboBox.setEnabled(False)
                self.volumenCheckBox.setEnabled(False)
            else:
                self.paint2Chart()
            self.dateButton.clicked.connect(self.updateDate)
            self.stepComboBox.currentIndexChanged.connect(self.updateStep)
            self.logRadioButton.toggled.connect(self.updateScale)
            if not isinstance( self.qModelIndex,list):
                self.chartTypeComboBox.currentIndexChanged.connect(self.updateChartType)
                self.volumenCheckBox.stateChanged.connect(self.updateHideVolumen)
                self.paintCheckBox.stateChanged.connect(self.updateEnablePainting)
                for box in self.oscilatorCheckBoxList:
                    box.clicked.connect(self.updateOscilator)
                self.smaCheckBox.stateChanged.connect(self.smaChanged)
                self.emaCheckBox.stateChanged.connect(self.emaChanged)
                self.wmaCheckBox.stateChanged.connect(self.wmaChanged)
                self.drawTrendCheckBox.stateChanged.connect(self.updateDrawTrend)
                self.bollingerCheckBox.stateChanged.connect(self.bollingerChanged)
            self.startDateEdit.dateChanged.connect(self.checkDate)
            self.endDateEdit.dateChanged.connect(self.checkDate)    
            
    def updateScale(self):
        if self.logRadioButton.isChecked():
            self.settings["scale"] = 'log'
        else:
            self.settings["scale"] = 'linear'
        
        if self.chart !=None:
            self.chart.setScaleType(self.settings["scale"])
            self.chart.repaint()
            self.chart.update()
            #self.chart.emit(QtCore.SIGNAL("movido"))
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
            
    def updateChartType(self):
        self.settings["ChartType"] = self.chartTypeComboBox.currentText()
        if self.chart !=None:
            self.chart.setMainType(self.settings["ChartType"])
            self.updateDrawTrend()
            self.chart.repaint()
            self.chart.update()
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
    def updateStep(self):
        self.settings["step"]= self.stepComboBox.currentText()
        if self.chart !=None:
            dateStart = self.startDateEdit.date()
            start = datetime.datetime(dateStart.year(),dateStart.month(),dateStart.day())
            dateEnd = self.endDateEdit.date()
            end = datetime.datetime(dateEnd.year(),dateEnd.month(),dateEnd.day())
            if isinstance( self.qModelIndex,list):
                for fin in self.finObj:
                    fin.updateArchive(self.settings['step'])
            else:
                self.finObj.updateArchive(self.settings["step"])
            self.chart.setData(self.finObj,start,end,self.settings["step"])
            self.chart.repaint()
            self.chart.update()
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
    def updateDate(self):
        print 'jestem w update date'
        dateStart = self.startDateEdit.date()
        self.settings["start"] = datetime.datetime(dateStart.year(),dateStart.month(),dateStart.day())
        dateEnd = self.endDateEdit.date()
        self.settings["end"] = datetime.datetime(dateEnd.year(),dateEnd.month(),dateEnd.day())
        if self.chart !=None:
            if isinstance( self.qModelIndex,list):
                for fin in self.finObj:
                    fin.updateArchive(self.settings['step'])
            else:
                self.finObj.updateArchive(self.settings["step"])
            self.chart.setData(self.finObj,self.settings["start"],self.settings["end"],self.settings["step"])
            self.chart.repaint()
            self.chart.update()
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
    def updateOscilator(self):
        self.settings["oscilator"] =" "
        for box in self.oscilatorCheckBoxList:
            if box.isChecked():
                self.settings["oscilator"] = str(box.text())
        if self.chart !=None:
            self.chart.setOscPlot(self.settings["oscilator"])
            self.chart.repaint()
            self.chart.update()
            #self.chart.emit(QtCore.SIGNAL("movido"))
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
            
    def updateHideVolumen(self):
        hideVolumen =self.volumenCheckBox.isChecked()
        if self.chart !=None:
            if not self.chartsLayout.isEmpty():
                self.chartsLayout.removeWidget(self.chart)
            if hideVolumen:
                self.chart.rmVolumeBars()
            else:
                self.chart.addVolumeBars()

            self.chartsLayout.addWidget(self.chart)
            self.chart.repaint()
            self.chart.update()
            self.checkDrawTrend()
            #self.chart.emit(QtCore.SIGNAL("movido"))
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)

    def updateEnablePainting(self):
        painting =self.paintCheckBox.isChecked()
        if self.chart !=None:
            if not self.chartsLayout.isEmpty():
                self.chartsLayout.removeWidget(self.chart)
            self.chart.setDrawingMode(painting)
            self.chartsLayout.addWidget(self.chart)
            self.chart.repaint()
            self.chart.update()
            #self.chart.emit(QtCore.SIGNAL("movido"))
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
            
    def smaChanged(self,state):
        print state
        if state == 0:
            self.settings['indicator'].remove('SMA')
        if state == 2:
            self.settings['indicator'].append('SMA')
        self.updateIndicator()
    def emaChanged(self,state):
        if state == 0:
            self.settings['indicator'].remove('EMA')
        if state == 2:
            self.settings['indicator'].append('EMA')
        self.updateIndicator()
    def wmaChanged(self,state):
        if state == 0:
            self.settings['indicator'].remove('WMA')
        if state == 2:
            self.settings['indicator'].append('WMA')
        self.updateIndicator()
    def bollingerChanged(self,state):
        if state == 0:
            self.settings['indicator'].remove('bollinger')
        if state == 2:
            self.settings['indicator'].append('bollinger')
        self.updateIndicator()
    def updateIndicator(self):
        if self.chart !=None:
            if self.settings['indicator']:
                self.chart.setMainIndicator(self.settings['indicator'][-1])
            else:
                self.chart.setMainIndicator("")
            self.chart.repaint()
            self.chart.update()
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
        font = QtGui.QFont()
        font.setBold(False)
        for box in self.indicatorCheckBoxList:
            box.setFont(font)
        font.setBold(True)
        #font.setWeight(75)
        if self.settings['indicator']:
            name = self.settings['indicator'][-1].lower()
            eval ('self.'+name+'CheckBox.setFont(font)')
    def updateDrawTrend(self):
        drawTrend =self.drawTrendCheckBox.isChecked()
        if self.chart !=None and drawTrend:
            self.chart.drawTrend()
            self.chart.repaint()
            self.chart.update()
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)
        else:
            self.chart.repaint()
            self.chart.update()
            m= self.parentWidget().parentWidget().parentWidget().parentWidget()
            m.resize(m.width() , m.height()-20)
            m.resize(m.width() , m.height()+20)

    def checkDrawTrend(self):
        drawTrend =self.drawTrendCheckBox.isChecked()
        if self.chart !=None and drawTrend:
            self.chart.drawTrend()

            
            
    def checkDate(self):
        if self.startDateEdit.date() >= self.endDateEdit.date():
            self.endDateEdit.setDate(self.startDateEdit.date())

    def paint2Chart(self):

        print self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[2]
        index = int (self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])

        if self.listName == "index":
            if dataParser.INDEX_LIST[index][2] == 'Yahoo':     
                self.finObj = dataParser.createWithArchivesFromYahoo(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3],self.settings["step"])
	    else:
                self.finObj = dataParser.createWithArchivesFromStooq(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3],self.settings["step"])
            self.currentChart = self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0]

        if self.listName == "stock":
            if dataParser.STOCK_LIST[index][2] == 'Yahoo':
                self.finObj = dataParser.createWithArchivesFromYahoo(dataParser.STOCK_LIST[index][1],dataParser.STOCK_LIST[index][0],'stock',dataParser.STOCK_LIST[index][3],self.settings["step"])
	    else:
		self.finObj = dataParser.createWithArchivesFromStooq(dataParser.STOCK_LIST[index][1],dataParser.STOCK_LIST[index][0],'stock',dataParser.STOCK_LIST[index][3],self.settings["step"])
            self.currentChart = self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        if self.listName == "forex":
            self.finObj = dataParser.createWithArchivesFromStooq(dataParser.FOREX_LIST[index][1],dataParser.FOREX_LIST[index][0],'forex',dataParser.FOREX_LIST[index][3],self.settings["step"])
            self.currentChart = self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0]

        if self.listName == "bond":
            if dataParser.BOND_LIST[index][2] == 'Yahoo':
                self.finObj = dataParser.createWithArchivesFromYahoo(dataParser.BOND_LIST[index][1],dataParser.BOND_LIST[index][0],'bond',dataParser.BOND_LIST[index][3],self.settings["step"])
	    else:
		self.finObj = dataParser.createWithArchivesFromStooq(dataParser.BOND_LIST[index][1],dataParser.BOND_LIST[index][0],'bond',dataParser.BOND_LIST[index][3],self.settings["step"])
            self.currentChart = self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0]
        if self.listName == "resource":
            if dataParser.RESOURCE_LIST[index][2] == 'Yahoo':
                self.finObj = dataParser.createWithArchivesFromYahoo(dataParser.RESOURCE_LIST[index][1],dataParser.RESOURCE_LIST[index][0],'resource',dataParser.RESOURCE_LIST[index][3],self.settings["step"])
	    else:
		self.finObj = dataParser.createWithArchivesFromStooq(dataParser.RESOURCE_LIST[index][1],dataParser.RESOURCE_LIST[index][0],'resource',dataParser.RESOURCE_LIST[index][3],self.settings["step"])
            self.currentChart = self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0]
            
        if self.listName == "futures":
            if dataParser.FUTURES_LIST[index][2] == 'Yahoo':
                self.finObj = dataParser.createWithArchivesFromYahoo(dataParser.FUTURES_LIST[index][1],dataParser.FUTURES_LIST[index][0],'futures',dataParser.FUTURES_LIST[index][3],self.settings["step"])
	    else:
		self.finObj = dataParser.createWithArchivesFromStooq(dataParser.FUTURES_LIST[index][1],dataParser.FUTURES_LIST[index][0],'resource',dataParser.FUTURES_LIST[index][3],self.settings["step"])
            self.currentChart = self.qModelIndex.data(QtCore.Qt.WhatsThisRole).toStringList()[0]

        self.chart = Chart(self, self.finObj)
        self.cid = self.chart.mpl_connect('button_press_event', self.showChartsWithAllIndicators)
        self.chartsLayout.addWidget(self.chart)
        self.hasChart = True
    
        self.chart.setOscPlot(self.settings["oscilator"])
        self.chart.setDrawingMode(self.settings["painting"])
        if self.settings["indicator"]:
            self.chart.setMainIndicator(self.settings["indicator"][-1])
        self.chart.setData(self.finObj,self.settings["start"],self.settings["end"],self.settings["step"])
        self.chart.setScaleType(self.settings["scale"])
        self.chart.setMainType(self.settings["chartType"])
        
        if self.settings['drawTrend']:
            lineWidth = self.settings['lineWidth']
            self.chart.drawTrend()
        
        if self.settings["hideVolumen"]:
            self.chart.rmVolumeBars()

        self.setOptions()

    def paintCompareChart(self):
        self.finObj = []
        print self.qModelIndex
        if self.listName == "index":
            for model in self.qModelIndex:
                index = int (model.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])
                if dataParser.INDEX_LIST[index][2] == 'Yahoo':
                    finObj = dataParser.createWithArchivesFromYahoo(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3],self.settings["step"])
                else:
                    finObj = dataParser.createWithArchivesFromStooq(dataParser.INDEX_LIST[index][1],dataParser.INDEX_LIST[index][0],'index',dataParser.INDEX_LIST[index][3],self.settings["step"])
                self.finObj.append(finObj)
        if self.listName == "stock":
            for model in self.qModelIndex:
                index = int (model.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])
                if dataParser.STOCK_LIST[index][2] == 'Yahoo':
                    finObj = dataParser.createWithArchivesFromYahoo(dataParser.STOCK_LIST[index][1],dataParser.STOCK_LIST[index][0],'stock',dataParser.STOCK_LIST[index][3],self.settings["step"])
                else:
                    finObj = dataParser.createWithArchivesFromStooq(dataParser.STOCK_LIST[index][1],dataParser.STOCK_LIST[index][0],'stock',dataParser.STOCK_LIST[index][3],self.settings["step"])
                self.finObj.append(finObj)
        if self.listName == "forex":
            for model in self.qModelIndex:
                index = int (model.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])
                if dataParser.FOREX_LIST[index][2] == 'Yahoo':
                    finObj = dataParser.createWithArchivesFromYahoo(dataParser.FOREX_LIST[index][1],dataParser.FOREX_LIST[index][0],'forex',dataParser.FOREX_LIST[index][3],self.settings["step"])
                else:
                    finObj = dataParser.createWithArchivesFromStooq(dataParser.FOREX_LIST[index][1],dataParser.FOREX_LIST[index][0],'forex',dataParser.FOREX_LIST[index][3],self.settings["step"])
                self.finObj.append(finObj)
        if self.listName == "bond":
            for model in self.qModelIndex:
                index = int (model.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])
                if dataParser.BOND_LIST[index][2] == 'Yahoo':
                    finObj = dataParser.createWithArchivesFromYahoo(dataParser.BOND_LIST[index][1],dataParser.BOND_LIST[index][0],'bond',dataParser.BOND_LIST[index][3],self.settings["step"])
                else:
                    finObj = dataParser.createWithArchivesFromStooq(dataParser.BOND_LIST[index][1],dataParser.BOND_LIST[index][0],'bond',dataParser.BOND_LIST[index][3],self.settings["step"])
                self.finObj.append(finObj)
        if self.listName == "resource":
            for model in self.qModelIndex:
                index = int (model.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])
                if dataParser.RESOURCE_LIST[index][2] == 'Yahoo':
                    finObj = dataParser.createWithArchivesFromYahoo(dataParser.RESOURCE_LIST[index][1],dataParser.RESOURCE_LIST[index][0],'resource',dataParser.RESOURCE_LIST[index][3],self.settings["step"])
                else:
                    finObj = dataParser.createWithArchivesFromStooq(dataParser.RESOURCE_LIST[index][1],dataParser.RESOURCE_LIST[index][0],'resource',dataParser.RESOURCE_LIST[index][3],self.settings["step"])
                self.finObj.append(finObj)
                
        if self.listName == "futures":
            for model in self.qModelIndex:
                index = int (model.data(QtCore.Qt.WhatsThisRole).toStringList()[-1])
                if dataParser.FUTURES_LIST[index][2] == 'Yahoo':
                    finObj = dataParser.createWithArchivesFromYahoo(dataParser.FUTURES_LIST[index][1],dataParser.FUTURES_LIST[index][0],'futures',dataParser.FUTURES_LIST[index][3],self.settings["step"])
                else:
                    finObj = dataParser.createWithArchivesFromStooq(dataParser.FUTURES_LIST[index][1],dataParser.FUTURES_LIST[index][0],'futures',dataParser.FUTURES_LIST[index][3],self.settings["step"])
                self.finObj.append(finObj)
        
        self.chart = CompareChart(self)
        self.chart.setData(self.finObj,self.settings["start"],self.settings["end"],self.settings["step"])
        self.chartsLayout.addWidget(self.chart)

        #przywracamy opcje
        self.startDateEdit.setDate(QtCore.QDate(self.settings["start"].year,
                                   self.settings["start"].month,
                                   self.settings["start"].day))
        self.endDateEdit.setDate(QtCore.QDate(self.settings["end"].year,
                                 self.settings["end"].month,
                                 self.settings["end"].day))
        #step
        if self.settings["step"] == "daily":
            self.stepComboBox.setCurrentIndex(0)
        elif self.settings["step"] == "weekly":
            self.stepComboBox.setCurrentIndex(1)
        else:
            self.stepComboBox.setCurrentIndex(2)
        if self.settings["painting"]:
            self.paintCheckBox.setCheckState(2)
	
    def setOptions(self):
        #przywracamy odpowiednie ustawienia opcji w GUI
        #data
        self.startDateEdit.setDate(QtCore.QDate(self.settings["start"].year,
                                   self.settings["start"].month,
                                   self.settings["start"].day))
        self.endDateEdit.setDate(QtCore.QDate(self.settings["end"].year,
                                 self.settings["end"].month,
                                 self.settings["end"].day))
        if "SMA" in self.settings["indicator"]:
            self.smaCheckBox.setChecked(True)
            self.indicatorList.append('SMA')
        if 'WMA' in self.settings["indicator"]:
            self.wmaCheckBox.setChecked(True)
            self.indicatorList.append('WMA')
        if 'EMA' in self.settings["indicator"]:
            self.emaCheckBox.setChecked(True)
            self.indicatorList.append('EMA')
        if 'bollinger' in self.settings["indicator"]:
            self.bollingerCheckBox.setChecked(True)
            self.indicatorList.append('boolinger')

        font = QtGui.QFont()
        font.setBold(True)
        #font.setWeight(75)
        if self.settings["indicator"]:
            name = self.settings["indicator"][-1].lower()
            eval ('self.'+name+'CheckBox.setFont(font)')            
        if self.settings["oscilator"] == "momentum":
            self.momentumCheckBox.setChecked(True)
        elif self.settings["oscilator"] == "CCI":
            self.cciCheckBox.setChecked(True)
        elif self.settings["oscilator"] == "ROC":
            self.rocCheckBox.setChecked(True)
        elif self.settings["oscilator"] == "RSI":
            self.rsiCheckBox.setChecked(True)
        elif self.settings["oscilator"] == "williams":
            self.williamsCheckBox.setChecked(True)
        #step
        if self.settings["step"] == "daily":
            self.stepComboBox.setCurrentIndex(0)
        elif self.settings["step"] == "weekly":
            self.stepComboBox.setCurrentIndex(1)
        else:
            self.stepComboBox.setCurrentIndex(2)
        #chartType
        if self.settings["chartType"] == "line":
            self.chartTypeComboBox.setCurrentIndex(0)
        elif self.settings["chartType"] == "point":
            self.chartTypeComboBox.setCurrentIndex(1)
        else:
            self.chartTypeComboBox.setCurrentIndex(2)
        #volumen
        if self.settings["hideVolumen"]:
            self.volumenCheckBox.setCheckState(2)
        #painting
        if self.settings["painting"]:
            self.paintCheckBox.setCheckState(2)
    def showChartsWithAllIndicators(self,x):
       
        if len(self.settings["indicator"]) >= 3:
            print 'opening popup'
            start = self.settings["start"]
            end = self.settings["end"]
            oscilator = self.settings["oscilator"]
            painting = self.settings["painting"]
            scale = self.settings['scale']
            chartType = self.settings["chartType"]
            step = self.settings["step"]
            hideVolumen = self.settings["hideVolumen"]
            
            self.chart.mpl_disconnect(self.cid)
            self.w = self.MyPopup(self)
            self.w.setGeometry(QtCore.QRect(100, 100, 1200, 900))
            k = 0
            for i in self.settings["indicator"]:
                chart2 = Chart(self, self.finObj)
                chart2.setData(self.finObj,start,end,step)
                chart2.setOscPlot(oscilator)
                chart2.setDrawingMode(painting)
                chart2.setMainIndicator(i)
                chart2.setScaleType(scale)
                chart2.setMainType(chartType)
                if hideVolumen:
                    chart2.rmVolumeBars()
                self.w.layout.addWidget(chart2,k/2,k%2,1,1)
                k+=1
                #self.cid = self.chart.mpl_connect('button_press_event', self.showChartsWithAllIndicators)
                self.w.show()
    class MyPopup(QtGui.QWidget):
        def __init__(self,parent):
            self.parent=parent
            QtGui.QWidget.__init__(self)
            self.initUI()
        def initUI(self):
            self.layout =  QtGui.QGridLayout(self)
        def closeEvent(self, event):
            self.parent.cid = self.parent.chart.mpl_connect('button_press_event', self.parent.showChartsWithAllIndicators)
