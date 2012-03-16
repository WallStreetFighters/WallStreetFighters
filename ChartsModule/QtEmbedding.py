# coding: utf-8
from PyQt4 import QtGui, QtCore
from Chart import Chart
import sys
import matplotlib

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
        #l.addWidget(chart2)                                    
        limits = chart.mainPlot.get_xlim()
        print limits        
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)         
        chart.setOscPlot("Test")        
        chart.setMainIndicator("Test")                                  
        chart.setDrawingMode(True)        
        chart.setMainType("candlestick")

qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Wykresik")
aw.show()
sys.exit(qApp.exec_())




