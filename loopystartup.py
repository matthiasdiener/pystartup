#!/usr/bin/env python3


import numpy as np
import pyopencl as cl
import pyopencl.array
import pyopencl.clrandom

import loopy as lp
# lp.set_caching_enabled(False)
from loopy.version import LOOPY_USE_LANGUAGE_VERSION_2018_2

ctx = cl.create_some_context(interactive=False)
queue = cl.CommandQueue(ctx)

from datetime import datetime
import sys
import grudge
import pyopencl


from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


n = 2*2

a_mat = cl.clrandom.rand(queue, (n, n), dtype=np.float32)
b_mat = cl.clrandom.rand(queue, (n, n), dtype=np.float32)
c_mat = cl.clrandom.rand(queue, (n, n), dtype=np.float32)

# a_mat = cl.array.Array(queue,shape=(4,4),data=[[0,-1,1,1],[1,0,1,1],[1,0,1,1],[1,0,1,1]], dtype=np.float32)

# print(type(a_mat))
# print(type(b_mat))
# print(a_mat)
# print(b_mat)
# a_mat = cl.array.Array(queue,[[1,0,1,1],[1,0,1,1],[1,0,1,1],[1,0,1,1]])

# a_mat = array([[0,-1,1,1],[1,0,1,1],[1,0,1,1],[1,0,1,1]], dtype=float32)

# [[1,0,1,1],[1,0,1,1],[1,0,1,1],[1,0,1,1]]

knl = lp.make_kernel(
                "{[i,j,k]: 0<=i,j,k<%d}" % n,
                [
                    "c[i, j] = sum(k, a[i, k]*b[k, j])"
                    ],
                [
                    lp.GlobalArg("a", np.float32, shape=(n, n), order='C'),
                    lp.GlobalArg("b", np.float32, shape=(n, n), order='C'),
                    lp.GlobalArg("c", np.float32, shape=(n, n), order='C'),
                    ],
                name="matmul")

knl(queue, a=a_mat, b = b_mat, c=c_mat)

queue.finish()
# print(a_mat)
# print(b_mat)
# print(c_mat)



if rank == 0:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S.%f")
    print(current_time)
    print('Rank ', rank, '/', comm.size)
    print(sys.version)
    print(lp.__path__)
