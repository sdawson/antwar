import multiprocessing as mp
import itertools, os
from functools import partial

import numpy

ON = 1
OFF = -1
EMPTY = 0

def main(n):
  grid = numpy.zeros((n, n), dtype=numpy.int)

  #print mp.cpu_count()
  #print "orig grid"
  #print grid

  inds = numpy.rollaxis(numpy.indices(grid.shape), 0, 3).reshape(-1, 2)
  for [r, c] in inds:
    print type(r), type(c)

  partial_change_cell = partial(change_cell, grid)
  #print "mapping to cpus"
  pool = mp.Pool()
  results = pool.map(partial_change_cell, inds)
  grid = combine_res(results, n)
  #print grid
  #print results

def combine_res(results, n):
  new_grid = numpy.zeros((n, n), dtype=numpy.int)
  for [v, r, c] in results:
    print type(c), type(r), type(v)
    new_grid[r][c] = v
  return new_grid


def mult(x):
  return x*x

def change_cell(matrix, r_c):
  #print "in change cell, process: %d" % os.getpid()
  [r, c] = r_c
  if matrix[r][c] == EMPTY:
    return [ON, r, c]
  elif matrix[r][c] == OFF:
    return [ON, r, c]
  elif matrix[r][c] == ON:
    return [OFF, r, c]

if __name__ == "__main__":
  for i in range(1):
    main(20)
