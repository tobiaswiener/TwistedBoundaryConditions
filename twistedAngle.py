import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from model import TightBinding_2D
from utils import printProgressBar



class TwistedAngle:

    def __init__(self, phi_x_lower=0, phi_x_upper=2*np.pi, phi_y_lower=0, phi_y_upper=2*np.pi, nphi_x=100, nphi_y=100, L_x=5, L_y=4, t=1):
        self.phi_x_lower = phi_x_lower
        self.phi_x_upper = phi_x_upper
        self.phi_y_lower = phi_y_lower
        self.phi_y_upper = phi_y_upper
        self.nphi_x = nphi_x
        self.nphi_y = nphi_y
        self.L_x = L_x
        self.L_y = L_y
        self.t = t

    def run_phis(self):
        phi_x_array = np.linspace(self.phi_x_lower, self.phi_x_upper, self.nphi_x)
        phi_y_array = np.linspace(self.phi_y_lower, self.phi_y_upper, self.nphi_y)

        size_hilbert = self.L_x*self.L_y


        eigenvalues_np = np.nan*np.empty((self.nphi_x, self.nphi_y, size_hilbert))
        self.eigenvalues_xr = xr.DataArray(data=eigenvalues_np, coords=[("phi_x",phi_x_array),
                                                                   ("phi_y",phi_y_array),
                                                                   ("#eval",np.arange(size_hilbert))])

        eigenvectors_np = np.nan*np.empty((self.nphi_x, self.nphi_y, size_hilbert, size_hilbert))
        self.eigenvectors_xr = xr.DataArray(data=eigenvectors_np,
                                           coords=[("phi_x", phi_x_array),
                                                   ("phi_y", phi_y_array),
                                                   ("#evec", np.arange(size_hilbert)),
                                                   ("dim_evec", np.arange(size_hilbert))])


        for counter_x, phi_x in enumerate(phi_x_array):
            for counter_y, phi_y in enumerate(phi_y_array):
                h = TightBinding_2D(L_x=self.L_x, L_y=self.L_y,phi_x=phi_x,phi_y=phi_y,t=self.t)
                eval, evec = h.solve()
                self.eigenvalues_xr[counter_x,counter_y,:] = eval
                self.eigenvectors_xr[counter_x,counter_y,:,:] = evec
            printProgressBar(counter_x + 1, self.nphi_x, prefix='Progress:', suffix='Complete', length=50)


    def plot_eigenvalues_phi_x(self, phi_y=0):
        eigenvalues = self.eigenvalues_xr.isel(phi_y=phi_y)

        for ev in eigenvalues:
            plt.scatter(ev["phi_x"].values * np.ones_like(ev.values), ev.values, color='black', s=0.5)

        plt.show()