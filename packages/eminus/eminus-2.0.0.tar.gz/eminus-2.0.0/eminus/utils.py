#!/usr/bin/env python3
'''Linear algebra calculation utilities.'''
import numpy as np
from numpy.linalg import norm

from .logger import log


def diagprod(a, B):
    '''Efficiently calculate the expression Diag(a) * B.

    Args:
        a (ndarray): Single vector.
        B (ndarray): Matrix.

    Returns:
        ndarray: The expressions result.
    '''
    # Reshape a to a column vector
    a_col = a[:, None]
    return a_col * B


def dotprod(a, b):
    '''Efficiently calculate the expression a * b.

    Add an extra check to make sure the result is never zero since this function is used as a
    denominator in minimizers.

    Args:
        a (ndarray): Array of vectors.
        b (ndarray): Array of vectors.

    Returns:
        float: The expressions result
    '''
    eps = 1e-15  # 2.22e-16 is the range of float64 machine precision
    res = np.real(np.trace(a.conj().T @ b))
    if abs(res) < eps:
        return eps
    return res


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/Ylm_real.jl
def Ylm_real(l, m, R):
    '''Calculate spherical harmonics.

    Args:
        l (int): Angular momentum number.
        m (int): Magnetic quantum number.
        R (ndarray): Real-space position vector or array of real-space position vectors.

    Returns:
        ndarray: Spherical harmonics.
    '''
    # Account for single vectors
    if R.ndim == 1:
        R = np.array([R])

    # No need to calculate more for l=0
    if l == 0:
        return 0.5 * np.sqrt(1 / np.pi) * np.ones(len(R))

    # Account for small norm, if norm(R) < eps: cost=0
    eps = 1e-9
    Rmod = norm(R, axis=1)
    cost = np.zeros(len(R))
    cost_idx = Rmod > eps
    cost[cost_idx] = R[cost_idx, 2] / Rmod[cost_idx]

    # Vectorized version of sqrt(max(0, 1-cost^2))
    sint = np.sqrt(np.amax([np.zeros(len(R)), 1 - cost**2], axis=0))

    # If Rx=0: phi=pi/2*sign(Ry)
    phi = -np.pi / 2 * np.ones(len(R))
    phi_idx = R[:, 1] >= 0
    phi[phi_idx] = np.pi / 2 * np.ones(len(phi[phi_idx]))

    # Beware the arctan, it is defined with modulo pi
    phi_idx = R[:, 0] < -eps
    phi[phi_idx] = np.arctan(R[phi_idx, 1] / R[phi_idx, 0]) + np.pi
    phi_idx = R[:, 0] > eps
    phi[phi_idx] = np.arctan(R[phi_idx, 1] / R[phi_idx, 0])

    if l == 1:
        if m == -1:   # py
            ylm = 0.5 * np.sqrt(3 / np.pi) * sint * np.sin(phi)
        elif m == 0:  # pz
            ylm = 0.5 * np.sqrt(3 / np.pi) * cost
        elif m == 1:  # px
            ylm = 0.5 * np.sqrt(3 / np.pi) * sint * np.cos(phi)
        else:
            log.error(f'No definition found for Ylm({l}, {m})')
    elif l == 2:
        if m == -2:    # dxy
            ylm = np.sqrt(15 / 16 / np.pi) * sint**2 * np.sin(2 * phi)
        elif m == -1:  # dyz
            ylm = np.sqrt(15 / 4 / np.pi) * cost * sint * np.sin(phi)
        elif m == 0:   # dz2
            ylm = 0.25 * np.sqrt(5 / np.pi) * (3 * cost**2 - 1)
        elif m == 1:   # dxz
            ylm = np.sqrt(15 / 4 / np.pi) * cost * sint * np.cos(phi)
        elif m == 2:   # dx2-y2
            ylm = np.sqrt(15 / 16 / np.pi) * sint**2 * np.cos(2 * phi)
        else:
            log.error(f'No definition found for Ylm({l}, {m})')
    elif l == 3:
        if m == -3:
            ylm = 0.25 * np.sqrt(35 / 2 / np.pi) * sint**3 * np.sin(3 * phi)
        elif m == -2:
            ylm = 0.25 * np.sqrt(105 / np.pi) * sint**2 * cost * np.sin(2 * phi)
        elif m == -1:
            ylm = 0.25 * np.sqrt(21 / 2 / np.pi) * sint * (5 * cost**2 - 1) * np.sin(phi)
        elif m == 0:
            ylm = 0.25 * np.sqrt(7 / np.pi) * (5 * cost**3 - 3 * cost)
        elif m == 1:
            ylm = 0.25 * np.sqrt(21 / 2 / np.pi) * sint * (5 * cost**2 - 1) * np.cos(phi)
        elif m == 2:
            ylm = 0.25 * np.sqrt(105 / np.pi) * sint**2 * cost * np.cos(2 * phi)
        elif m == 3:
            ylm = 0.25 * np.sqrt(35 / 2 / np.pi) * sint**3 * np.cos(3 * phi)
        else:
            log.error(f'No definition found for Ylm({l}, {m})')
    else:
        log.error(f'No definition found for Ylm({l}, {m})')
    return ylm
