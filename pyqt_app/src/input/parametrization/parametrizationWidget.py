from PyQt6 import QtWidgets
import sys


from src.ParameterDicts import *
from src.input.parametrization.parametrizationParamsWidget import PlotParamsWidget

class ParametrizationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()

        self._layout_choose_model = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("choose plot:")
        self.choose_plot = QtWidgets.QComboBox()

        self.plot_params_widgets = {}
        self.init_ModelParamsWidget()


        self.setupUI()

    def init_ModelParamsWidget(self):
        for m in PLOTS:
            self.plot_params_widgets[m] = PlotParamsWidget(m)


    def add_model_param_Ui(self):
        for m in self.plot_params_widgets:
            if not m == self.choose_plot.currentText():
                self.plot_params_widgets[m].hide()
            self._layout.addWidget(self.plot_params_widgets[m])

    def setupUI(self):
        self.choose_plot.addItems(PLOTS)
        self.choose_plot.currentTextChanged.connect(self.setPlot)


        self._layout_choose_model.addWidget(self.label)
        self._layout_choose_model.addWidget(self.choose_plot)
        self._layout.addLayout(self._layout_choose_model)

        self.add_model_param_Ui()
        self.setLayout(self._layout)


    def setPlot(self):
        m = self.choose_plot.currentText()
        self._hide_all_model_params()
        self.plot_params_widgets[m].show()

    def _hide_all_model_params(self):
        for key, value in self.plot_params_widgets.items():
            value.hide()





if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = ParametrizationWidget()
    mw.show()
    sys.exit(app.exec())