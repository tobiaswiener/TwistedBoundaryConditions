
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from model import TightBinding_2D
from old.utils import printProgressBar


class TwistedAngleLine:
    def __init__(self, phi_x_array, m, c, L_x=5, L_y=4, t=1, loc_imp=(0, 0), e_imp=0):
        self.eigenvectors_xr_imp = None
        self.eigenvalues_xr_imp = None
        self.eigenvectors_xr = None
        self.eigenvalues_xr = None

        self.phi_x_array = phi_x_array

        self.m = m
        self.c = c

        self.nphi = self.phi_x_array.size
        self.L_x = L_x
        self.L_y = L_y
        self.t = t

        self.loc_imp = loc_imp
        self.e_imp = e_imp


    def run_phis(self):

        size_hilbert = self.L_x * self.L_y

        eigenvalues_np = np.nan * np.empty((self.nphi, size_hilbert))

        self.eigenvalues_xr = xr.DataArray(data=eigenvalues_np, coords=[("phi_x", self.phi_x_array),
                                                                   ("#eval",np.arange(size_hilbert))])

        eigenvectors_np = np.nan * np.empty((self.nphi, size_hilbert, size_hilbert))
        self.eigenvectors_xr = xr.DataArray(data=eigenvectors_np,
                                            coords=[("phi_x", self.phi_x_array),
                                                    ("#evec", np.arange(size_hilbert)),
                                                    ("dim_evec", np.arange(size_hilbert))])
        eigenvalues_np_imp = np.nan * np.empty((self.nphi, size_hilbert))
        self.eigenvalues_xr_imp = xr.DataArray(data=eigenvalues_np_imp, coords=[("phi_x", self.phi_x_array),
                                                                                ("#eval", np.arange(size_hilbert))])

        eigenvectors_np_imp = np.nan * np.empty((self.nphi, size_hilbert, size_hilbert))
        self.eigenvectors_xr_imp = xr.DataArray(data=eigenvectors_np_imp,
                                                coords=[("phi_x", self.phi_x_array),
                                                        ("#evec", np.arange(size_hilbert)),
                                                        ("dim_evec", np.arange(size_hilbert))])

        for counter_x, phi_x in enumerate(self.phi_x_array):
            phi_y = self.m * phi_x + self.c
            h = TightBinding_2D(L_x=self.L_x, L_y=self.L_y, phi_x=phi_x, phi_y=phi_y, t=self.t)
            eval, evec = h.solve()
            self.eigenvalues_xr[counter_x, :] = eval
            self.eigenvectors_xr[counter_x, :, :] = evec

            h_imp = TightBinding_2D(L_x=self.L_x, L_y=self.L_y, phi_x=phi_x, phi_y=phi_y, t=self.t)
            h_imp.set_impurity(loc_tuple=self.loc_imp, e_imp=self.e_imp)
            eval_imp, evec_imp = h_imp.solve()
            self.eigenvalues_xr_imp[counter_x, :] = eval_imp
            self.eigenvectors_xr_imp[counter_x, :, :] = evec_imp
            printProgressBar(counter_x + 1, self.nphi, prefix='Progress:', suffix='Complete', length=50)

    def give_list_eigenvalues(self):
        n = self.nphi

        all_spots = []
        all_spots_imp = []
        for ev in self.eigenvalues_xr:
            x = ev["phi_x"].values*np.ones_like(ev.values)
            y = ev.values
            pos = np.column_stack((x, y))
            spots = [{'pos': pos[i], 'data': 1} for i in range(x.shape[0])]
            all_spots += spots

        for ev in self.eigenvalues_xr_imp:
            x = ev["phi_x"].values*np.ones_like(ev.values)
            y = ev.values
            pos = np.column_stack((x, y))
            spots = [{'pos': pos[i], 'data': 1} for i in range(x.shape[0])]
            all_spots_imp += spots

        return (all_spots, all_spots_imp)

    def plot_eigenvalues_phi(self):
        fig, axs = plt.subplots(2)
        fig.set_dpi(100)
        fig.suptitle(
            f'twisted boundary for lattice of size={self.L_x, self.L_y}; hopping t={self.t}; m={self.m}; c={self.c}')

        eigenvalues = self.eigenvalues_xr
        eigenvalues_imp = self.eigenvalues_xr_imp

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

        pos = np.random.normal(size=(2, n), scale=1e-5)
        spots = [{'pos': pos[:, i], 'data': 1} for i in range(n)]

        eigenvalues = self.eigenvalues_xr.isel(phi_y=phi_x)

        for ev in eigenvalues:
            plt.scatter(ev["phi_x"].values * np.ones_like(ev.values), ev.values, color='black', s=0.5)

        plt.show()


if __name__ == '__main__':

    phi_x_lower = 0
    phi_x_upper = 2 * np.pi
    nphi = 10

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
    ta.plot_eigenvalues_phi()
