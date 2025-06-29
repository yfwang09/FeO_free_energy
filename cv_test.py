# %%
# Test the collective variable (CV) for bcc and fcc structures

import os
from ase.build import bulk
import numpy as np
from ase.io import write, read
from ase.neighborlist import NeighborList, natural_cutoffs

from scipy.special import sph_harm

os.makedirs('configurations', exist_ok=True)

# generate a fcc iron supercell
# https://next-gen.materialsproject.org/materials/mp-150
n = 10
atoms = bulk('Fe', 'fcc', a=3.66, cubic=True) * (n, n, n)
fcc_file = 'configurations/fcc_iron.xyz'
if not os.path.exists(fcc_file):
    write('configurations/fcc_iron.xyz', atoms)
    write('configurations/fcc_iron.lmp', atoms, format='lammps-data',)

# generate a bcc iron supercell
# https://next-gen.materialsproject.org/materials/mp-13
atoms = bulk('Fe', 'bcc', a=2.87, cubic=True) * (n, n, n)
bcc_file = 'configurations/bcc_iron.xyz'
if not os.path.exists(bcc_file):
    write('configurations/bcc_iron.xyz', atoms)
    write('configurations/bcc_iron.lmp', atoms, format='lammps-data')

# %%
# create a neighbor list

# atoms = read('fcc_iron.xyz')
atoms = read('bcc_iron.xyz')

# Filter out non-iron atoms (for oxide structures later)
symbols = atoms.get_chemical_symbols()
fe_idx = [i for i,s in enumerate(symbols) if s == 'Fe']

# natural cutoff RADIUS of each atom
cutoffs = natural_cutoffs(atoms, mult=1.15)
print("Natural cutoffs:", cutoffs)

# NeighborList based on overlapping sphere method
nl = NeighborList(cutoffs, skin=0.0, bothways=True, self_interaction=False)

nl.update(atoms) # update the neighbor list

# Examine the neighbor list for the first 3 atoms
for i in range(3):
    idx, offsets = nl.get_neighbors(i)
    print(f"Atom {i} has {len(idx)} neighbors")

    for j, (neighbor_idx, offset) in enumerate(zip(idx, offsets)):
        print(f"  Neighbor {j}: Atom {neighbor_idx}, Offset: {offset}")

# %%
# compute the q6 order parameter for each atom
l       = 6
m_vals  = np.arange(-l, l+1)              # m = -6 ... 6
pref    = 4.0 * np.pi / (2*l + 1)         # 4π/13
cell    = atoms.get_cell()                # for PBC shift

q6_all  = np.zeros(len(fe_idx))           # for saving q6

for i, atom_idx in enumerate(fe_idx):
    # get the neighbors of the i-th atom
    idx, offsets = nl.get_neighbors(atom_idx)
    
    # calculate the spherical harmonics for each neighbor
    pbc_shift = offsets @ cell
    r_vec = atoms.get_positions()[idx] - atoms.get_positions()[atom_idx] + pbc_shift
    r_norm = np.linalg.norm(r_vec, axis=1)
    
    # compute the spherical harmonics for each neighbor
    theta = np.arccos(r_vec[:, 2] / r_norm)  # polar angle
    phi = np.arctan2(r_vec[:, 1], r_vec[:, 0])  # azimuthal angle

    qlm = np.zeros((len(idx), len(m_vals)), dtype=complex) # (n_neighbors, 2l+1)
    for k, m in enumerate(m_vals):
        qlm[:, k] = sph_harm(m, l, phi, theta)
    qlm = np.sum(qlm, axis=0) / len(idx) # (2l+1, )

    # compute the q6 order parameter
    q6_all[i] = np.sqrt(pref * np.sum(np.abs(qlm)**2))

    print(f"Atom {atom_idx} has q6 = {q6_all[i]}")


# %%
