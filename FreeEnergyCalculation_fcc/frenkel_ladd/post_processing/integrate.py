"""
  This script collects the data from forward and backward switchings and computed the absolute free energy for each temperature.

  Usage:
    python integrate.py
"""

import os
os.chdir(os.path.dirname(__file__))
from numpy import *
import scipy.constants as sc

# Input parameters.
T = array([100,400,700,1000,1300,1600]) # [K].
# a = array([2.8841,2.9115,2.9315,2.9484,2.9637,2.9782]) # [A].
# k = array([5.787,4.866,4.073,3.373,2.799,2.443]) # [eV/A^2].
a = array([3.65115, 3.66284, 3.67454, 3.68485, 3.69339, 3.70129]) # [A].
k = array([6.05708571, 5.92721161, 5.55444079, 5.47308567, 5.42595292, 5.31114955]) # [eV/A^2].
m = 55.845 # Iron mass [g/mol].
natoms = 500 # Number of atoms.

# Physical constants.
kB = sc.value('Boltzmann constant in eV/K')
eV = sc.value('electron volt')
hbar = sc.value('Planck constant in eV/Hz') / (2*pi) # [eV*s].
mu = sc.value('atomic mass constant')

################################################################################
# Lambda integration [Eq.(12) in the paper].
################################################################################

W = zeros(len(T)) # Reversible work for each temperature.
for i in range(len(T)):
  # Forward integration.
  dE, lamb = loadtxt('../data/forward_%dK.dat' % T[i], unpack=True)
  I_forw = trapz(dE,lamb)
  # Backward integration.
  dE, lamb = loadtxt('../data/backward_%dK.dat' % T[i], unpack=True)
  I_back = trapz(dE,lamb)
  # Compute reversible work.
  W[i] = (I_forw-I_back) / 2

################################################################################
# Compute free energy.
################################################################################

# Define harmonic reference system free energy [Eq.(15) in the paper].
omega = sqrt(k*eV/(m*mu)) * 1.0e+10 # [1/s].
F_harm = 3*natoms*kB*T * log(hbar*omega/(kB*T)) # [eV].

# Fixed center of mass correction [Eq.(24) in the paper].
V = (a**3/2) * natoms # Total volume.
F_CM = (kB*T)*log((natoms/V) * (2*pi*kB*T / (natoms*k))**(3/2)) # [eV].

# Compute absolute free energy per atom [Eq.(16) in the paper] and save data.
F = (F_harm + W + F_CM) / natoms # [eV/atom].
savetxt('../data/free_energy.dat', transpose([T,F]),
        header='T [K] F [eV/atom]', fmt='%4d %.4f')

################################################################################
