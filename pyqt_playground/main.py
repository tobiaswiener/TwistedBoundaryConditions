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
import inputDialog
from twistedAngleLine import TwistedAngleLine

class Widget(QtWidgets.QWidget):

    def __init__(self):
        super(Widget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.s1 = None
        self.view = None
        self.input = None
        self.button = QtWidgets.QPushButton("Button")

        self.setupUi()

        self.w1 = self.view.addPlot()
        self.w1.setMouseEnabled(x=False)
        self.view.nextRow()
        self.w2 = self.view.addPlot()




    def setupUi(self):
        self.resize(800, 800)
        self.view = pg.GraphicsLayoutWidget()
        self.input = inputDialog.inputdialogdemo()
        self._layout.addWidget(self.view)
        self._layout.addWidget(self.input)
        self.setWindowTitle('pyqtgraph example: ScatterPlot')


    def add_data(self, spots, w=0):
        plots = [self.w1, self.w2]
        w = plots[w]
        s = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        s.addPoints(spots)
        w.addItem(s)





class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = Widget()
        self.setCentralWidget(self.widget)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # app = pg.mkQApp("Scatter Plot Item Example")
    mw = MainWindow()
    mw.resize(800, 800)

    phi_x_lower = 0
    phi_x_upper = 2 * np.pi
    nphi = 1000

    phi_x_array = np.linspace(phi_x_lower, phi_x_upper, nphi)
    m = 0.
    c = 0.

    L_x = 5
    L_y = 4
    t = 1
    loc_imp = (1, 2)
    e_imp = 3

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

    mw.widget.add_data(spots, w=0)
    mw.widget.add_data(spots_imp, w=1)


    mw.show()
    sys.exit(app.exec())

