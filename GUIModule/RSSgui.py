import sys
from PyQt4 import QtGui ,QtCore
from RSS import *

class RSSSite:
    """An RSS Site"""
    def __init__(self, Name="", Url=""):
        self.Name = Name
        rss_reader = RSSReader(Url)
class RSSWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUi()
        self.rssReader = RSSReader("http://rss.slashdot.org/Slashdot/slashdot")
        self.listItems = self.rssReader.GetItems()
        self.descriptionList = []
        self.showItems()   
    def initUi(self):
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.listFrame = QtGui.QFrame(self)
        self.listFrame.setMaximumSize(QtCore.QSize(350, 16777215))
        self.listFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.listFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(self.listFrame)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setMargin(1)
        self.label = QtGui.QLabel('Select Site',self.listFrame)
        self.verticalLayout.addWidget(self.label)

        self.urlView = QtGui.QListWidget(self.listFrame)
        self.urlView.setMaximumSize(QtCore.QSize(16777215, 100))
        item = QtGui.QListWidgetItem('strona1')
        self.urlView.addItem(item)
        item = QtGui.QListWidgetItem('strona2')
        self.urlView.addItem(item)
        #QtCore.QObject.connect(self.urlView,QtCore.SIGNAL("itemClicked(QListWidgetItem*)"),self.showItems)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.urlView.setFont(font)
        self.verticalLayout.addWidget(self.urlView)
        self.label_2 = QtGui.QLabel('Select RSS Item',self.listFrame)
        self.verticalLayout.addWidget(self.label_2)
        self.itemView = QtGui.QListWidget(self.listFrame)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.itemView.setFont(font)
        self.itemView.setObjectName("itemView")
        self.verticalLayout.addWidget(self.itemView)
        conect = QtCore.QObject.connect(self.itemView,QtCore.SIGNAL("itemClicked(QListWidgetItem*)"),self.showDescription)
        self.horizontalLayout.addWidget(self.listFrame)
        self.frame = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setMargin(1)
        self.textBrowser = QtGui.QTextBrowser(self.frame)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout.addWidget(self.frame)
    def showItems(self):
	for rssItem in self.listItems:
	    if (rssItem):
                self.descriptionList.append(rssItem.description)
		item = QtGui.QListWidgetItem(rssItem.title,self.itemView)
		self.itemView.addItem(item)
		
		
    def showDescription(self):
       index = self.itemView.currentRow()
       item = self.descriptionList[index]
       self.textBrowser.setText(item)
       
    
				

