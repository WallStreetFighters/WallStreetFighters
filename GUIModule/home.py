# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Home (QtGui.QWidget):
    def __init__(self,topList = None,mostList = None,gainerList = None, loserList = None):
        self.topList = topList
        self.mostList = mostList
        self.loserList = loserList
        self.gainerList = gainerList
        QtGui.QWidget.__init__(self)
        self.initUi()
    def initUi(self):
        self.gridLayout = QtGui.QGridLayout(self)
        #ramka zawierajaca obiekty z góry yahoo 
        self.topFrame = QtGui.QFrame(self)
        self.topFrame.setMaximumSize(QtCore.QSize(16777215, 120))
        self.topFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.topFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.topLayout = QtGui.QHBoxLayout(self.topFrame)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.topLayout.addItem(spacerItem)
        for objList in self.topList:
            self.addTopObject(objList)


        
        spacerItem1 = QtGui.QSpacerItem(39, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.topLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.topFrame, 0, 1, 1, 1)
        #koniec top ramki

        #ramka zawierajaca Most Activities, Gainers i Losers
        self.scrollArea = QtGui.QScrollArea(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(340, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(340, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.leftFrame = QtGui.QWidget()
        self.leftLayout = QtGui.QVBoxLayout(self.leftFrame)
        self.label1 = QtGui.QLabel("Most Activities",self.leftFrame)
        self.leftLayout.addWidget(self.label1)
        self.addTable(self.mostList)
        self.addTable(self.gainerList)
        self.addTable(self.loserList)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.leftLayout.addItem(spacerItem2)
        self.scrollArea.setWidget(self.leftFrame)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 2, 1)


        #rssLayout
        self.rssFrame = QtGui.QFrame(self)
        self.rssFrame.setAutoFillBackground(True)
        self.rssFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rssFrame.setFrameShadow(QtGui.QFrame.Raised)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rssFrame.sizePolicy().hasHeightForWidth())
        self.rssFrame.setSizePolicy(sizePolicy)
        self.rssLayout = QtGui.QHBoxLayout(self.rssFrame)
        self.gridLayout.addWidget(self.rssFrame, 1, 1, 1, 1)

    def addTopObject(self,objList):
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setMaximumSize(QtCore.QSize(100, 100))
        self.frame.setMinimumSize(QtCore.QSize(100, 100))
        verticalLayout = QtGui.QVBoxLayout(self.frame)
        nameLabel = QtGui.QLabel(self.frame)
        nameLabel.setText(objList[0])
        nameLabel.setStyleSheet('QLabel {color: blue}')
        verticalLayout.addWidget(nameLabel)
        prizeLabel = QtGui.QLabel(self.frame)
        prizeLabel.setText(objList[1])
        verticalLayout.addWidget(prizeLabel)
        changeLabel = QtGui.QLabel(self.frame)
        if objList[2][0] == '-':
            changeLabel.setStyleSheet('QLabel {color: red}')
        else:
            changeLabel.setStyleSheet('QLabel {color: green}')
        changeLabel.setText(objList[2])
        verticalLayout.addWidget(changeLabel)
        precentLabel = QtGui.QLabel(self.frame)
        if objList[3][0] == '-':
            precentLabel.setStyleSheet('QLabel {color: red}')
        else:
            precentLabel.setStyleSheet('QLabel {color: green}')
        precentLabel.setText(objList[3])
        verticalLayout.addWidget(precentLabel)
        self.topLayout.addWidget(self.frame)
        
                                  
    def addTable(self,objList2):
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 180))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 180))
        font = QtGui.QFont()
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.tableWidget.setFont(font)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(4)
        item = QtGui.QTableWidgetItem("Name")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem("Prize")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem('Change')
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem('Chg')
        self.tableWidget.setHorizontalHeaderItem(3, item)
        k = 0
        for objList in objList2:
            item = QtGui.QTableWidgetItem(objList[0])
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setBackground(brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
            brush.setStyle(QtCore.Qt.BDiagPattern)
            item.setForeground(brush)
            self.tableWidget.setItem(k, 0, item)
            #Prize
            item = QtGui.QTableWidgetItem(objList[1])
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(k, 1, item)
            #Change
            item = QtGui.QTableWidgetItem(objList[2])
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setForeground(brush)
            item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(k, 2, item)
            #%chg
            item = QtGui.QTableWidgetItem(objList[3])
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setForeground(brush)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(k, 3, item)
            k+=1
        
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(74)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.leftLayout.addWidget(self.tableWidget)
        
        
