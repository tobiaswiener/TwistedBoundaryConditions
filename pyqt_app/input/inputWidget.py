import numpy as np
from PyQt6 import QtWidgets, QtCore
import sys

from PyQt6.QtWidgets import QMessageBox

from pyqt_app.ParameterDicts import *
from pyqt_app.input.modelWidget import ModelWidget
from pyqt_app.input.impWidget import ImpWidget
from pyqt_app.input.impListWidget import *

from pyqt_app.input.plotWidget import PlotWidget
import random
class InputWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)

        self._layout = QtWidgets.QGridLayout()

        self.model_widget = ModelWidget()

        self.plot_widget = PlotWidget()
        self.imp_widget = ImpWidget()

        self.btn_calc = QtWidgets.QPushButton("Calculate")
        self.btn_clear = QtWidgets.QPushButton("Clear")

        for m in self.model_widget.model_params_widgets:
            model_params_widget = self.model_widget.model_params_widgets[m]
            model_params_widget.model_params["L_x"].editingFinished.connect(self.imp_widget.imp_list_widget.listWidget.clear)
            model_params_widget.model_params["L_y"].editingFinished.connect(self.imp_widget.imp_list_widget.listWidget.clear)
        self.model_widget.choose_model.currentTextChanged.connect(self.imp_widget.imp_list_widget.listWidget.clear)



        self.setupUi()



    def setupUi(self):

        self._layout.addWidget(self.model_widget,0,0)
        self._layout.addWidget(self.plot_widget,0,1)
        self._layout.addWidget(self.imp_widget, 0,2)

        self._layout.addWidget(self.btn_calc,1,0)
        self._layout.addWidget(self.btn_clear,2,0)


        self.imp_widget.imp_list_widget.btn_add.clicked.connect(self.add_impurity_to_list)


        self.setLayout(self._layout)

    def get_model_params(self):
        m = self.model_widget.choose_model.currentText()
        params = self.model_widget.model_params_widgets[m].get_model_params()
        return m, params

    def get_plot_params(self):
        p = self.plot_widget.choose_plot.currentText()
        params = self.plot_widget.plot_params_widgets[p].get_plot_params()
        return p, params

    def get_imp_params(self):
        i = self.imp_widget.choose_imp.currentText()
        params = self.imp_widget.imp_params_widgets[i].get_imp_params()
        return i, params

    def get_impurity_dict(self):
        occupied_impurity_dict = self.imp_widget.imp_list_widget.get_impurities()
        return occupied_impurity_dict




    def add_impurity_to_list(self):
        i = self.imp_widget.choose_imp.currentText()
        occupied_impurity_dict = self.imp_widget.imp_list_widget.get_impurities()
        m, params = self.get_model_params()
        L_x = params["L_x"]
        L_y = params["L_y"]

        if i == "individual":
            x = int(self.imp_widget.imp_params_widgets[i].imp_params["x"].text())
            y = int(self.imp_widget.imp_params_widgets[i].imp_params["y"].text())
            energy = float(self.imp_widget.imp_params_widgets[i].imp_params["energy"].text())
            if (x,y) in occupied_impurity_dict:
                self._show_dialog("occupied", x=x, y=y, energy=energy)
            elif x >= L_x or y >= L_y:
                self._show_dialog("lattice size", x=x, y=y, L_x=L_x, L_y=L_y)
            else:
                item = ImpInfoWidget(x, y, energy)
                self.imp_widget.imp_list_widget.listWidget.addItem(item)


        elif i == "uniform":
            all_sites = []

            N = int(self.imp_widget.imp_params_widgets[i].imp_params["N"].text())
            a = float(self.imp_widget.imp_params_widgets[i].imp_params["a"].text())
            b = float(self.imp_widget.imp_params_widgets[i].imp_params["b"].text())
            for x in range(L_x):
                for y in range(L_y):
                    all_sites.append((x, y))
            for occ_site in occupied_impurity_dict:
                all_sites.remove(occ_site)

            for i in range(N):
                if len(all_sites) == 0:
                    self._show_dialog("full")
                    break
                site = random.choice(all_sites)
                all_sites.remove(site)
                energy = format(np.random.uniform(a, b), ".2f")

                item = ImpInfoWidget(site[0],site[1], energy)
                self.imp_widget.imp_list_widget.listWidget.addItem(item)


    def _show_dialog(self, text=None, x=None, y=None,L_x=None, L_y=None, energy=None):
        msg = QMessageBox()
        if text =="occupied":
            msg.setText("This site is already occupied.")
            msg.setInformativeText(f"site ({x},{y}) with e_imp={energy}")
        elif text=="lattice size":
            msg.setText("This site is not on the lattice.")
            msg.setInformativeText(f"impurity ({x},{y}) on ({L_x},{L_y}) lattice.")
        elif text == "full":
            msg.setText("Lattice is full.")

        msg.setWindowTitle("MessageBox demo")

        retval = msg.exec()





if __name__ == '__main__':


    app = QtWidgets.QApplication([])
    #app = pg.mkQApp("Scatter Plot Item Example")

    mw = InputWidget()
    mw.show()
    sys.exit(app.exec())