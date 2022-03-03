from PyQt6 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from twistedAngleLine import TwistedAngleLine
from pyqt_app.input.inputWidget import InputWidget
from pyqt_app.calc.calculation import Calculation
import numpy as np
from functools import partial


class MainWidget(QtWidgets.QWidget):

    def __init__(self, Nw=2):
        super().__init__()
        self._layout = QtWidgets.QGridLayout()

        self.Nw = 2
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.w = {}
        self.input_widget = {}
        self.spots = {}
        for i in range(self.Nw):
            self.w[i] = self.plot_widget.addPlot()
            self.input_widget[i] = InputWidget()
            self.spots[i] = []



        self.setupUi()

    def setupUi(self):
        self.resize(800, 800)
        self._layout.addWidget(self.plot_widget, 0,0,1,self.Nw)

        for i in range(self.Nw):
            self._layout.addWidget(self.input_widget[i],1,i)
            self.input_widget[i].btn_calc.clicked.connect(partial(self.calc, i))
            self.input_widget[i].btn_clear.clicked.connect(partial(self.clear, i))

        self._link_views()
        self.setLayout(self._layout)
        self.setWindowTitle('Twisted Boundary Conditions')



    def calc(self, i):
        m, model_params = self.input_widget[i].get_model_params()
        p, plot_params = self.input_widget[i].get_plot_params()
        im, imp_params = self.input_widget[i].get_imp_params()

        calculation = Calculation(m, model_params, p, plot_params, im, imp_params)
        calculation.run_phis()

        new_spots = calculation.give_list_eigenvalues()

        all_spots_empty = self._all_spots_empty()
        self.spots[i].extend(new_spots)
        self.add_spots_to_plot(i, new_spots)

        if all_spots_empty:
            self.w[i].getViewBox().autoRange()

    def _all_spots_empty(self):
        all_empty = True
        for s in self.spots.values():
            if s:
                all_empty = False
            else:
                pass
        return all_empty

    def _link_views(self):
        for i in range(self.Nw):
            self.w[i].getViewBox().setXLink(view=self.w[(i+1)%self.Nw])
            self.w[i].getViewBox().setYLink(view=self.w[(i+1)%self.Nw])


    def add_spots_to_plot(self, i, new_spots):
        s = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        s.setSize(2)
        s.addPoints(new_spots)
        self.w[i].addItem(s)

    def refresh_plot(self, i):
        s = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        s.setSize(2)
        s.addPoints(self.spots[i])
        self.w[i].clear()
        self.w[i].addItem(s)


    def clear(self, i):
            self.w[i].clear()
            self.spots[i] = []


