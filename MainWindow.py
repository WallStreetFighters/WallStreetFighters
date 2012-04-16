import sys
import os
from PyQt4 import QtGui
from mainGui import GuiMainWindow
import DataParserModule.dataParser as dataParser
import cPickle

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
	valueList = [self.gui.home.topList,self.gui.home.mostList,self.gui.home.loserList,self.gui.home.gainerList]
	cPickle.dump(valueList, open('save.wsf','w'))

	ran = range(self.gui.tabs.count())
	tabHistoryList = []
	for i in ran:
            if i >1:
                t=  self.gui.tabs.widget(i).getSettings()
                tabHistoryList.append(t)
        cPickle.dump(tabHistoryList, open('tabHistory.wsf','w'))
    
    


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    print "ddd"
    while True:
        app.processEvents()
    
    
    
