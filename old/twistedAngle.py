import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import scipy as sp

from model import TightBinding_2D
from utils import printProgressBar



class TwistedAngle:

    def __init__(self, phi_x_lower=0, phi_x_upper=2*np.pi, phi_y_lower=0, phi_y_upper=2*np.pi, nphi_x=100, nphi_y=100, L_x=5, L_y=4, t=1, loc_imp=(0,0),e_imp=0):
        self.phi_x_lower = phi_x_lower
        self.phi_x_upper = phi_x_upper
        self.phi_y_lower = phi_y_lower
        self.phi_y_upper = phi_y_upper
        self.nphi_x = nphi_x
        self.nphi_y = nphi_y
        self.L_x = L_x
        self.L_y = L_y
        self.t = t


        self.loc_imp = loc_imp
        self.e_imp = e_imp

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
        eigenvalues_np_imp = np.nan*np.empty((self.nphi_x, self.nphi_y, size_hilbert))
        self.eigenvalues_xr_imp = xr.DataArray(data=eigenvalues_np_imp, coords=[("phi_x",phi_x_array),
                                                                   ("phi_y",phi_y_array),
                                                                   ("#eval",np.arange(size_hilbert))])

        eigenvectors_np_imp = np.nan*np.empty((self.nphi_x, self.nphi_y, size_hilbert, size_hilbert))
        self.eigenvectors_xr_imp = xr.DataArray(data=eigenvectors_np_imp,
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

                h_imp = TightBinding_2D(L_x=self.L_x, L_y=self.L_y,phi_x=phi_x,phi_y=phi_y,t=self.t)
                h_imp.set_impurity(loc_tuple=self.loc_imp, e_imp=self.e_imp)
                eval_imp, evec_imp = h_imp.solve()
                self.eigenvalues_xr_imp[counter_x,counter_y,:] = eval_imp
                self.eigenvectors_xr_imp[counter_x,counter_y,:,:] = evec_imp
            printProgressBar(counter_x + 1, self.nphi_x, prefix='Progress:', suffix='Complete', length=50)



    def plot_eigenvalues_phi_x(self, phi_y_index=0):

        phi_y = self.eigenvalues_xr.coords["phi_y"].values[phi_y_index]
        fig, axs = plt.subplots(2)
        fig.suptitle(f'twisted boundary for lattice of size={self.L_x,self.L_y}; hopping t={self.t}; $\phi_y = {{{phi_y}}}$')

        eigenvalues = self.eigenvalues_xr.isel(phi_y=phi_y_index)
        eigenvalues_imp = self.eigenvalues_xr_imp.isel(phi_y=phi_y_index)

        for ev in eigenvalues:
            axs[0].scatter(ev["phi_x"].values * np.ones_like(ev.values), ev.values, color='black', s=0.5)
        for ev in eigenvalues_imp:
            axs[1].scatter(ev["phi_x"].values * np.ones_like(ev.values), ev.values, color='black', s=0.5)


        axs[0].set_title("without impurity")
        axs[0].set(xlabel=f"$\phi_x$")
        axs[1].set_title(f"with impurity with $\epsilon = {{{self.e_imp}}}$ at {self.loc_imp}")
        axs[1].set(xlabel=f"$\phi_x$")

        plt.show()

    def plot_eigenvalues_phi_y(self, phi_x=0):
        eigenvalues = self.eigenvalues_xr.isel(phi_y=phi_x)

        for ev in eigenvalues:
            plt.scatter(ev["phi_x"].values * np.ones_like(ev.values), ev.values, color='black', s=0.5)

        plt.show()