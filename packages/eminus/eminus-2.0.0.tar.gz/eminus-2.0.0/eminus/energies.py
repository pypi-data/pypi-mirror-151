#!/usr/bin/env python3
'''Calculate different energy contributions.'''
import numpy as np
from numpy.linalg import inv
from scipy.special import erfc

from .dft import get_n_single, solve_poisson
from .xc import get_xc


class Energy:
    '''Energy class to save energy contributions in one place.'''
    __slots__ = ['Ekin', 'Eloc', 'Enonloc', 'Ecoul', 'Exc', 'Eewald', 'Esic']

    def __init__(self):
        self.Ekin = 0     # Kinetic energy
        self.Ecoul = 0    # Coulomb energy
        self.Exc = 0      # Exchange-correlation energy
        self.Eloc = 0     # Local energy
        self.Enonloc = 0  # Non-local energy
        self.Eewald = 0   # Ewald energy
        self.Esic = 0     # Self-interaction correction energy

    @property
    def Etot(self):
        '''Total energy is the sum of all energy contributions.'''
        return self.Ekin + self.Ecoul + self.Exc + self.Eloc + self.Enonloc + self.Eewald + \
               self.Esic

    def __repr__(self):
        '''Print the energies stored in the Energy object.'''
        out = ''
        for ie in self.__slots__:
            energy = eval('self.' + ie)
            if energy != 0:
                out = f'{out}{ie.ljust(8)}: {energy:+.9f} Eh\n'
        return f'{out}{"-" * 25}\nEtot    : {self.Etot:+.9f} Eh'


def get_E(scf):
    '''Calculate all energy contributions and update Atoms energies needed in one SCF step.

    Args:
        scf: SCF object.

    Returns:
        float: Total energy.
    '''
    scf.energies.Ekin = get_Ekin(scf.atoms, scf.Y)
    scf.energies.Ecoul = get_Ecoul(scf.atoms, scf.n, scf.phi)
    scf.energies.Exc = get_Exc(scf, scf.n, scf.exc)
    scf.energies.Eloc = get_Eloc(scf, scf.n)
    scf.energies.Enonloc = get_Enonloc(scf, scf.Y)
    return scf.energies.Etot


def get_Ekin(atoms, Y):
    '''Calculate the kinetic energy.

    Reference: Comput. Phys. Commun. 128, 1.

    Args:
        atoms: Atoms object.
        Y (ndarray): Expansion coefficients of orthogonal wave functions in reciprocal space.

    Returns:
        float: Kinetic energy in Hartree.
    '''
    # Ekin = -0.5 Tr(F Wdag L(W))
    return np.real(-0.5 * np.trace(np.diag(atoms.f) @ (Y.conj().T @ atoms.L(Y))))


def get_Ecoul(atoms, n, phi=None):
    '''Calculate the Coulomb energy.

    Reference: Comput. Phys. Commun. 128, 1.

    Args:
        atoms: Atoms object.
        n (ndarray): Real-space electronic density.

    Kwargs:
        phi (ndarray): Hartree ﬁeld.

    Returns:
        float: Coulomb energy in Hartree.
    '''
    if phi is None:
        phi = solve_poisson(atoms, n)
    # Ecoul = -(J(n))dag O(phi)
    return np.real(0.5 * n.conj().T @ atoms.Jdag(atoms.O(phi)))


def get_Exc(scf, n, exc=None):
    '''Calculate the exchange-correlation energy.

    Reference: Comput. Phys. Commun. 128, 1.

    Args:
        scf: SCF object.
        n (ndarray): Real-space electronic density.

    Keyword Args:
        exc (ndarray): Exchange-correlation energy density.

    Returns:
        float: Exchange-correlation energy in Hartree.
    '''
    atoms = scf.atoms
    if exc is None:
        exc = get_xc(scf.xc, n)[0]
    # Exc = (J(n))dag O(J(exc))
    return np.real(n.conj().T @ atoms.Jdag(atoms.O(atoms.J(exc))))


def get_Eloc(scf, n):
    '''Calculate the local energy contribution.

    Args:
        scf: SCF object.
        n (ndarray): Real-space electronic density.

    Returns:
        float: Local energy contribution in Hartree.
    '''
    return np.real(scf.Vloc.conj().T @ n)


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/calc_energies.jl
def get_Enonloc(scf, Y):
    '''Calculate the non-local GTH energy contribution.

    Reference: Phys. Rev. B 54, 1703.

    Args:
        scf: SCF object.
        Y (ndarray): Expansion coefficients of orthogonal wave functions in reciprocal space.

    Returns:
        float: Non-local GTH energy contribution in Hartree.
    '''
    atoms = scf.atoms
    Enonloc = 0
    if scf.NbetaNL > 0:  # Only calculate non-local potential if necessary
        Natoms = atoms.Natoms
        Nstates = atoms.Ns
        prj2beta = scf.prj2beta
        betaNL = scf.betaNL

        betaNL_psi = (Y.conj().T @ betaNL).conj()

        for ist in range(Nstates):
            enl = 0
            for ia in range(Natoms):
                psp = scf.GTH[atoms.atom[ia]]
                for l in range(psp['lmax']):
                    for m in range(-l, l + 1):
                        for iprj in range(psp['Nproj_l'][l]):
                            ibeta = prj2beta[iprj, ia, l, m + psp['lmax'] - 1] - 1
                            for jprj in range(psp['Nproj_l'][l]):
                                jbeta = prj2beta[jprj, ia, l, m + psp['lmax'] - 1] - 1
                                hij = psp['h'][l, iprj, jprj]
                                enl += hij * np.real(betaNL_psi[ist, ibeta].conj() *
                                       betaNL_psi[ist, jbeta])
            Enonloc += atoms.f[ist] * enl
    # We have to multiply with the cell volume, because of different orthogonalization methods
    return Enonloc * atoms.Omega


