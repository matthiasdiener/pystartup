#!/usr/bin/env python3


from datetime import datetime
import sys
import grudge
import pyopencl


from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S.%f")
    print(current_time)
    print('Rank ', rank, '/', comm.size)
    print(sys.version)
