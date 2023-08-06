#!/usr/bin/env python3
'''parametrizations of exchange-correlation functionals.'''
import numpy as np

from .logger import log


def get_xc(xc, n, spinpol=False):
    '''Handle and get exchange-correlation functionals.

    Args:
        xc (str): Exchange and correlation identifier, separated by a comma.
        n (ndarray): Real-space electronic density.

    Keyword Args:
        spinpol (bool): Choose if a spin-polarized exchange-correlation functional will be used.

    Returns:
        tuple[ndarray, ndarray]: Exchange-correlation energy density and potential.
    '''
    xc_map = {
        'lda': 'lda_slater_x',
        'pw': 'lda_pw_c',
        'vwn': 'lda_vwn_c'
    }
    exch, corr = xc.split(',')

    # Only use non-zero values of the density
    n_nz = n[np.nonzero(n)]

    # Only import libxc interface if necessary
    if 'libxc' in xc:
        from .addons.libxc import libxc_functional

    # Handle exchange part
    if 'libxc' in exch:
        exch = exch.split(':')[1]
        ex, vx = libxc_functional(exch, n_nz, spinpol)
    else:
        # If the desired functional is not implemented use a mock functional
        try:
            f_exch = xc_map[exch]
        except KeyError:
            f_exch = 'mock_xc'
            log.warning('Use a mock functional for the exchange part.')
        if spinpol:
            f_exch = f'{f_exch}_spin'
        # FIXME: In spin-polarized calculations zeta is normally not one, only when coming from
        #        spin-unpolarized calculations
        ex, vx = eval(f_exch)(n_nz, zeta=np.ones_like(n_nz))

    # Handle correlation part
    if 'libxc' in corr:
        corr = corr.split(':')[1]
        ec, vc = libxc_functional(corr, n_nz, spinpol)
    else:
        # If the desired functional is not implemented use a mock functional
        try:
            f_corr = xc_map[corr]
        except KeyError:
            f_corr = 'mock_xc'
            log.warning('Use a mock functional for the correlation part.')
        if spinpol:
            f_corr = f'{f_corr}_spin'
        # FIXME: In spin-polarized calculations zeta is normally not one, only when coming from
        #        spin-unpolarized calculations
        ec, vc = eval(f_corr)(n_nz, zeta=np.ones_like(n_nz))

    # Use zero as the result for zero values
    exc = np.zeros_like(n)
    exc[np.nonzero(n)] = ex + ec
    vxc = np.zeros_like(n)
    vxc[np.nonzero(n)] = vx + vc
    return exc, vxc


def mock_xc(n, **kwargs):
    '''Mock exchange-correlation functional with no effect.

    Args:
        n (ndarray): Real-space electronic density.

    Returns:
        tuple[ndarray, ndarray]: Mock exchange-correlation energy density and potential.
    '''
    zeros = np.zeros_like(n)
    return zeros, zeros


mock_xc_spin = mock_xc


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_x_slater.jl
def lda_slater_x(n, alpha=2 / 3, **kwargs):
    '''Slater exchange functional (spin-paired).

    Corresponds to the functional with the label LDA_C_PW and ID 1 in LibXC.
    Reference: Phys. Rev. 81, 385.

    Args:
        n (ndarray): Real-space electronic density.

    Keyword Args:
        alpha (float): Scaling factor.

    Returns:
        tuple[ndarray, ndarray]: Exchange energy density and potential.
    '''
    third = 1 / 3
    pi34 = (3 / (4 * np.pi))**third
    f = -9 / 8 * (3 / (2 * np.pi))**(2 / 3)
    rs = pi34 / n**third

    ex = f * alpha / rs
    vx = 4 / 3 * ex
    return ex, vx


