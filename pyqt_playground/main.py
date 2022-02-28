# -*- coding: utf-8 -*-
"""
Example demonstrating a variety of scatter plot features.
"""
import sys

from PyQt6 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
from collections import namedtuple
from itertools import chain
import inputWidget
from twistedAngleLine import TwistedAngleLine

class MainWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()

        self.plot_widget = pg.GraphicsLayoutWidget()
        self.w1 = self.plot_widget.addPlot()
        self.w2 = self.plot_widget.addPlot()



        self.input_widget = inputWidget.InputWidget()

        self.input_widget.btn_calc.clicked.connect(self.calc)
        self.input_widget.btn_clear.clicked.connect(self.clear)

        self.setupUi()

    def setupUi(self):
        self.resize(800, 800)

        self._layout.addWidget(self.plot_widget)
        self._layout.addWidget(self.input_widget)

        self.setLayout(self._layout)
        self.setWindowTitle('Twisted Boundary Conditions')



    def calc(self):

        m, model_params = self.input_widget.get_model_params()
        plot_params = self.input_widget.get_plot_params()

        L_x = int(model_params["L_x"])
        L_y = int(model_params["L_y"])
        t = float(model_params["t"])
        loc_imp = (int(model_params["loc_imp_x"]), int(model_params["loc_imp_y"]))
        e_imp = float(model_params["e_imp"])



        phi_x_lower = float(plot_params["phi_x_min"])
        phi_x_upper = float(plot_params["phi_x_max"]) * np.pi
        nphi = int(plot_params["nphi"])
        phi_x_array = np.linspace(phi_x_lower, phi_x_upper, nphi)
        m = float(plot_params["m"])
        c = float(plot_params["c"])
        ta = TwistedAngleLine(phi_x_array=phi_x_array,
                              m=m,
                              c=c,
                              L_x=L_x,
                              L_y=L_y,
                              t=t,
                              loc_imp=loc_imp,
                              e_imp=e_imp)

        ta.run_phis()

        spots, spots_imp = ta.give_list_eigenvalues()

        self.add_data(spots,w=0)
        self.add_data(spots_imp, w=1)
        self.w1.getViewBox().setXLink(view=self.w2)
        self.w2.getViewBox().setXLink(view=self.w1)
        self.w1.getViewBox().setYLink(view=self.w2)
        self.w2.getViewBox().setYLink(view=self.w1)

    def add_data(self, spots, w=0):
        plots = [self.w1, self.w2]
        w = plots[w]
        s = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        s.setSize(2)
        s.addPoints(spots)
        w.addItem(s)


    def clear(self):
        self.w1.clear()
        self.w2.clear()






class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # app = pg.mkQApp("Scatter Plot Item Example")
    mw = MainWindow()

    mw.show()
    sys.exit(app.exec())

