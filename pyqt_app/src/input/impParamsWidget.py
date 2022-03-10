from PyQt6 import QtWidgets, QtCore
from collections.abc import Iterable

from src.ParameterDicts import *



class ImpParamsWidget(QtWidgets.QWidget):
    def __init__(self, i):
        super().__init__()
        self.i = i
        self._layout = QtWidgets.QVBoxLayout()


        self.imp_params = {}
        self.init_imp_params()

        self.setupUI()

    def init_imp_params(self):
        for param, standard_value in IMPURITIES[self.i].items():
            if param == "types" or param == "name":
                pass
            elif isinstance(standard_value, Iterable):
                self.imp_params[param] = QtWidgets.QComboBox()
                self.imp_params[param].addItems(list(standard_value))
            else:
                self.imp_params[param] = QtWidgets.QLineEdit(str(standard_value))
                self.imp_params[param].setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


    def add_imp_param_Ui(self):
        for param, lines in self.imp_params.items():
            hbox = QtWidgets.QFormLayout()
            hbox.addRow(param, lines)
            self._layout.addItem(hbox)


    def setupUI(self):
        self.add_imp_param_Ui()
        self.setLayout(self._layout)






    def get_imp_params(self):
        params = {}
        params["name"] = self.i
        for param, value in self.imp_params.items():
            if isinstance(value, QtWidgets.QComboBox):
                temp_value = value.currentText()
                params[param] = IMPURITIES[self.i]["types"][param](temp_value)
            else:
                temp_value = value.text()
                params[param] = IMPURITIES[self.i]["types"][param](temp_value)
        return params





