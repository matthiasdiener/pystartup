#!/bin/bash
#SBATCH -N 2                  
#SBATCH -t 00:30:00                
#SBATCH -J pystartup               
#SBATCH -p pbatch                  

nnodes=$SLURM_JOB_NUM_NODES

echo $nnodes

# Warmup
srun -n 1 python3 startup.py

for i in 1 2 4 8 16 32; do
    for j in $(seq 1 10); do
        nproc=$((i*nnodes))
        echo $nproc

        start=$(date +"%T.%N")

        srun -n $nproc python3 startup.py | tee out.txt

        end=$(date +"%T.%N")

        mid=$(head -1 out.txt)

        startup_time=$(ddiff -f '%H:%M:%S.%N' -i '%H:%M:%S.%N' $start $mid)
        total_time=$(ddiff -f '%H:%M:%S.%N' -i '%H:%M:%S.%N' $start $end)

        echo $startup_time $total_time >> $nnodes-$i.txt
    done
done

echo 'Done'
