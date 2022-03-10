from PyQt6 import QtWidgets

from src.input.impParamsWidget import ImpParamsWidget
from src.input.impListWidget import ImpListWidget
from src.ParameterDicts import *

class ImpWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()

        self._layout_choose_imp = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("choose impurity mode:")
        self.choose_imp = QtWidgets.QComboBox()

        self.imp_params_widgets = {}
        self.init_ImpurityParamsWidget()

        self.imp_list_widget = ImpListWidget()

        self.setupUI()

    def init_ImpurityParamsWidget(self):
        for m in IMPURITIES:
            self.imp_params_widgets[m] = ImpParamsWidget(m)


    def add_imp_param_Ui(self):
        for m in self.imp_params_widgets:
            if not m == self.choose_imp.currentText():
                self.imp_params_widgets[m].hide()
            self._layout.addWidget(self.imp_params_widgets[m])

    def setupUI(self):
        self.choose_imp.addItems(IMPURITIES)
        self.choose_imp.currentTextChanged.connect(self.setimp)


        self._layout_choose_imp.addWidget(self.label)
        self._layout_choose_imp.addWidget(self.choose_imp)
        self._layout.addLayout(self._layout_choose_imp)


        self.add_imp_param_Ui()

        self._layout.addWidget(self.imp_list_widget)
        #self.imp_list_widget.btn_add.clicked.connect(self.add_impurity_to_list)
        self.setLayout(self._layout)


    def setimp(self):
        i = self.choose_imp.currentText()
        self._hide_all_imp_params()
        self.imp_params_widgets[i].show()

    def _hide_all_imp_params(self):
        for key, value in self.imp_params_widgets.items():
            value.hide()


if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = ImpWidget()
    mw.show()
    sys.exit(app.exec())