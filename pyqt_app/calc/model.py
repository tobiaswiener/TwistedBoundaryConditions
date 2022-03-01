import numpy as np
import xarray as xr
from scipy import linalg

class TightBinding_2D:
    def __init__(self, L_x, L_y, t, phi_x, phi_y):
        self.L_x = L_x
        self.L_y = L_y
        self.dim_hilbert_space = L_x*L_y

        self.t = t
        self.phi_x = phi_x
        self.phi_y = phi_y

        self.__build()
        self.eval = None
        self.evec = None

    def __build_chain(self):
        #hopping
        h = -self.t * (np.eye(self.L_x, k=1, dtype=complex) + np.eye(self.L_x, k=-1, dtype=complex))
        #twisted angle on boundaries
        h[0, -1] = -self.t * np.exp(1j * self.phi_x)
        h[-1, 0] = -self.t * np.exp(-1j * self.phi_x)
        return h

    def __build(self):
        h = np.zeros((self.dim_hilbert_space, self.dim_hilbert_space), dtype=complex)
        h_chain = self.__build_chain()
        diagonal = -self.t * np.eye(self.L_x)

        for i in range(self.L_y):
            lower = i * self.L_x
            upper = (i + 1) * self.L_x
            h[lower:upper, lower:upper] = h_chain

            if i != self.L_y - 1:
                h[lower:upper, lower + self.L_x:upper + self.L_x] = diagonal
            else:
                h[lower:upper, :self.L_x] = diagonal * np.exp(-1j * self.phi_y)

            if i != 0:
                h[lower:upper, lower - self.L_x:upper - self.L_x] = diagonal
            else:
                h[lower:upper, -self.L_x:] = diagonal * np.exp(1j * self.phi_y)
        self.matrix = h
        return h

    def __location_tuple_to_hilbert_space_index(self, loc_tuple):
        x_imp, y_imp = loc_tuple
        try:
            assert x_imp < self.L_x
            assert y_imp < self.L_y
        except AssertionError:
            print("Impurity outside of lattice")
            raise
        hilbert_space_index = x_imp + y_imp*(self.L_y-1)
        return hilbert_space_index

    def set_impurity(self, loc_tuple = (0,0), e_imp = 0):
        hilbert_index = self.__location_tuple_to_hilbert_space_index(loc_tuple=loc_tuple)
        self.matrix[hilbert_index,hilbert_index] = e_imp

    def solve(self):
        eval, evec = linalg.eigh(self.matrix)
        self.eval, self.evec = eval, evec
        return eval, evec


