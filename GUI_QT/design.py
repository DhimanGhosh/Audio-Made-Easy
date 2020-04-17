# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PYTHON\Codes\GUIs\MusicTheoryGuide.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(312, 257)
        self.notation_label = QtWidgets.QLabel(Dialog)
        self.notation_label.setGeometry(QtCore.QRect(40, 30, 47, 13))
        self.notation_label.setObjectName("notation_label")
        self.radioButton_S = QtWidgets.QRadioButton(Dialog)
        self.radioButton_S.setGeometry(QtCore.QRect(130, 30, 31, 17))
        self.radioButton_S.setObjectName("radioButton_S")
        self.radioButton_b = QtWidgets.QRadioButton(Dialog)
        self.radioButton_b.setGeometry(QtCore.QRect(210, 30, 31, 17))
        self.radioButton_b.setObjectName("radioButton_b")
        self.options_label = QtWidgets.QLabel(Dialog)
        self.options_label.setGeometry(QtCore.QRect(40, 70, 47, 13))
        self.options_label.setObjectName("options_label")
        self.input_label = QtWidgets.QLabel(Dialog)
        self.input_label.setGeometry(QtCore.QRect(40, 120, 47, 13))
        self.input_label.setObjectName("input_label")
        self.output_label = QtWidgets.QLabel(Dialog)
        self.output_label.setGeometry(QtCore.QRect(40, 170, 47, 13))
        self.output_label.setObjectName("output_label")
        self.reset_button = QtWidgets.QPushButton(Dialog)
        self.reset_button.setGeometry(QtCore.QRect(110, 210, 75, 23))
        self.reset_button.setObjectName("reset_button")
        self.option_menu = QtWidgets.QComboBox(Dialog)
        self.option_menu.setGeometry(QtCore.QRect(110, 70, 171, 22))
        self.option_menu.setObjectName("option_menu")
        self.input_menu = QtWidgets.QComboBox(Dialog)
        self.input_menu.setGeometry(QtCore.QRect(110, 120, 171, 22))
        self.input_menu.setObjectName("input_menu")
        self.output_text = QtWidgets.QLineEdit(Dialog)
        self.output_text.setGeometry(QtCore.QRect(110, 170, 171, 20))
        self.output_text.setObjectName("output_text")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.notation_label.setText(_translate("Dialog", "Notation"))
        self.radioButton_S.setText(_translate("Dialog", "#"))
        self.radioButton_b.setText(_translate("Dialog", "b"))
        self.options_label.setText(_translate("Dialog", "Options"))
        self.input_label.setText(_translate("Dialog", "Input"))
        self.output_label.setText(_translate("Dialog", "Output"))
        self.reset_button.setText(_translate("Dialog", "RESET"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
