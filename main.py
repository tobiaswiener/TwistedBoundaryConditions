from twistedAngle import TwistedAngle
import numpy as np


if __name__ == '__main__':
    phi_x_lower = 0
    phi_x_upper = 2 * np.pi
    phi_y_lower = 0
    phi_y_upper = 2 * np.pi
    nphi_x = 100
    nphi_y = 1
    L_x = 30
    L_y = 30
    t = 1
    loc_imp = (3,2)
    e_imp = 3
    ta = TwistedAngle(phi_x_lower=phi_x_lower,
                      phi_x_upper=phi_x_upper,
                      phi_y_lower=phi_y_lower,
                      phi_y_upper=phi_y_upper,
                      nphi_x=nphi_x,
                      nphi_y=nphi_y,
                      L_x=L_x,
                      L_y=L_y,
                      t=t,
                      loc_imp=loc_imp,
                      e_imp=e_imp)

    ta.run_phis()
    ta.plot_eigenvalues_phi_x(phi_y_index=0)