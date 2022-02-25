from PyQt6 import QtGui, QtCore, QtWidgets


class ParameterDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        e1 = QtWidgets.QLineEdit("1.")

        e2 = QtWidgets.QLineEdit("0.")

        e3 = QtWidgets.QLineEdit("2.")

        e4 = QtWidgets.QLineEdit("1000")

        e5 = QtWidgets.QLineEdit("0.5")

        e6 = QtWidgets.QLineEdit("0.")

        flo = QtWidgets.QFormLayout()
        flo.addRow("t", e1)
        flo.addRow("phi_x_lower", e2)
        flo.addRow("phi_x_upper", e3)
        flo.addRow("nphi", e4)
        flo.addRow("m", e5)
        flo.addRow("c", e6)

        self.setLayout(flo)
        self.setWindowTitle("QLineEdit Example")

