#!/bin/bash
#SBATCH -t 00:30:00
#SBATCH -J pystartup
#SBATCH -p pbatch

nnodes=$SLURM_JOB_NUM_NODES

echo $nnodes

export PYOPENCL_NO_CACHE=1
export LOOPY_NO_CACHE=1
export XDG_CACHE_HOME=/p/lscratchh/diener3/xdg-scratch

# Warmup
srun -n 1 python3 loopystartup.py

for i in 1 ; do
    for j in $(seq 1 2); do
        nproc=$((i*nnodes))
        echo $nproc

        start=$(date +"%T.%N")

        srun -n $nproc python3 loopystartup.py | tee out$nnodes.txt

        end=$(date +"%T.%N")

        mid=$(head -1 out$nnodes.txt)

        startup_time=$(ddiff -f '%S.%N' -i '%H:%M:%S.%N' $start $mid)
        total_time=$(ddiff -f '%S.%N' -i '%H:%M:%S.%N' $start $end)

        echo $startup_time $total_time >> $nnodes-$i.txt
    done
done

echo 'Done'
