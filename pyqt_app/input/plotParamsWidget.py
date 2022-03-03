from PyQt6 import QtWidgets, QtCore
import sys

from collections.abc import Iterable

from pyqt_app.ParameterDicts import *



class PlotParamsWidget(QtWidgets.QWidget):
    def __init__(self, p):
        super().__init__()
        self.p = p
        self._layout = QtWidgets.QVBoxLayout()


        self.plot_params = {}
        self.init_plot_params()


        self.setupUI()

    def init_plot_params(self):
        for param, standard_value in PLOTS[self.p].items():
            if param == "types" or param == "name":
                pass
            elif isinstance(standard_value, Iterable):
                self.plot_params[param] = QtWidgets.QComboBox()
                self.plot_params[param].addItems(list(standard_value))
            else:
                self.plot_params[param] = QtWidgets.QLineEdit(str(standard_value))
                self.plot_params[param].setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


    def add_plot_param_Ui(self):
        for param, lines in self.plot_params.items():
            hbox = QtWidgets.QFormLayout()
            hbox.addRow(param, lines)
            self._layout.addItem(hbox)


    def setupUI(self):
        self.add_plot_param_Ui()
        self.setLayout(self._layout)


    def get_plot_params(self):
        params = {}
        params["name"] = self.p
        for param, value in self.plot_params.items():
            if isinstance(value, QtWidgets.QComboBox):
                temp_value = value.currentText()
                params[param] = PLOTS[self.p]["types"][param](temp_value)
            else:
                temp_value = value.text()
                params[param] = PLOTS[self.p]["types"][param](temp_value)
        return params



if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = PlotParamsWidget("linear")
    mw.show()
    sys.exit(app.exec())