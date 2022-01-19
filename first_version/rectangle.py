import numpy as np
from scipy import linalg
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import scipy as sp
import xarray as xr
import matplotlib.pyplot as plt

from miscs import printProgressBar

def tight_binding_hamilton_chain(L,t,phi):
    H = -t * (np.eye(L, k=1, dtype=complex) + np.eye(L, k=-1, dtype=complex))
    H[0, -1] = -t * np.exp(1j * phi)
    H[-1, 0] = -t * np.exp(-1j * phi)

    return H

def tight_binding_hamilton(t,size=(5,5), phi_x=0,phi_y=0):
    L_x,L_y = size

    H = np.zeros((L_x*L_y,L_x*L_y), dtype=complex)
    H_chain = tight_binding_hamilton_chain(L_x, t, phi=phi_x)
    diagonal = -t * np.eye(L_x)

    for i in range(L_y):
        lower = i * L_x
        upper = (i + 1) * L_x
        H[lower:upper, lower:upper] = H_chain

        if i != L_y - 1:
            H[lower:upper, lower + L_x:upper + L_x] = diagonal
        else:
            H[lower:upper, :L_x] = diagonal * np.exp(-1j * phi_y)

        if i != 0:
            H[lower:upper, lower - L_x:upper - L_x] = diagonal
        else:
            H[lower:upper, -L_x:] = diagonal * np.exp(1j * phi_y)
    return H


def run_phis(size=(5,5), t=1, epsilon=3, index_epsilon=0, phi_x_lower=0,phi_x_upper=2*np.pi,phi_y_lower=0,phi_y_upper=2*np.pi, nphi_x=100,nphi_y =100):
    L_x,L_y = size

    phi_x_array = np.linspace(phi_x_lower,phi_x_upper, nphi_x)
    phi_y_array = np.linspace(phi_y_lower,phi_y_upper, nphi_y)

    size_hilbert = L_x*L_y


    eigenvalues_numpy = np.empty((nphi_x,nphi_y,size_hilbert))
    eigenvalues_numpy[:] = np.nan
    eigenvalues_xarray = xr.DataArray(data=eigenvalues_numpy, coords=[("phi_x",phi_x_array),("phi_y",phi_y_array),("#eval",np.arange(size_hilbert))])
    eigenvectors_numpy = np.empty((nphi_x,nphi_y,size_hilbert,size_hilbert))
    eigenvectors_xarray = xr.DataArray(data=eigenvectors_numpy, coords=[("phi_x",phi_x_array),("phi_y", phi_y_array), ("#evec", np.arange(size_hilbert)),("dim_evec", np.arange(size_hilbert))])



    printProgressBar(0, nphi_x, prefix='Progress:', suffix='Complete', length=50)
    for counter_x, phi_x in enumerate(phi_x_array):
        for counter_y, phi_y in enumerate(phi_y_array):
            H = tight_binding_hamilton(size=size, t=t, phi_x=phi_x, phi_y=phi_y)
            H[index_epsilon, index_epsilon] = epsilon
            eigenvalues, eigenvectors = sp.linalg.eigh(H)
            eigenvalues_xarray[counter_x, counter_y,:] = eigenvalues
            eigenvectors_xarray[counter_x, counter_y,:,:] = eigenvectors
        printProgressBar(counter_x + 1, nphi_x, prefix='Progress:', suffix='Complete', length=50)

    return eigenvalues_xarray, eigenvectors_xarray

def plot_eigenvalues_phi_x(full_array, phi_y=0):
    eigenvalues= full_array.isel(phi_y=phi_y)

    for ev in eigenvalues:
        plt.scatter(ev["phi_x"].values*np.ones_like(ev.values), ev.values, color='black', s=0.5)

    plt.show()

