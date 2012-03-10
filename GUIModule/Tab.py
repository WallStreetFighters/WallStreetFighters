# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore

class AbstractTab(QtGui.QWidget):
    """klasa bazowa dla każdej z zakładek aplikacji"""
    def __init__(self,parent=None):
         QtGui.QWidget.__init__(self,parent)
         self.initUi()
    def initUi(self):
        
        
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        """Każdą zakładkę dzielimy jak na razie na 3 obszary: opcje,
        listy , wykresy """
        
        """Ramka przechowujaca listy"""
        self.listsFrame = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
        QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listsFrame.sizePolicy().hasHeightForWidth())
        self.listsFrame.setSizePolicy(sizePolicy)
        # ustawimy maksymalna szerokosc kolumny na 150
        self.listsFrame.setMaximumSize(QtCore.QSize(150, 16777215))
        self.listsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.listsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.listsFrame.setLineWidth(3)
        self.horizontalLayout.addWidget(self.listsFrame)

        """Ramka przechowujaca opcje"""
        self.optionsFrame = QtGui.QFrame(self)
        sizePolicy2 = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
        QtGui.QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.optionsFrame.sizePolicy().hasHeightForWidth())
        self.optionsFrame.setSizePolicy(sizePolicy2)
        # ustawimy maksymalna szerokosc kolumny na 150
        self.optionsFrame.setMaximumSize(QtCore.QSize(150, 16777215))
        self.optionsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.optionsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.optionsFrame.setLineWidth(3)
        self.horizontalLayout.addWidget(self.optionsFrame)

        
        """Ramka przechowujaca wykresy"""
        self.chartsFrame = QtGui.QFrame(self)
        sizePolicy3 = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
        QtGui.QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.chartsFrame.sizePolicy().hasHeightForWidth())
        self.chartsFrame.setSizePolicy(sizePolicy3)
        self.chartsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.chartsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.chartsFrame.setLineWidth(3)
        self.horizontalLayout.addWidget(self.chartsFrame)

        
                
        """ przycisk wyjścia z programu"""
        quitButton = QtGui.QPushButton('Quit',self.optionsFrame)
        quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quitButton.resize(quitButton.sizeHint())
         
    
