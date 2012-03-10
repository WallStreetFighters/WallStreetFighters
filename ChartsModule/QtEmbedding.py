# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
import sys

class ApplicationWindow(QtGui.QMainWindow):
    """Klasa demonstrująca jak przykładowo można osadzić wykres w Qt."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        chart = Chart(self.main_widget)                
        l.addWidget(chart)        
        """można też kilka wykresów w jednym oknie - ich poukładanie (pionowo/poziomo)
        to już kwestia ustawień layoutu Qt, czyli działka Dawida"""
        #chart2 = Chart(self.main_widget)
        #l.addWidget(chart)                        
        chart.setOscPlot("Test")
        chart.rmVolumeBars()
        chart.setMainIndicator("Test")                
        chart.setOscPlot("Test")
        chart.setMainType("candlestick")        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)        

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Wykresik")
aw.show()
sys.exit(qApp.exec_())




