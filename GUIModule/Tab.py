# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore

class AbstractTab(QtGui.QWidget):
    """klasa bazowa dla każdej z zakładek aplikacji"""
    def __init__(self,parent=None):
         QtGui.QWidget.__init__(self,parent)
         self.initUi()
    def initUi(self):
        """ przycisk wyjścia z programu"""
        quitButton = QtGui.QPushButton('Quit',self)
        quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quitButton.resize(quitButton.sizeHint())
        quitButton.move(880, 570) 
    
