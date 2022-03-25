import numpy as np
import sys
import random
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from src.input.impurity.impListWidget import ImpInfoWidget
from src.input.model.modelWidget import ModelWidget
from src.input.impurity.impWidget import ImpWidget
from src.input.parametrization.parametrizationWidget import ParametrizationWidget
from src.utils.progressBar import ProgressBar

class InputWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)

        self._layout = QtWidgets.QGridLayout()

        self.model_widget = ModelWidget()

        self.plot_widget = ParametrizationWidget()
        self.imp_widget = ImpWidget()

        self.btn_calc = QtWidgets.QPushButton("Calculate")
        self.btn_kill = QtWidgets.QPushButton("Kill Calculation")
        self.btn_kill.hide()
        self.btn_clear = QtWidgets.QPushButton("Clear Plot")

        self.progress_bar = ProgressBar()
        for m in self.model_widget.model_params_widgets:
            model_params_widget = self.model_widget.model_params_widgets[m]
            model_params_widget.model_params["L_x"].editingFinished.connect(self.imp_widget.imp_list_widget.listWidget.clear)
            model_params_widget.model_params["L_y"].editingFinished.connect(self.imp_widget.imp_list_widget.listWidget.clear)
        self.model_widget.choose_model.currentTextChanged.connect(self.imp_widget.imp_list_widget.listWidget.clear)



        self.setupUi()

    def set_calc_btn(self):
        self.btn_kill.hide()
        self.btn_calc.show()
        self.progress_bar.reset()

    def set_kill_btn(self):
        self.btn_calc.hide()
        self.btn_kill.show()

    def setupUi(self):

        self._layout.addWidget(self.model_widget,0,0)
        self._layout.addWidget(self.plot_widget,0,1)
        self._layout.addWidget(self.imp_widget, 0,2)

        self._layout.addWidget(self.btn_calc,2,0)
        self._layout.addWidget(self.btn_kill,2,0)

        self._layout.addWidget(self.btn_clear,3,0)

        self._layout.addWidget(self.progress_bar,1,0)

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

    def get_parametrization_dict(self):
        pass

    def get_imp_params(self):
        i = self.imp_widget.choose_imp.currentText()
        params = self.imp_widget.imp_params_widgets[i].get_imp_params()
        return i, params

    def get_impurity_dict(self):
        occupied_impurity_dict = self.imp_widget.imp_list_widget.get_impurities()
        return occupied_impurity_dict

    def setInputEnabled(self, enabled):
        for child in self.findChildren(QtWidgets.QComboBox):
            child.setEnabled(enabled)
        for child in self.findChildren(QtWidgets.QLineEdit):
            child.setEnabled(enabled)
        for child in self.findChildren(QtWidgets.QPushButton):
            if child.text() == "Kill Calculation" or child.text() == "Clear Plot":
                continue
            child.setEnabled(enabled)

    def _s_to_phis(self, s, p, plot_params):
        phi_x = None
        phi_y = None
        p, plot_params = self.get_plot_params()
        if plot_params["name"] == "linear":
            m_x = plot_params["m_x"]
            c_x = plot_params["c_x"]

            m_y = plot_params["m_y"]
            c_y = plot_params["c_y"]

            phi_x = m_x*s + c_x
            phi_y = m_y*s + c_y

        elif plot_params["name"] == "ellipse":
            a = plot_params["a"]
            b = plot_params["b"]
            x_0 = plot_params["x_0"]
            y_0 = plot_params["y_0"]

            phi_x = a*np.cos(2*np.pi*s) + x_0
            phi_y = a*np.sin(2*np.pi*s) + y_0

        return phi_x, phi_y

    def add_curve_to_dict(self):
        p, plot_params = self.get_plot_params()

        ds = plot_params["ds"]
        s_min = plot_params["s_min"]
        s_max = plot_params["s_max"]

        s_array = np.arange(s_min, s_max, ds)
        Ns = s_array.size

        [(s, self._s_to_phis(s,p,plot_params)) for s in s_array]




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