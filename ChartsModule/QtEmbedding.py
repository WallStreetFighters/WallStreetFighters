from PyQt4 import QtGui, QtCore
from Chart import Chart
import sys

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        chart = Chart(self.main_widget)        
        l.addWidget(chart)
        chart.drawPlot()

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)        

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Wykresik")
aw.show()
sys.exit(qApp.exec_())




