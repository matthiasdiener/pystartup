#!/usr/bin/env python3


from datetime import datetime
import sys

import sys
# sys.path.insert(0, 'grudge-2015.1-py3-none-any.whl')
# sys.path.insert(0, 'dagrt-2019.4-py3-none-any.whl')
# sys.path.insert(0, 'leap-2019.5-py3-none-any.whl')
# sys.path.insert(0, 'loo.py-2019.1-py3-none-any.whl')
# sys.path.insert(0, 'meshmode-2016.1-py3-none-any.whl')


import dagrt
import grudge
import loopy
import meshmode
import leap


from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    print(dagrt.__file__, file=sys.stderr)
    print(grudge.__file__, file=sys.stderr)
    print(loopy.__file__, file=sys.stderr)
    print(meshmode.__file__, file=sys.stderr)
    print(leap.__file__, file=sys.stderr)

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S.%f")
    print(current_time)
    print('Rank ', rank, '/', comm.size)
    print(sys.version)
