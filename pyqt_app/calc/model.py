import numpy as np
import xarray as xr
from scipy import linalg
import random
class TightBinding_2D:
    def __init__(self, L_x, L_y, t, phi_x, phi_y, BC_x, BC_y):
        self.L_x = L_x
        self.L_y = L_y
        self.dim_hilbert_space = L_x*L_y

        self.t = t
        self.phi_x = phi_x
        self.phi_y = phi_y

        self.BC_x = BC_x
        self.BC_y = BC_y

        self.__build()
        self.eval = None
        self.evec = None

    def __build_chain(self):
        #hopping
        h = -self.t * (np.eye(self.L_x, k=1, dtype=complex) + np.eye(self.L_x, k=-1, dtype=complex))
        #boundary conditions x
        if self.BC_x == "twisted":
            boundary_matrix_element_x = -self.t * np.exp(1j * np.pi * self.phi_x)
        elif self.BC_x == "periodic":
            boundary_matrix_element_x = -self.t
        else:
            #open bc
            boundary_matrix_element_x = 0.
        h[0, -1] = boundary_matrix_element_x
        h[-1, 0] = boundary_matrix_element_x.conjugate()

        return h

    def __build(self):
        h = np.zeros((self.dim_hilbert_space, self.dim_hilbert_space), dtype=complex)
        h_chain = self.__build_chain()
        diagonal = -self.t * np.eye(self.L_x)

        #boundary conditions y
        if self.BC_y == "twisted":
            boundary_matrix_element_y = -self.t * np.exp(1j * np.pi * self.phi_y)
        elif self.BC_y == "periodic":
            boundary_matrix_element_y = -self.t
        else:
            #open bc
            boundary_matrix_element_y = 0.



        for i in range(self.L_y):
            lower = i * self.L_x
            upper = (i + 1) * self.L_x
            h[lower:upper, lower:upper] = h_chain

            if i != self.L_y - 1:
                h[lower:upper, lower + self.L_x:upper + self.L_x] = diagonal
            else:
                h[lower:upper, :self.L_x] = diagonal * boundary_matrix_element_y

            if i != 0:
                h[lower:upper, lower - self.L_x:upper - self.L_x] = diagonal
            else:
                h[lower:upper, -self.L_x:] = diagonal * boundary_matrix_element_y.conjugate()
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

    def set_impurities(self, imp_indices, imp_energies):
        for index, energy in zip(imp_indices, imp_energies):
            self.matrix[index,index] = energy


    def solve(self):
        eval, evec = linalg.eigh(self.matrix)
        self.eval, self.evec = eval, evec
        return eval, evec





class TwoBand_2D:
    def __init__(self, L_x, L_y, t, V_1, V_2, phi_x, phi_y, BC_x, BC_y):
        self.L_x = L_x
        self.L_y = L_y
        self.dim_hilbert_space = L_x*L_y

        self.t = t
        self.V_1 = V_1
        self.V_2 = V_2

        self.phi_x = phi_x
        self.phi_y = phi_y

        self.BC_x = BC_x
        self.BC_y = BC_y

        self.__build()
        self.eval = None
        self.evec = None

    def __build_chain(self):
        #hopping
        h = -self.t * (np.eye(self.L_x, k=1, dtype=complex) + np.eye(self.L_x, k=-1, dtype=complex))
        #boundary conditions x
        if self.BC_x == "twisted":
            boundary_matrix_element_x = -self.t * np.exp(1j * np.pi * self.phi_x)
        elif self.BC_x == "periodic":
            boundary_matrix_element_x = -self.t
        else:
            #open bc
            boundary_matrix_element_x = 0.
        h[0, -1] = boundary_matrix_element_x
        h[-1, 0] = boundary_matrix_element_x.conjugate()

        return h

    def __build(self):
        h = np.zeros((self.dim_hilbert_space, self.dim_hilbert_space), dtype=complex)
        h_chain = self.__build_chain()
        diagonal = -self.t * np.eye(self.L_x)

        #boundary conditions y
        if self.BC_y == "twisted":
            boundary_matrix_element_y = -self.t * np.exp(1j * np.pi * self.phi_y)
        elif self.BC_y == "periodic":
            boundary_matrix_element_y = -self.t
        else:
            #open bc
            boundary_matrix_element_y = 0.



        for i in range(self.L_y):
            lower = i * self.L_x
            upper = (i + 1) * self.L_x
            h[lower:upper, lower:upper] = h_chain

            if i != self.L_y - 1:
                h[lower:upper, lower + self.L_x:upper + self.L_x] = diagonal
            else:
                h[lower:upper, :self.L_x] = diagonal * boundary_matrix_element_y

            if i != 0:
                h[lower:upper, lower - self.L_x:upper - self.L_x] = diagonal
            else:
                h[lower:upper, -self.L_x:] = diagonal * boundary_matrix_element_y.conjugate()
        h = self._set_alternating_potential(h)
        self.matrix = h

        return h

    def _set_alternating_potential(self, h):
        for x in range(self.L_x):
            for y in range(self.L_y):
                if (x % 2 == 0 and y % 2 == 0):
                    V = self.V_1
                elif (x % 2 != 0 and y % 2 != 0):
                    V = self.V_1
                else:
                    V = self.V_2
                hilbert_index = self.__location_tuple_to_hilbert_space_index((x,y))
                h[hilbert_index,hilbert_index] = V
        return h

    def __location_tuple_to_hilbert_space_index(self, loc_tuple):
        x, y = loc_tuple
        try:
            assert x < self.L_x
            assert y < self.L_y
        except AssertionError:
            print("location outside of lattice")
            raise
        hilbert_space_index = x + y*(self.L_y-1)
        return hilbert_space_index

    def set_impurity(self, loc_tuple = (0,0), e_imp = 0):
        hilbert_index = self.__location_tuple_to_hilbert_space_index(loc_tuple=loc_tuple)
        self.matrix[hilbert_index,hilbert_index] = e_imp

    def set_impurities(self, imp_indices, imp_energies):
        for index, energy in zip(imp_indices, imp_energies):
            self.matrix[index,index] = energy

    def solve(self):
        eval, evec = linalg.eigh(self.matrix)
        self.eval, self.evec = eval, evec
        return eval, evec



