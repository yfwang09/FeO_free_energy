import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from log import log as lammps_log

nlat = 5
tstep = 0.002
Tlist = [100, 400, 700, 1000, 1300, 1600]
bsize = []

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
    lx = log.get('Lx')
    ly = log.get('Ly')
    lz = log.get('Lz')
    nstep_eq = len(t) // 2
    bsize.append(np.mean(lx[nstep_eq:])/nlat)

    ax.plot(t, T, 'C%d'%i, label=f'{fT} K', linewidth=2.0)
    axl.plot(t, ly, 'C%d'%i, label=f'{fT} K', linewidth=2.0)

ax.set_xlabel('Time (ps)')
ax.set_ylabel('Temperature (K)')
axl.set_xlabel('Time (ps)')
axl.set_ylabel('lx, ly (Angstrom)')

fig1, ax1 = plt.subplots()
ax1.plot(Tlist, bsize, 'o-')
print(bsize)

plt.show()
