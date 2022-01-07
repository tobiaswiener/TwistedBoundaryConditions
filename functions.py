import numpy as np
from scipy import linalg
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import scipy as sp
import xarray as xr
import matplotlib.pyplot as plt

from miscs import printProgressBar


def tight_binding_hamilton(size, t, dimension=1, phi=0):
    if dimension == 1:
        H = -t * (np.eye(size, k=1, dtype=complex) + np.eye(size, k=-1, dtype=complex))
        H[0, -1] = -t * np.exp(1j * phi)
        H[-1, 0] = -t * np.exp(-1j * phi)
    elif dimension == 2:
        H = np.zeros((size ** 2, size ** 2), dtype=complex)
        H1D = tight_binding_hamilton(size, t, dimension=1, phi=phi)
        diagonal = -t * np.eye(size)
        for i in range(size):
            lower = i * size
            upper = (i + 1) * size
            H[lower:upper, lower:upper] = H1D

            if i != size - 1:
                H[lower:upper, lower + size:upper + size] = diagonal
            else:
                H[lower:upper, :size] = diagonal * np.exp(-1j * phi)

            if i != 0:
                H[lower:upper, lower - size:upper - size] = diagonal
            else:
                H[lower:upper, -size:] = diagonal * np.exp(1j * phi)
    return H


def run_phis(size=6, t=1, epsilon=3, index_epsilon=0, dimension=2, phi_lower=0,phi_upper=2*np.pi, nphi=100):
    phi_array = np.linspace(phi_lower,phi_upper, nphi)
    num_ev = size**dimension
    eigenvalues_numpy = np.empty((nphi,num_ev))
    eigenvalues_numpy[:] = np.nan
    eigenvalues_xarray = xr.DataArray(data=eigenvalues_numpy, coords=[("phi",phi_array),("ev",np.arange(size*size))])



    printProgressBar(0, nphi, prefix='Progress:', suffix='Complete', length=50)
    for counter, phi in enumerate(phi_array):
        H = tight_binding_hamilton(size=size, t=t, dimension=dimension, phi=phi)
        H[index_epsilon, index_epsilon] = epsilon
        eigenvalues, eigenvectors = sp.linalg.eigh(H)
        eigenvalues_xarray[counter,:] = eigenvalues
        printProgressBar(counter + 1, nphi, prefix='Progress:', suffix='Complete', length=50)

    return eigenvalues_xarray

def plot_eigenvalues_phi(eigenvalues):

    for ev in eigenvalues:
        plt.scatter(ev["phi"].values*np.ones_like(ev.values), ev.values, color='black', s=0.5)

    plt.show()