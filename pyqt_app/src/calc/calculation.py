from PyQt6 import QtGui
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from src.calc.model import *
from src.utils.progressBar import ProgressBar

import time

class Calculation(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    time_remain = pyqtSignal(int)
    killed = pyqtSignal()

    def __init__(self, m, model_params, p, plot_params, i ,imp_params, imp_dict=None):
        super(Calculation, self).__init__()
        self.active = False
        self.m = m
        self.p = p
        self.i = i
        self.model_params = model_params
        self.plot_params = plot_params
        self.imp_params = imp_params
        self.imp_dict= imp_dict
        self.Ns = None
        self.eigenvectors_xr = None
        self.eigenvalues_xr = None

        self.points = []




    def run_phis(self):
        self.active = True
        self.started.emit()
        size_hilbert = self.model_params["L_x"] * self.model_params["L_y"]
        ds = self.plot_params["ds"]
        s_min = self.plot_params["s_min"]
        s_max = self.plot_params["s_max"]

        s_array = np.arange(s_min, s_max, ds)
        self.Ns = s_array.size


        self.eigenvalues_xr = xr.DataArray(data=np.nan * np.empty((self.Ns, size_hilbert)),
                                           coords=[("s", s_array),
                                                   ("#eval", np.arange(size_hilbert))])
        self.eigenvectors_xr = xr.DataArray(data=np.nan * np.empty((self.Ns, size_hilbert, size_hilbert)),
                                            coords=[("s", s_array),
                                                    ("#evec", np.arange(size_hilbert)),
                                                    ("dim_evec", np.arange(size_hilbert))])
        sum = 0
        i = 0
        for counter, s in enumerate(s_array):

            tic = time.time_ns()
            phi_x, phi_y = self._s_to_phis(s)
            self.points.append((phi_x, phi_y))
            h = self._build_model(phi_x=phi_x, phi_y=phi_y)
            h.set_impurities(imp_dict = self.imp_dict)
            eigvals, eigvecs = h.solve()
            self.eigenvalues_xr[counter, :] = eigvals
            self.eigenvectors_xr[counter, :, :] = eigvecs
            toc = time.time_ns()
            sum += toc-tic
            mean_time = int(sum/(counter+1))
            if i != int(100*counter/self.Ns):
                time_remain = int(mean_time*(self.Ns-counter)/1_000_000_000)
                self.progress.emit(i)
                self.time_remain.emit(time_remain)
                i += 1
            if not self.active:
                self.killed.emit()
                break

        if self.active:
            self.finished.emit()



    def stop(self):
        self.active = False


    def _s_to_phis(self, s):
        phi_x = None
        phi_y = None
        if self.plot_params["name"] == "linear":
            m_x = self.plot_params["m_x"]
            c_x = self.plot_params["c_x"]

            m_y = self.plot_params["m_y"]
            c_y = self.plot_params["c_y"]

            phi_x = m_x*s + c_x
            phi_y = m_y*s + c_y

        elif self.plot_params["name"] == "ellipse":
            a = self.plot_params["a"]
            b = self.plot_params["b"]
            x_0 = self.plot_params["x_0"]
            y_0 = self.plot_params["y_0"]

            phi_x = a*np.cos(2*np.pi*s) + x_0
            phi_y = a*np.sin(2*np.pi*s) + y_0

        return phi_x, phi_y

    def _build_model(self, phi_x, phi_y):
        model = None
        if self.m == "tight binding":
            model = TightBinding_2D(**self.model_params, phi_x=phi_x, phi_y=phi_y)

        if self.m == "two band":
            model = TwoBand_2D(**self.model_params, phi_x=phi_x, phi_y=phi_y)
        return model





    def give_list_eigenvalues(self):
        all_spots = []
        for ev in self.eigenvalues_xr:
            x = ev["s"].values*np.ones_like(ev.values)
            y = ev.values
            pos = np.column_stack((x, y))
            spots = [{'pos': pos[i], 'data': 1} for i in range(x.shape[0])]
            all_spots += spots


        return all_spots

