import multiprocessing as mp
import itertools

import numpy

ON = 1
OFF = -1
EMPTY = 0

def main(n):
  grid = numpy.zeros((n, n), dtype=numpy.int)

  print mp.cpu_count()

  inds = numpy.rollaxis(numpy.indices(grid.shape), 0, 3).reshape(-1, 2)

  print "mapping to cpus"
  pool = mp.Pool()
  results = pool.map(mult, itertools.repeat(3, 16))
  print results


def mult(x):
  return x*x

if __name__ == "__main__":
  main(5)
