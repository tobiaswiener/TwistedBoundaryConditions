from PyQt6 import QtWidgets
import sys

from src.ParameterDicts import *
from src.input.modelParamsWidget import ModelParamsWidget


class ModelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()

        self._layout_choose_model = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("choose model:")
        self.choose_model = QtWidgets.QComboBox()

        self.model_params_widgets = {}
        self.init_ModelParamsWidget()


        self.setupUI()

    def init_ModelParamsWidget(self):
        for m in MODELS:
            self.model_params_widgets[m] = ModelParamsWidget(m)


    def add_model_param_Ui(self):
        for m in self.model_params_widgets:
            if not m == self.choose_model.currentText():
                self.model_params_widgets[m].hide()
            self._layout.addWidget(self.model_params_widgets[m])

    def setupUI(self):
        self.choose_model.addItems(MODELS)
        self.choose_model.currentTextChanged.connect(self.setModel)


        self._layout_choose_model.addWidget(self.label)
        self._layout_choose_model.addWidget(self.choose_model)
        self._layout.addLayout(self._layout_choose_model)

        self.add_model_param_Ui()
        self.setLayout(self._layout)


    def setModel(self):
        m = self.choose_model.currentText()
        self._hide_all_model_params()
        self.model_params_widgets[m].show()

    def _hide_all_model_params(self):
        for key, value in self.model_params_widgets.items():
            value.hide()




if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = ModelWidget()
    mw.show()
    sys.exit(app.exec())