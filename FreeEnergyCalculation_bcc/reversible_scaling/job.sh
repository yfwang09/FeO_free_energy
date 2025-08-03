#!/bin/bash
#SBATCH --job-name=equil
#SBATCH -G 1
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -p mc,gpu

ml chemistry lammps/20230802

# This script executes a single LAMMPS simulations.
# lammps="srun -n 1 lmp_gpu -sf gpu -pk gpu 1"
lammps="lmp"

mkdir -p data # Create directory structure for data output.

# Run job.
${lammps} -in in.lmp -log data/lammps.log -screen none -var RANDOM ${RANDOM}
