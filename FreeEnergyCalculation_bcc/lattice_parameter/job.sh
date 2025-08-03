#!/bin/bash
#SBATCH --job-name=equil
#SBATCH -G 1
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -p mc,gpu

# This script executes sequentially a series of LAMMPS simulations at different temperatures.
module purge
module load chemistry
module load lammps/20230802

# lammps="../../lammps/src/lmp_serial" # Path to LAMMPS executable.
lammps="srun -n 1 lmp_gpu -sf gpu -pk gpu 1" # Path to LAMMPS executable.

# Setup list of parameters to loop over.
T=(   100    400    700   1000   1300   1600)

mkdir -p data # Create directory structure for data output.

# Run job.
for n in $(seq 0 5)
do
  printf "Running T = ${T[n]}K simulation.\n"
  ${lammps} -in  in.anneal.npt.FeO        \
            -log data/lammps_${T[n]}K.log \
            -screen none                  \
            -var RANDOM ${RANDOM}         \
            -var T ${T[n]}                
  printf "Finished running T = ${T[n]}K simulation.\n"
done

wait