# Adapted from
# https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_x_slater_spin.jl
def lda_slater_x_spin(n, zeta, alpha=2 / 3):
    '''Slater exchange functional (spin-polarized).

    Corresponds to the functional with the label LDA_C_PW and ID 1 in LibXC.
    Reference: Phys. Rev. 81, 385.

    Args:
        n (ndarray): Real-space electronic density.
        zeta (ndarray): Relative spin polarization.

    Keyword Args:
        alpha (float): Scaling factor.

    Returns:
        tuple[ndarray, ndarray]: Exchange energy density and potential.
    '''
    third = 1 / 3
    p43 = 4 / 3
    f = -9 / 8 * (3 / np.pi)**third

    rho13p = ((1 + zeta) * n)**third
    rho13m = ((1 - zeta) * n)**third

    exup = f * alpha * rho13p
    exdw = f * alpha * rho13m
    ex = 0.5 * ((1 + zeta) * exup + (1 - zeta) * exdw)

    vxup = p43 * f * alpha * rho13p
    vxdw = p43 * f * alpha * rho13m
    return ex, [vxup, vxdw]


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_pw.jl
def lda_pw_c(n, **kwargs):
    '''Perdew-Wang parametrization of the correlation functional (spin-paired).

    Corresponds to the functional with the label LDA_C_PW and ID 12 in LibXC.
    Reference: Phys. Rev. B 45, 13244.

    Args:
        n (ndarray): Real-space electronic density.

    Returns:
        tuple[ndarray, ndarray]: PW correlation energy density and potential.
    '''
    third = 1 / 3
    pi34 = (3 / (4 * np.pi))**third
    rs = pi34 / n**third

    a = 0.031091
    a1 = 0.2137
    b1 = 7.5957
    b2 = 3.5876
    b3 = 1.6382
    b4 = 0.49294

    rs12 = np.sqrt(rs)
    rs32 = rs * rs12
    rs2 = rs**2

    om = 2 * a * (b1 * rs12 + b2 * rs + b3 * rs32 + b4 * rs2)
    olog = np.log(1 + 1 / om)
    ec = -2 * a * (1 + a1 * rs) * olog

    dom = 2 * a * (0.5 * b1 * rs12 + b2 * rs + 1.5 * b3 * rs32 + 2 * b4 * rs2)
    vc = -2 * a * (1 + 2 / 3 * a1 * rs) * olog - 2 / 3 * a * (1 + a1 * rs) * dom / (om * (om + 1))
    return ec, vc


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_pw_spin.jl
def lda_pw_c_spin(n, zeta, **kwargs):
    '''Perdew-Wang parametrization of the correlation functional (spin-polarized).

    Corresponds to the functional with the label LDA_C_PW and ID 12 in LibXC.
    Reference: Phys. Rev. B 45, 13244.

    Args:
        n (ndarray): Real-space electronic density.
        zeta (ndarray): Relative spin polarization.

    Returns:
        tuple[ndarray, ndarray]: PW correlation energy density and potential.
    '''
    third = 1 / 3
    pi34 = (3 / (4 * np.pi))**third
    rs = pi34 / n**third

    fz0 = 1.709921

    zeta2 = zeta * zeta
    zeta3 = zeta2 * zeta
    zeta4 = zeta3 * zeta
    rs12 = np.sqrt(rs)
    rs32 = rs * rs12
    rs2 = rs**2

    def pw_fit(i):
        '''Calculate correlation energies by Perdew-Wang approximation interpolation.

        Args:
            i (int): Index to choose unpolarized (0), polarized (1), or antiferromagnetic (2) fit.

        Returns:
            tuple[ndarray, ndarray]: PW fit and the derivative.
        '''
        a = (0.031091, 0.015545, 0.016887)
        a1 = (0.2137, 0.20548, 0.11125)
        b1 = (7.5957, 14.1189, 10.357)
        b2 = (3.5876, 6.1977, 3.6231)
        b3 = (1.6382, 3.3662, 0.88026)
        b4 = (0.49294, 0.62517, 0.49671)

        om = 2 * a[i] * (b1[i] * rs12 + b2[i] * rs + b3[i] * rs32 + b4[i] * rs2)
        dom = 2 * a[i] * (0.5 * b1[i] * rs12 + b2[i] * rs + 1.5 * b3[i] * rs32 + 2 * b4[i] * rs2)
        olog = np.log(1 + 1 / om)

        fit = -2 * a[i] * (1 + a1[i] * rs) * olog
        dfit = -2 * a[i] * (1 + 2 / 3 * a1[i] * rs) * olog - \
               2 / 3 * a[i] * (1 + a1[i] * rs) * dom / (om * (om + 1))
        return fit, dfit

    ecU, vcU = pw_fit(0)  # Unpolarized
    ecP, vcP = pw_fit(1)  # Polarized
    ac, dac = pw_fit(2)  # Spin stiffness

    fz = ((1 + zeta)**(4 / 3) + (1 - zeta)**(4 / 3) - 2) / (2**(4 / 3) - 2)
    ec = ecU + ac * fz * (1 - zeta4) / fz0 + (ecP - ecU) * fz * zeta4

    dfz = ((1 + zeta)**third - (1 - zeta)**third) * 4 / (3 * (2**(4 / 3) - 2))
    vcup = vcU + dac * fz * (1 - zeta4) / fz0 + (vcP - vcU) * fz * zeta4 + \
           (ac / fz0 * (dfz * (1 - zeta4) - 4 * fz * zeta3) +
           (ecP - ecU) * (dfz * zeta4 + 4 * fz * zeta3)) * (1 - zeta)
    vcdw = vcU + dac * fz * (1 - zeta4) / fz0 + (vcP - vcU) * fz * zeta4 - \
           (ac / fz0 * (dfz * (1 - zeta4) - 4 * fz * zeta3) +
           (ecP - ecU) * (dfz * zeta4 + 4 * fz * zeta3)) * (1 + zeta)
    return ec, [vcup, vcdw]


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_vwn.jl
def lda_vwn_c(n, **kwargs):
    '''Vosko, Wilk, and Nusair parametrization of the correlation functional (spin-paired).

    Corresponds to the functional with the label LDA_C_PW and ID 7 in LibXC.
    Reference: Phys. Rev. B 22, 3812.

    Args:
        n (ndarray): Real-space electronic density.

    Returns:
        tuple[ndarray, ndarray]: VWN correlation energy density and potential.
    '''
    third = 1 / 3
    pi34 = (3 / (4 * np.pi))**third
    rs = pi34 / n**third

    a = 0.0310907
    b = 3.72744
    c = 12.9352
    x0 = -0.10498

    q = np.sqrt(4 * c - b * b)
    f1 = 2 * b / q
    f2 = b * x0 / (x0 * x0 + b * x0 + c)
    f3 = 2 * (2 * x0 + b) / q
    rs12 = np.sqrt(rs)
    fx = rs + b * rs12 + c
    qx = np.arctan(q / (2 * rs12 + b))

    ec = a * (np.log(rs / fx) + f1 * qx - f2 * (np.log((rs12 - x0)**2 / fx) + f3 * qx))

    tx = 2 * rs12 + b
    tt = tx * tx + q * q
    vc = ec - rs12 * a / 6 * (2 / rs12 - tx / fx - 4 * b / tt -
         f2 * (2 / (rs12 - x0) - tx / fx - 4 * (2 * x0 + b) / tt))
    return ec, vc


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_vwn_spin.jl
def lda_vwn_c_spin(n, zeta, **kwargs):
    '''Vosko, Wilk, and Nusair parametrization of the correlation functional (spin-polarized).

    Corresponds to the functional with the label LDA_C_PW and ID 7 in LibXC.
    Reference: Phys. Rev. B 22, 3812.

    Args:
        n (ndarray): Real-space electronic density.
        zeta (ndarray): Relative spin polarization.

    Returns:
        tuple[ndarray, ndarray]: VWN correlation energy density and potential.
    '''
    third = 1 / 3
    pi34 = (3 / (4 * np.pi))**third
    rs = pi34 / n**third

    cfz = 2**(4 / 3) - 2
    cfz1 = 1 / cfz
    cfz2 = 4 / 3 * cfz1
    iddfz0 = 9 / 8 * cfz
    sqrtrs = np.sqrt(rs)
    zeta3 = zeta**3
    zeta4 = zeta3 * zeta
    trup = 1 + zeta
    trdw = 1 - zeta
    trup13 = trup**third
    trdw13 = trdw**third
    fz = cfz1 * (trup13 * trup + trdw13 * trdw - 2)  # f(zeta)
    dfz = cfz2 * (trup13 - trdw13)  # df/dzeta

    def pade_fit(i):
        '''Calculate correlation energies by Pade approximation interpolation.

        Args:
            i (int): Index to choose paramagnetic (0), ferromagnetic (1), or spin stiffness (2) fit.

        Returns:
            tuple[ndarray, ndarray]: Pade fit and the derivative.
        '''
        a = (0.0310907, 0.01554535, -0.01688686394039)
        b = (3.72744, 7.06042, 1.13107)
        c = (12.9352, 18.0578, 13.0045)
        x0 = (-0.10498, -0.325, -0.0047584)
        Q = (6.15199081975908, 4.73092690956011, 7.12310891781812)
        tbQ = (1.21178334272806, 2.98479352354082, 0.31757762321188)
        bx0fx0 = (-0.03116760867894, -0.14460061018521, -0.00041403379428)

        xx0 = sqrtrs - x0[i]
        Qtxb = Q[i] / (2 * sqrtrs + b[i])
        atg = np.arctan(Qtxb)
        fx = rs + b[i] * sqrtrs + c[i]

        fit = a[i] * (np.log(rs / fx) + tbQ[i] * atg -
              bx0fx0[i] * (np.log(xx0 * xx0 / fx) + (tbQ[i] + 4 * x0[i] / Q[i]) * atg))

        txb = 2 * sqrtrs + b[i]
        txbfx = txb / fx
        itxbQ = 1 / (txb * txb + Q[i] * Q[i])

        dfit = fit - a[i] / 3 + a[i] * sqrtrs / 6 * (txbfx + 4 * b[i] * itxbQ +
               bx0fx0[i] * (2 / xx0 - txbfx - 4 * (b[i] + 2 * x0[i]) * itxbQ))
        return fit, dfit

    ecP, vcP = pade_fit(0)  # Paramagnetic fit
    ecF, vcF = pade_fit(1)  # Ferromagnetic fit
    ac, dac = pade_fit(2)  # Spin stiffness

    ac = ac * iddfz0
    De = ecF - ecP - ac  # e_c[F] - e_c[P] - alpha_c/(ddf/ddz(z=0))
    fzz4 = fz * zeta4
    ec = ecP + ac * fz + De * fzz4

    dac = dac * iddfz0
    dec1 = vcP + dac * fz + (vcF - vcP - dac) * fzz4  # e_c-(r_s/3)*(de_c/dr_s)
    dec2 = ac * dfz + De * (4 * zeta3 * fz + zeta4 * dfz)  # de_c/dzeta

    vcup = dec1 + (1 - zeta) * dec2
    vcdw = dec1 - (1 + zeta) * dec2
    return ec, [vcup, vcdw]
