"""
  This script plots the free energy vs temperature computed using the Frenkel-Ladd and the Reversible Scaling methods.

  Usage:
    python plot.py
"""

import os
os.chdir(os.path.dirname(__file__))
from numpy import *
import matplotlib.pyplot as plt                 
c = ['#E41A1C','#377EB8','#4DAF4A','#984EA3','#FF7F00','#FFFF33','#A65628','#F781BF','#999999']

################################################################################
# Load data.                                                                   #
################################################################################

T_rs, F_rs = loadtxt('../data/free_energy.dat', unpack=True)
T_fl, F_fl = loadtxt('../../frenkel_ladd/data/free_energy.dat', unpack=True, usecols=[0,1])
T_fl_bcc, F_fl_bcc = loadtxt('../../../FreeEnergyCalculation_bcc/frenkel_ladd/data/free_energy.dat', unpack=True, usecols=[0,1])
T_rs_bcc, F_rs_bcc = loadtxt('../../../FreeEnergyCalculation_bcc/reversible_scaling/data/free_energy.dat', unpack=True)

################################################################################
# Plot.                                                                        #
################################################################################

# Start figure.
fig = plt.figure()
ax = fig.add_axes([0.15,0.15,0.80,0.80])

# Plot.
# ax.plot(T_rs, F_rs, '-', c='k', lw=1, label='Reversible Scaling')
# ax.plot(T_fl, F_fl, 'o', c=c[0], label='Frenkel-Ladd')
# ax.plot(T_rs_bcc, F_rs_bcc, '-', c='C0', lw=1, label='RS bcc')
# ax.plot(T_fl_bcc, F_fl_bcc, 'oC1', label='FL bcc')
ax.plot(T_rs, F_rs_bcc - F_rs, '-C0', label='RS diff')
ax.plot(T_fl, F_fl_bcc - F_fl, 'oC1', label='FL diff')


# Add details and save figure.
ax.set_xlabel(r'Temperature [K]')
ax.set_ylabel(r'Free energy [eV/atom]')
ax.legend(loc='best', frameon=False)
fig.savefig("fig_free_energy_vs_temperature.png", dpi=300)
plt.close()

################################################################################
