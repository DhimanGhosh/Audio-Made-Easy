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
        
        music = Music()
        self.notesS = music.notesS
        self.notesb = music.notesb
        self.notes = self.notesS
        self.options_menu_vals = tuple()
        with open(features, 'r') as f:
            self.options_menu_vals = tuple([x.strip() for x in f.readlines()])
        self.input_menu_vals = tuple()
        self.rel_maj_min_options = ('Relative Major', 'Relative Minor')
        self.major_minor_options = ('Major', 'Minor')
        self.guitar_frets_options = tuple([str(i) for i in range(1, 23)]) # For Capo position entry
        self.sub_menu_selected = dict() # To Keep track of options selected
        self.option_change_detect = ''
        self.input_change_detect = ''
        
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
        self.option_menu.currentIndexChanged.connect(self.option_selection_change)

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

    def option_selection_change(self):
        selected_text = self.option_menu.currentText()
        
        # ----- Detect change in menu selection ----- #
        if self.option_change_detect != selected_text:
            print(self.sub_menu_selected)
            print('Option Menu Change Detected')
            self.input_menu.clear()
            print('Input Menu cleared')
            self.option_change_detect = selected_text
            print('New opt change detect set')
        
        # ----- Change Input Menu Values ----- #
        if selected_text != '--Select--':
            print('Option Item Selected:',selected_text)
            self.input_menu.setDisabled(False)
            if selected_text == self.options_menu_vals[0]: # Major Scale
                print('maj scale')
                if self.notation_S.isChecked():
                    self.notes = self.notesS
                elif self.notation_b.isChecked():
                    self.notes = self.notesb
                self.input_menu_vals = self.notes
            elif selected_text == self.options_menu_vals[1]: # Major Chord
                print('maj chord')
                if self.notation_S.isChecked():
                    self.notes = self.notesS
                elif self.notation_b.isChecked():
                    self.notes = self.notesb
                self.input_menu_vals = self.notes
            elif selected_text == self.options_menu_vals[2]: # Chords in Major Scale
                print('chords in maj scale')
                if self.notation_S.isChecked():
                    self.notes = self.notesS
                elif self.notation_b.isChecked():
                    self.notes = self.notesb
                self.input_menu_vals = self.notes
            print('rcvd inp menu vals')
            self.input_menu.addItem('--Select--')
            self.input_menu.addItems(self.input_menu_vals)
            self.input_menu.currentIndexChanged.connect(self.input_selection_change)
            print('set inp menu vals')
        else:
            self.input_menu.clear()
            self.input_menu.setDisabled(True)

        # ----- To Keep track of Selections ----- #
        if self.option_menu.currentText() in self.sub_menu_selected:
            self.sub_menu_selected[self.option_menu.currentText()].append(selected_text)
        else:
            self.sub_menu_selected[self.option_menu.currentText] = [selected_text]
    
    def input_selection_change(self):
        selected_text = self.input_menu.currentText()
        
        # ----- Detect change in menu selection ----- #
        if self.input_change_detect != selected_text:
            self.input_change_detect = selected_text
        
        # ----- Action performed on Input Menu Values ----- #
        if selected_text != '--Select--':
            option_menu_selected_text = self.option_menu.currentText()
            if option_menu_selected_text == self.options_menu_vals[0]: # Major Scale
                note = selected_text
                music = Music(note)
                result = music.major_scale()
                self.output_text.setText('     '.join(result))
            elif option_menu_selected_text == self.options_menu_vals[1]: # Major Chord
                note = selected_text
                music = Music(note)
                result = music.major_chord()
                self.output_text.setText('     '.join(result))
            elif option_menu_selected_text == self.options_menu_vals[2]: # Chords in Major Scale
                note = selected_text
                music = Music(note)
                result = music.chords_in_major_scale()
                self.output_text.setText('     '.join(result))

        # ----- To Keep track of Selections ----- #
        if self.input_menu.currentText() in self.sub_menu_selected:
            self.sub_menu_selected[self.input_menu.currentText()].append(selected_text)
        else:
            self.sub_menu_selected[self.input_menu.currentText] = [selected_text]

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
            window_obj.setGeometry(rect.width()//2-width//2, rect.height()//2-height//2, width, height)
            #window_obj.resize(width, height)
            window_obj.setMaximumHeight(height)
            window_obj.setMinimumHeight(height)
            window_obj.setMaximumWidth(width)
            window_obj.setMinimumWidth(width)
        else:
            window_obj.resize(width, height)

    def reset(self):
        self.notation_S.setChecked(True)
        self.option_menu.setCurrentIndex(0)
        self.input_menu.clear()
        self.output_text.setText('')

if __name__ == "__main__": 
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    #print('Screen: %s' % screen.name())
    size = screen.size()
    #print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    #print('Available: %d x %d' % (rect.width(), rect.height()))
    
    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QtGui.QIcon(''))
    ui = Ui_Dialog(MainWindow)

    ui.setupUi(MainWindow)
    ui.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())
