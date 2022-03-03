from PyQt6 import QtWidgets, QtCore
import sys
from pyqt_app.ParameterDicts import *
from pyqt_app.input.modelWidget import ModelWidget
from pyqt_app.input.impWidget import ImpWidget

from pyqt_app.input.plotWidget import PlotWidget

class InputWidget(QtWidgets.QWidget):
    sig_calc_triggered = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)

        self._layout = QtWidgets.QGridLayout()

        self.model_widget = ModelWidget()
        self.plot_widget = PlotWidget()
        self.imp_widget = ImpWidget()
        self.btn_calc = QtWidgets.QPushButton("Calculate")
        self.btn_clear = QtWidgets.QPushButton("Clear")
        self.setupUi()



    def setupUi(self):
        self._layout.addWidget(self.model_widget,0,0)
        self._layout.addWidget(self.plot_widget,0,1)
        self._layout.addWidget(self.imp_widget,0,2)
        self._layout.addWidget(self.btn_calc,1,0)
        self._layout.addWidget(self.btn_clear,2,0)

        self.setLayout(self._layout)

    def get_model_params(self):
        m = self.model_widget.choose_model.currentText()
        params = self.model_widget.model_params_widgets[m].get_model_params()
        return m, params

    def get_plot_params(self):
        p = self.plot_widget.choose_plot.currentText()
        params = self.plot_widget.plot_params_widgets[p].get_plot_params()
        return p, params

    def get_imp_params(self):
        i = self.imp_widget.choose_imp.currentText()
        params = self.imp_widget.imp_params_widgets[i].get_imp_params()
        return i, params

if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = InputWidget()
    mw.show()
    sys.exit(app.exec())