import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from log import log as lammps_log

tstep = 0.002
Tlist = [100, 400, 700, 1000, 1300, 1600]
v_msd = []

fig, (ax, axl) = plt.subplots(2, 1, figsize=(6, 8), sharex=True)

for i, fT in enumerate(Tlist):
    filename = f'../data/lammps_{fT}K.log'
    if not os.path.exists(filename):
        print(f'File {filename} does not exist. Skipping.')
        continue
    try:
        log = lammps_log(filename)
    except:
        print(f'Error reading {filename}. Skipping.')
        continue

    t = np.multiply(log.get('Step'), tstep)
    T = log.get('Temp')
    msd = log.get('c_msd_Fe[4]')
    nstep_eq = len(t) // 2
    v_msd.append(np.mean(msd[nstep_eq:]))

    ax.plot(t, T, 'C%d'%i, label=f'{fT} K', linewidth=2.0)
    axl.plot(t, msd, 'C%d'%i, label=f'{fT} K', linewidth=2.0)

ax.set_xlabel('Time (ps)')
ax.set_ylabel('Temperature (K)')
axl.set_xlabel('Time (ps)')
axl.set_ylabel('lx, ly (Angstrom)')

kB = 8.617333262145e-5  # eV/K
k_val = 3*np.multiply(kB, Tlist)/v_msd
print(k_val)

fig1, ax1 = plt.subplots()
ax1.plot(Tlist, v_msd, 'o-')

fig.savefig('simulation_process.png')
fig1.savefig('spring_constant_result.png', dpi=300)
plt.close()
