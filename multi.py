import multiprocessing as mp
import itertools, os
from functools import partial

import numpy

ON = 1
OFF = -1
EMPTY = 0

def main(n):
  grid = numpy.zeros((n, n), dtype=numpy.int)

  print mp.cpu_count()
  print "orig grid"
  print grid

  inds = numpy.rollaxis(numpy.indices(grid.shape), 0, 3).reshape(-1, 2)
  print inds

  partial_change_cell = partial(change_cell, grid)
  print "mapping to cpus"
  pool = mp.Pool()
  results = pool.map(partial_change_cell, inds)
  print results


def mult(x):
  return x*x

def change_cell_unpack(matrix, r_c):
  change_cell(matrix, *r_c)

def change_cell(matrix, *r_c):
  print "in change cell, process: %d" % os.getpid()
  if matrix[r][c] == EMPTY:
    return [ON, r, c]
  elif matrix[r][c] == OFF:
    return [ON, r, c]
  elif matrix[r][c] == ON:
    return [OFF, r, c]

if __name__ == "__main__":
  main(5)
