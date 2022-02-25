import sys

from PyQt6 import QtGui, QtCore, QtWidgets
from parameterDialog import ParameterDialog
class inputdialogdemo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(inputdialogdemo, self).__init__(parent)

        layout = QtWidgets.QFormLayout()
        self.btn = QtWidgets.QPushButton("Choose model")
        self.btn.clicked.connect(self.getItem)
        self.le = QtWidgets.QLineEdit()
        layout.addRow(self.btn, self.le)


        self.parameters = ParameterDialog()
        layout.addRow(self.parameters)

        self.setLayout(layout)
        self.setWindowTitle("Input Dialog demo")


    def getItem(self):
        items = ("tight binding", "2 band isolator")

        item, ok = QtWidgets.QInputDialog.getItem(self, "select model dialog",
                                        "list of models", items, 0, False)

        if ok and item:
            self.le.setText(item)

    def gettext(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 't:')

        if ok:
            self.le1.setText(str(text))

    def getint(self):
        num, ok = QtWidgets.QInputDialog.getInt(self, "integer input dualog", "enter a number")

        if ok:
            self.le2.setText(str(num))