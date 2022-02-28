from PyQt6 import QtGui, QtCore, QtWidgets


TIGHT_BINDING_PARAMETER_DICT = dict({"L_x": 5, "L_y":6, 't': 1.0, "N_imp": 1})
TWO_BAND_ISOLATOR_PARAMETER_DICT = dict({"L_x": 5, "L_y":6, 't': 1.0, "V_1":1., "V_2":2.})

class ParameterDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QtWidgets.QFormLayout()

        self.parameter_lines = {}

        self.btn = QtWidgets.QPushButton("Calculate")

        self._layout.addRow(self.btn)

        self.setLayout(self._layout)


    def set_model(self, m):
        if m == "tight binding" or m==None:
            for param, standard_value in TIGHT_BINDING_PARAMETER_DICT.items():
                self.parameter_lines[param] = QtWidgets.QLineEdit(str(standard_value))
                self._layout.addRow(param, self.parameter_lines[param])


    def getParams(self):
        param_dict = {}
        for key, value in self.parameter_lines.items():
            param_dict[key] = value.text()
        return param_dict

