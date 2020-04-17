import os, sys, platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QRadioButton, QComboBox, QLineEdit, QPushButton


if platform.system() == 'Linux':
    utils_dir = os.path.realpath('../Utils/')
    sys.path.insert(0, utils_dir)
    from Music import Music
    features = utils_dir + '/Features.txt'
else:
    root_dir = os.path.realpath('..')
    sys.path.insert(0, root_dir)
    from Utils.Music import Music
    features = root_dir + '/Utils/Features.txt'


class Ui_Dialog(object):
    def __init__(self, Dialog):
        self.window_width = 400
        self.window_height = 260

        Dialog.setObjectName("Dialog")
        self.set_window_resizable(window_obj=Dialog, width=self.window_width, height=self.window_height, flag=False)

        self.notation_label = QLabel(Dialog)
        self.notation_S = QRadioButton(Dialog)
        self.notation_b = QRadioButton(Dialog)
        self.options_label = QLabel(Dialog)
        self.option_menu = QComboBox(Dialog)
        self.input_label = QLabel(Dialog)
        self.input_menu = QComboBox(Dialog)
        self.output_label = QLabel(Dialog)
        self.output_text = QLineEdit(Dialog)
        self.reset_button = QPushButton(Dialog)

        self.options_menu_vals = tuple()
        with open(features, 'r') as f:
            self.options_menu_vals = tuple([x.strip() for x in f.readlines()])

    def setupUi(self, Dialog):
        # Notations
        self.notation_label.setGeometry(QtCore.QRect(40, 25, 47, 13))
        self.notation_label.setObjectName("notation_label")
        self.notation_S.setGeometry(QtCore.QRect(110, 23, 31, 17))
        self.notation_S.setObjectName("notation_S")
        self.notation_S.setChecked(True)
        self.notation_b.setGeometry(QtCore.QRect(300, 23, 31, 17))
        self.notation_b.setObjectName("notation_b")

        # Option Menu
        self.options_label.setGeometry(QtCore.QRect(40, 70, 47, 13))
        self.options_label.setObjectName("options_label")
        self.option_menu.setGeometry(QtCore.QRect(110, 68, self.window_width//2 + 50, 22))
        self.option_menu.setObjectName("option_menu")

        self.option_menu.addItem('--Select--')
        self.option_menu.addItems(self.options_menu_vals)

        # Input Menu
        self.input_label.setGeometry(QtCore.QRect(40, 120, 47, 13))
        self.input_label.setObjectName("input_label")
        self.input_menu.setGeometry(QtCore.QRect(110, 118, self.window_width//2 + 50, 22))
        self.input_menu.setObjectName("input_menu")
        self.input_menu.setDisabled(True)

        # Output
        self.output_label.setGeometry(QtCore.QRect(40, 170, 47, 13))
        self.output_label.setObjectName("output_label")
        self.output_text.setGeometry(QtCore.QRect(110, 168, 250, 22))
        self.output_text.setObjectName("output_text")
        self.output_text.setDisabled(True)

        # App RESET
        self.reset_button.setGeometry(QtCore.QRect(40, 210, 320, 30))
        self.reset_button.setObjectName("reset_button")
        self.reset_button.clicked.connect(self.reset)  


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Music Theory Guide"))
        self.notation_label.setText(_translate("Dialog", "Notation"))
        self.notation_S.setText(_translate("Dialog", "#"))
        self.notation_b.setText(_translate("Dialog", "b"))
        self.options_label.setText(_translate("Dialog", "Options"))
        self.input_label.setText(_translate("Dialog", "Input"))
        self.output_label.setText(_translate("Dialog", "Output"))
        self.output_text.setText(_translate("Dialog", ""))
        self.reset_button.setText(_translate("Dialog", "Reset Application"))

    def set_window_resizable(self, window_obj, width, height, flag=False):
        if not flag:
            window_obj.resize(width, height)
            window_obj.setMaximumHeight(height)
            window_obj.setMinimumHeight(height)
            window_obj.setMaximumWidth(width)
            window_obj.setMinimumWidth(width)
        else:
            window_obj.resize(width, height)

    def reset(self):
        self.notation_S.setChecked(True)

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    
    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QtGui.QIcon(''))
    ui = Ui_Dialog(MainWindow)

    ui.setupUi(MainWindow)
    ui.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())
