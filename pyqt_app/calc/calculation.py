import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import scipy as sp
from pyqt_app.calc.model import *

from pyqt_app.ParameterDicts import *


class Calculation:
    def __init__(self, m, model_params, p, plot_params, i ,imp_params):
        self.m = m
        self.p = p
        self.i = i
        self.model_params = model_params
        self.plot_params = plot_params
        self.imp_params = imp_params

        self.Ns = None
        self.eigenvectors_xr = None
        self.eigenvalues_xr = None

        self.imp_sites = []
        self.imp_energies = []
        self.imp_indices = []
        self._make_impurities()

        self.points = []

    def run_phis(self):
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


        for counter, s in enumerate(s_array):
            phi_x, phi_y = self._s_to_phis(s)
            self.points.append((phi_x, phi_y))
            h = self._build_model(phi_x=phi_x, phi_y=phi_y)
            h.set_impurities(imp_indices=self.imp_indices, imp_energies=self.imp_energies)
            eigvals, eigvecs = h.solve()
            self.eigenvalues_xr[counter, :] = eigvals
            self.eigenvectors_xr[counter, :, :] = eigvecs

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

    def __location_tuple_to_hilbert_space_index(self, loc_tuple):
        x, y = loc_tuple

        try:
            assert x < self.model_params["L_x"]
            assert y < self.model_params["L_y"]
        except AssertionError:
            print("location outside of lattice")
            raise
        hilbert_space_index = x + y*(self.model_params["L_y"]-1)
        return hilbert_space_index

    def _make_impurities(self):
        all_sites = []
        imp_sites = []
        imp_energies = []
        imp_indices = []
        if self.i == "uniform":
            a = self.imp_params["a"]
            b = self.imp_params["b"]
            N = self.imp_params["N"]
            for x in range(self.model_params["L_x"]):
                for y in range(self.model_params["L_y"]):
                    all_sites.append((x,y))
            for i in range(N):
                site = random.choice(all_sites)
                all_sites.remove(site)
                imp_sites.append(site)
                imp_indices.append(self.__location_tuple_to_hilbert_space_index(site))
                energy = np.random.uniform(a, b)
                imp_energies.append(energy)

        self.imp_sites = imp_sites
        self.imp_indices = imp_indices
        self.imp_energies = imp_energies



    def give_list_eigenvalues(self):
        all_spots = []
        for ev in self.eigenvalues_xr:
            x = ev["s"].values*np.ones_like(ev.values)
            y = ev.values
            pos = np.column_stack((x, y))
            spots = [{'pos': pos[i], 'data': 1} for i in range(x.shape[0])]
            all_spots += spots


        return all_spots


