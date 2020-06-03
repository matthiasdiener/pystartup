### LSF syntax
#BSUB -nnodes 384                 #number of nodes
#BSUB -W 30                       #walltime in minutes
#BSUB -J pystartup                #name of job
#BSUB -q pbatch                   #queue to use

nnodes=$(echo $LSB_MCPU_HOSTS | wc -w)
nnodes=$((nnodes/2-1))

echo $nnodes

# Warmup
lrun -n 1 python3 startup.py

for i in 1 2 4 8 16 32; do
    for j in $(seq 1 10); do
        nproc=$((i*nnodes))
        echo $nproc

        start=$(date +"%T.%N")

        lrun -n $nproc python3 startup.py | tee out.txt

        end=$(date +"%T.%N")

        mid=$(head -1 out.txt)

        startup_time=$(ddiff -f '%H:%M:%S.%N' -i '%H:%M:%S.%N' $start $mid)
        total_time=$(ddiff -f '%H:%M:%S.%N' -i '%H:%M:%S.%N' $start $end)

        echo $startup_time $total_time >> $nnodes-$i.txt
    done
done

echo 'Done'
