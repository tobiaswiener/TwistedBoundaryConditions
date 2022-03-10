from PyQt6 import QtWidgets, QtCore
import sys

from collections.abc import Iterable

from pyqt_app.ParameterDicts import *



class ModelParamsWidget(QtWidgets.QWidget):
    def __init__(self, m):
        super().__init__()
        self.m = m
        self._layout = QtWidgets.QVBoxLayout()


        self.model_params = {}
        self.init_model_params()


        self.setupUI()

    def init_model_params(self):
        for param, standard_value in MODELS[self.m].items():
            if param == "types" or param == "name":
                pass
            elif isinstance(standard_value, Iterable):
                self.model_params[param] = QtWidgets.QComboBox()
                self.model_params[param].addItems(list(standard_value))
            else:
                self.model_params[param] = QtWidgets.QLineEdit(str(standard_value))
                self.model_params[param].setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def add_model_param_Ui(self):
        for param, lines in self.model_params.items():
            hbox = QtWidgets.QFormLayout()
            hbox.addRow(param, lines)
            self._layout.addItem(hbox)


    def setupUI(self):
        self.add_model_param_Ui()
        self.setLayout(self._layout)


    def get_model_params(self):
        params = {}
        for param, value in self.model_params.items():
            if isinstance(value, QtWidgets.QComboBox):
                temp_value = value.currentText()
                params[param] = MODELS[self.m]["types"][param](temp_value)
            else:
                temp_value = value.text()
                params[param] = MODELS[self.m]["types"][param](temp_value)
        return params






if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = ModelParamsWidget("two band")
    mw.show()
    sys.exit(app.exec())