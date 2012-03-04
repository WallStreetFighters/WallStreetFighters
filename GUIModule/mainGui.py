from PyQt4 import QtGui, QtCore

class GuiMainWindow(object):
    def setupGui(self,MainWindow):
        MainWindow.setObjectName("WallStreetFighters")
        MainWindow.resize(1000,700)

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralwidget")

        # tabWidget
        self.tabs = QtGui.QTabWidget(self.centralWidget)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 980, 640))
        #self.tabs.setTabPosition(self.tabs.West)
        self.tabs.setObjectName("Tabs") 
     
        # tab A
        self.tabA = QtGui.QWidget()
        self.tabA.setObjectName("tabA")
        
        self.tabs.addTab(self.tabA,"tabA")
        
        # tab B
        self.tabB = QtGui.QWidget()
        self.tabB.setObjectName("tabB")
        
        self.tabs.addTab(self.tabB,"tabB")
        # tab C
        self.tabC = QtGui.QWidget()
        self.tabC.setObjectName("tabC")
        
        self.tabs.addTab(self.tabC,"tabC")
        # tabs

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
       

        
