import sys
import os
from PyQt4 import QtGui
from mainGui import GuiMainWindow
import DataParserModule.dataParser as dataParser

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        # obiekt Gui
        self.gui = GuiMainWindow()
        self.gui.setupGui(self)
    def closeEvent(self, event):
	FILE = open('data.wsf','w')
	dataParser.saveHistory(FILE)
	FILE.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    print "ddd"
    while True:
        app.processEvents()
    
    
    
