#!/bin/bash
#SBATCH --job-name=equil
#SBATCH -G 1
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -p mc,gpu

# This script executes sequentially a series of LAMMPS simulations at different temperatures.
ml chemistry lammps/20230802

# lammps="../../lammps/src/lmp_serial" # Path to LAMMPS executable.
lammps="srun -n 1 lmp_gpu -sf gpu -pk gpu 1" # Path to LAMMPS executable.

# Setup list of parameters to loop over.
T=(   100    400    700   1000   1300   1600)
a=(2.8895590928428625 2.8888136685325874 2.8917819393042783 2.8994749913634545 2.910753033506597 2.9229202382247097)
k=( 7.88671532 9.12609654 8.01620284 6.97561494 5.0726685 4.04736043)

mkdir -p data # Create directory structure for data output.

# Run job.
for n in $(seq 0 5)
do
  printf "Running T = ${T[n]}K simulation.\n"
  ${lammps} -in  in.lmp                   \
            -log data/lammps_${T[n]}K.log \
            -screen none                  \
            -var RANDOM ${RANDOM}         \
            -var T ${T[n]}                \
            -var a ${a[n]}                \
            -var k ${k[n]}
done

wait
