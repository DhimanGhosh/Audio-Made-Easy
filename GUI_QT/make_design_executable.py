import sys

# Place the design code here
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
  
    MainWindow = QtWidgets.QMainWindow()
    #<ui = design_class_name()>
  
    #<ui.setupUi(MainWindow)>
    MainWindow.show()
    sys.exit(app.exec_())



# Convert .ui to .py (pyuic5 -x D:\PYTHON\Codes\GUIs\MusicTheoryGuide.ui -o D:\PYTHON\Codes\Music-Theory-Guide\GUI_QT\design.py)