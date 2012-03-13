# A simulation of ant warfare modelled as a self-organized critical system.
# Author: Sophie Dawson
import numpy, sys, random

# Cell constants
EMPTY = 0
REDMINOR = 1
REDMAJOR = 2
BLUEMINOR = 3
BLUEMAJOR = 4

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
    grid = updateGrid(grid, birthProb, majorProb)
    printGrid(grid)

def initGrid(n):
  return numpy.zeros((n, n), dtype=numpy.int)

# Grid is updated destructively, so a new copy
# of the grid is returned
def updateGrid(grid, birthProb, majorProb):
  newGrid = grid.copy()
  (r, c) = grid.shape
  for i in range(r):
    for j in range(c):
      if grid[i][j] == EMPTY:
        newGrid[i][j] = maybePopulateCell(birthProb, majorProb)
      elif grid[i][j] == REDMINOR or grid[i][j] == BLUEMINOR:
        newGrid[i][j] = updateMinorCell(grid, i, j)
      else:
        newGrid[i][j] = updateMajorCell(grid, i, j)

def updateMinorCell(grid, r, c):
  pass

def updateMajorCell(grid, r, c):
  pass

def maybePopulateCell(birthProb, majorProb):
  birthRand = random.random()
  if birthRand < birthProb:
    # Ant is born/cell is populated
    majorRand = random.random()
    if majorRand < majorProb:
      # Determine side r/b
      # is a major
      if random.random() < 0.5:
        return BLUEMAJOR
      else:
        return REDMAJOR
    else:
      if random.random() < 0.5:
        return BLUEMINOR
      else:
        return REDMINOR
      # is a minor
  else:
    return EMPTY

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