# Adapted from https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/calc_E_NN.jl
def get_Eewald(atoms, gcut=2, gamma=1e-8):
    '''Calculate the Ewald energy.

    Reference: J. Chem. Theory Comput. 10, 381.

    Args:
        atoms: Atoms object.

    Keyword Args:
        gcut (float): G-vector cut-off.
        gamma (float): Error tolerance

    Returns:
        float: Ewald energy in Hartree.
    '''
    # For a plane wave code we have multiple contributions for the Ewald energy
    # Namely, a sum from contributions from real-space, reciprocal space,
    # the self energy, (the dipole term [neglected]), and an additional electroneutrality term
    Natoms = atoms.Natoms
    X = atoms.X
    Z = atoms.Z
    Omega = atoms.Omega
    R = atoms.R

    t1, t2, t3 = R
    t1m = np.sqrt(t1 @ t1)
    t2m = np.sqrt(t2 @ t2)
    t3m = np.sqrt(t3 @ t3)

    g1, g2, g3 = 2 * np.pi * inv(R.conj().T)
    g1m = np.sqrt(g1 @ g1)
    g2m = np.sqrt(g2 @ g2)
    g3m = np.sqrt(g3 @ g3)

    gexp = -np.log(gamma)
    nu = 0.5 * np.sqrt(gcut**2 / gexp)

    x = np.sum(Z**2)
    totalcharge = np.sum(Z)

    # Start by calculating the self-energy
    Eewald = -nu * x / np.sqrt(np.pi)
    # Add the electroneutrality term
    Eewald += -np.pi * totalcharge**2 / (2 * Omega * nu**2)

    tmax = np.sqrt(0.5 * gexp) / nu
    mmm1 = np.rint(tmax / t1m + 1.5)
    mmm2 = np.rint(tmax / t2m + 1.5)
    mmm3 = np.rint(tmax / t3m + 1.5)

    dX = np.empty(3)
    T = np.empty(3)
    for ia in range(Natoms):
        for ja in range(Natoms):
            dX = X[ia] - X[ja]
            ZiZj = Z[ia] * Z[ja]
            for i in np.arange(-mmm1, mmm1 + 1):
                for j in np.arange(-mmm2, mmm2 + 1):
                    for k in np.arange(-mmm3, mmm3 + 1):
                        if (ia != ja) or ((abs(i) + abs(j) + abs(k)) != 0):
                            T = i * t1 + j * t2 + k * t3
                            rmag = np.sqrt(np.sum((dX - T)**2))
                            # Add the real-space contribution
                            Eewald += 0.5 * ZiZj * erfc(rmag * nu) / rmag

    mmm1 = np.rint(gcut / g1m + 1.5)
    mmm2 = np.rint(gcut / g2m + 1.5)
    mmm3 = np.rint(gcut / g3m + 1.5)

    G = np.empty(3)
    for ia in range(Natoms):
        for ja in range(Natoms):
            dX = X[ia] - X[ja]
            ZiZj = Z[ia] * Z[ja]
            for i in np.arange(-mmm1, mmm1 + 1):
                for j in np.arange(-mmm2, mmm2 + 1):
                    for k in np.arange(-mmm3, mmm3 + 1):
                        if (abs(i) + abs(j) + abs(k)) != 0:
                            G = i * g1 + j * g2 + k * g3
                            GX = np.sum(G * dX)
                            G2 = np.sum(G**2)
                            # Add the reciprocal space contribution
                            x = 2 * np.pi / Omega * np.exp(-0.25 * G2 / nu**2) / G2
                            Eewald += x * ZiZj * np.cos(GX)
    return Eewald


def get_Esic(scf, Y, n_single=None):
    '''Calculate the Perdew-Zunger self-interaction energy.

    Reference: Phys. Rev. B 23, 5048.

    Args:
        scf: SCF object.
        Y (ndarray): Expansion coefficients of orthogonal wave functions in reciprocal space.

    Keyword Args:
        n_single (ndarray): Single-electron densities.

    Returns:
        float: PZ self-interaction energy.
    '''
    atoms = scf.atoms
    # E_PZ-SIC = \sum_i Ecoul[n_i] + Exc[n_i, 0]
    if n_single is None:
        n_single = get_n_single(atoms, Y)

    Esic = 0
    for i in range(atoms.Ns):
        # Normalize single-particle densities to 1
        ni = n_single[:, i] / atoms.f[i]
        coul = get_Ecoul(atoms, ni)
        # The exchange part for a SIC correction has to be spin polarized
        xc = get_Exc(scf, ni, spinpol=True)
        # SIC energy is scaled by the occupation number
        Esic += (coul + xc) * atoms.f[i]
    scf.energies.Esic = Esic
    return Esic
