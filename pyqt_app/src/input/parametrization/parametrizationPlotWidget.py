
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import sys



class ParametrizationPlotWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout()
        self.btn_add = QtWidgets.QPushButton("add curve")
        self.btn_clear = QtWidgets.QPushButton("clear")
        self.plot_curves = pg.PlotWidget()

        self.curves = {}
        self.setupUI()



    def setupUI(self):
        self._layout.addWidget(self.btn_add,0,0,1,3)
        self._layout.addWidget(self.plot_curves,1,0,1,3)
        self._layout.addWidget(self.btn_clear,2,2)

        self.setLayout(self._layout)



    def get_parametrization(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = ParametrizationPlotWidget()
    widget.show()
    sys.exit(app.exec())
