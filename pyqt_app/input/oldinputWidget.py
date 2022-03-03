from PyQt6 import QtWidgets, QtCore


class OldInputWidget(QtWidgets.QWidget):
    sig_calc_triggered = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)

        self._layout = QtWidgets.QVBoxLayout()

        self._layout_model = QtWidgets.QFormLayout()
        self.btn_choose_model = QtWidgets.QPushButton("Choose model")
        self.le = QtWidgets.QLineEdit()

        self._layout_params = QtWidgets.QHBoxLayout()

        self._layout_plot_params = QtWidgets.QVBoxLayout()
        self.plot_params = {}
        self.init_plot_params()

        self._layout_model_params = QtWidgets.QVBoxLayout()
        self.model_params = {}
        self.init_model_params()
        self.btn_calc = QtWidgets.QPushButton("Calculate")

        self.btn_clear = QtWidgets.QPushButton("Clear")
        self.setupUi()

    def init_model_params(self):
        for m, model_dicts in MODELS.items():
            self.model_params[m] = {}
            for param, standard_value in model_dicts.items():
                self.model_params[m][param] = QtWidgets.QLineEdit(str(standard_value))

    def init_plot_params(self):
        for param, standard_value in PLOT_PARAMS.items():
            self.plot_params[param] = QtWidgets.QLineEdit(str(standard_value))

    def setupUi(self):
        self._layout_model.addRow(self.btn_choose_model, self.le)
        self._layout.addItem(self._layout_model)
        self.btn_choose_model.clicked.connect(self.setModel)

        self.setLayout(self._layout)

    def add_model_param_Ui(self, m):
        params = self.model_params[m]
        for param, lines in params.items():
            hbox = QtWidgets.QFormLayout()
            hbox.addRow(param, lines)
            self._layout_model_params.addItem(hbox)

    def add_plot_param_Ui(self):
        params = self.plot_params
        for param, lines in params.items():
            hbox = QtWidgets.QFormLayout()
            hbox.addRow(param, lines)
            self._layout_plot_params.addItem(hbox)


    def get_model_params(self):
        m = self.le.text()
        params = {}
        for key, value in self.model_params[m].items():
            params[key] = value.text()
        return m, params

    def get_plot_params(self):
        params = {}
        for key, value in self.plot_params.items():
            params[key] = value.text()
        return params


    def setModel(self):
        item, ok = QtWidgets.QInputDialog.getItem(self, "select model dialog",
                                        "list of models", MODELS, 0, False)
        if ok and item:
            self.le.setText(item)
            #self.add_plot_param_Ui()
            #self._layout_params.addItem(self._layout_model_params)
            #self._layout_params.addItem(self._layout_plot_params)
            #self._layout_params.addItem(self.btn_calc)
            #self._layout.addItem(self._layout_params)


            self.add_model_param_Ui(item)
            self.add_plot_param_Ui()
            self._layout_params.addLayout(self._layout_model_params)
            self._layout_params.addLayout(self._layout_plot_params)
            self._layout.addLayout(self._layout_params)
            self._layout.addWidget(self.btn_calc)
            self._layout.addWidget(self.btn_clear)

