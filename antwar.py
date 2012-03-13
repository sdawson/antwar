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
  print genCheckList(grid, 0, 5, "nondiag")
  print genCheckList(grid, 0, 5, "diag")
  sys.exit(0)

  for i in range(noOfSteps):
    grid = updateGrid(grid, birthProb, majorProb)
    printGrid(grid)

def initGrid(n):
  return numpy.zeros((n, n), dtype=numpy.int)

# Grid is updated destructively, so a new copy
# of the grid is returned
def updateGrid(grid, birthProb, majorProb, check="nodiag"):
  newGrid = grid.copy()
  (r, c) = grid.shape
  for i in range(r):
    for j in range(c):
      if grid[i][j] == EMPTY:
        newGrid[i][j] = maybePopulateCell(birthProb, majorProb)
      else:
        newGrid[i][j] = updateCell(grid, i, j, check)

def updateCell(grid, r, c, check):
  if grid[r][c] == REDMINOR or grid[r][c] == BLUEMINOR:
    if isDeathCondition(grid, r, c, check, 1, 1):
      return EMPTY
    else:
      return grid[r][c]
  elif grid[r][c] == REDMAJOR or grid[r][c] == BLUEMAJOR:
    if isDeathCondition(grid, r, c, check, 4, 1):
      return EMPTY
    else:
      return grid[r][c]
  else:
    print "Error: invalid cell value %d" % grid[r][c]
    sys.exit(1)

def isDeathCondition(grid, r, c, check, noOfMinors, noOfMajors):
  minorCount = 0
  majorCount = 0
  for (i, j) in genCheckList(grid, r, c, check):
    if (grid[r][c] == BLUEMAJOR
        or grid[r][c] == BLUEMINOR) and (grid[i][j] == REDMAJOR):
      majorCount = majorCount + 1
    elif (grid[r][c] == BLUEMAJOR
          or grid[r][c] == BLUEMINOR) and (grid[i][j] == REDMINOR):
      minorCount = minorCount + 1
    elif (grid[r][c] == REDMAJOR
          or grid[r][c] == REDMINOR) and (grid[i][j] == BLUEMAJOR):
      majorCount = majorCount + 1
    elif (grid[r][c] == REDMAJOR
          or grid[r][c] == REDMINOR) and (grid[i][j] == BLUEMINOR):
      minorCount = minorCount + 1
  return minorCount >= noOfMinors or majorCount >= noOfMajors

# generates a list of cells to check, based on
# whether diagonal cells should be checked or not.
def genCheckList(grid, r, c, check):
  (maxr, maxc) = grid.shape
  cells = []
  if r == 0:
    cells.append((r+1, c))
    addColCells(grid, cells, r, c, r+1, check)
  elif r == maxr - 1:
    cells.append((r-1, c))
    addColCells(grid, cells, r, c, r-1, check)
  else:
    if check == "diag":
      cells.extend([(r, c-1), (r, c+1), (r-1, c), (r+1, c),
        (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)])
    else:
      cells.extend([(r, c-1), (r, c+1), (r-1, c), (r+1, c)])
  return cells

def addColCells(grid, cells, r, c, offsetRow, check):
  (maxr, maxc) = grid.shape
  if c == 0:
    cells.append((r, c+1))
    if check == "diag":
      cells.append((offsetRow, c+1))
  elif c == maxc - 1:
    cells.append((r, c-1))
    if check == "diag":
      cells.append((offsetRow, c-1))
  else:
    cells.extend([(r, c-1), (r, c+1)])
    if check == "diag":
      cells.extend([(offsetRow, c-1), (offsetRow, c+1)])

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
