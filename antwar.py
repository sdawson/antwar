# A simulation of ant warfare modelled as a self-organized critical system.
# Author: Sophie Dawson
import numpy, sys

def main():
  if len(sys.argv[1:]) != 4:
    usage()
    sys.exit(1)
  grid = initGrid(int(sys.argv[1]))
  birthProb = float(sys.argv[2])
  majorProb = float(sys.argv[3])
  noOfSteps = int(sys.argv[4])

  printGrid(grid)
  sys.exit(0)

  for i in range(noOfSteps):
    updateGrid(grid, birthProb, majorProb)
    printGrid(grid)

def initGrid(n):
  return numpy.zeros((n, n), dtype=numpy.int)

def updateGrid(grid, birthProb, majorProb):
  pass

def printGrid(grid):
  (r, c) = grid.shape
  for i in range(r):
    for j in range(c):
      print "%s " % cellPrinting(grid[i][j]), # comma suppresses newline
    print


def usage():
  print "python antwar.py gridsize birthprob majorprob noofsteps"

def getCellType(x):
  return {
    0: "EMPTY",
    1: "REDMINOR",
    2: "REDMAJOR",
    3: "BLUEMINOR",
    4: "BLUEMAJOR",
  }[x]

def cellPrinting(x):
  return {
    0: "EM",
    1: "Rm",
    2: "RM",
    3: "Bm",
    4: "BM"
  }[x]


if __name__ == "__main__":
  main()
