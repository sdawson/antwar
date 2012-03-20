from __future__ import division
# A simulation of ant warfare modelled as a self-organized critical system.
# Author: Sophie Dawson
import numpy, sys, random, os, time
import colorama

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

  stats = [0, 0] # (no. of major deaths, no. of minor deaths)

  colorama.init() # Initialize colorama
  for i in range(noOfSteps):
    grid = updateGrid(grid, birthProb, majorProb, stats, "diag")
    printGrid(grid)
  # Major Deaths\t Minor Deaths\t S+\t S-
  print "%d\t%d\t%f\t%f" % (stats[0], stats[1], stats[0]/noOfSteps, stats[1]/noOfSteps)
  colorama.deinit()

def probTest():
  if len(sys.argv[1:]) != 4:
    usage()
    sys.exit(1)
  grid = initGrid(int(sys.argv[1]))
  birthProb = float(sys.argv[2])
  majorProb = float(sys.argv[3])
  noOfSteps = int(sys.argv[4])
  
  major = 0
  minor = 0
  empty = 0
  for i in range(noOfSteps):
    res = maybePopulateCell(birthProb, majorProb)
    if res == BLUEMAJOR or res == REDMAJOR:
      major = major + 1
    elif res == BLUEMINOR or res == REDMINOR:
      minor = minor + 1
    else:
      empty = empty + 1
  print "empty: %d" % empty
  print "# of steps: %d" % noOfSteps
  print "major/no of steps: %f" % (major / noOfSteps)
  print "minor/no of steps: %f" % (minor / noOfSteps)
  print "empty + M + m: %d" % (empty + major + minor)

def cornerCaseTest():
  grid = initGrid(5)
  grid[4][0] = REDMINOR
  grid[3][0] = BLUEMAJOR
  grid[3][1] = BLUEMAJOR
  print "init grid"
  printGrid(grid)
  print isDeathCondition(grid, 4, 0, "diag", 1, 1)
  print updateCell(grid, 4, 0, [0, 0], 0.5, 0.25, "diag")

def initGrid(n):
  return numpy.zeros((n, n), dtype=numpy.int)

# Grid is updated destructively, so a new copy
# of the grid is returned
def updateGrid(grid, birthProb, majorProb, stats, check="nodiag"):
  newGrid = grid.copy()
  (r, c) = grid.shape
  for i in range(r):
    for j in range(c):
      if grid[i][j] == EMPTY:
        newGrid[i][j] = maybePopulateCell(birthProb, majorProb)
      else:
        newGrid[i][j] = updateCell(grid, i, j, stats, birthProb, majorProb, check)
  return newGrid

def updateCell(grid, r, c, stats, birthProb, majorProb, check):
  if grid[r][c] == REDMINOR or grid[r][c] == BLUEMINOR:
    isDeath = isDeathCondition(grid, r, c, check, 1, 1)
    if isDeath:
      stats[1] = stats[1] + 1 # +1 to no. of minor ant deaths
      return fillAntDeathCell(grid, r, c, isDeath, birthProb, majorProb)
    else:
      return grid[r][c]
  elif grid[r][c] == REDMAJOR or grid[r][c] == BLUEMAJOR:
    isDeath = isDeathCondition(grid, r, c, check, 4, 1)
    if isDeath:
      stats[0] = stats[0] + 1 # +1 to no. of major ant deaths
      return fillAntDeathCell(grid, r, c, isDeath, birthProb, majorProb)
    else:
      return grid[r][c]
  else:
    print "Error: invalid cell value %d" % grid[r][c]
    sys.exit(1)

# If a the ants in a cell have died, determines whether
# the cell should be filled with minors, majors or made empty.
# Cell will be filled with majors with probability pf, and
# minors with probability p(1-f)
def fillAntDeathCell(grid, r, c, winAntType, birthProb, majorProb):
  if winAntType == "minor" and getCellColour(grid[r][c]) == "RED":
    # Fill the cell with an ant of the opposite colour
    return maybeFillWinnerCell(birthProb, majorProb, BLUEMINOR)
  elif winAntType == "minor" and getCellColour(grid[r][c]) == "BLUE":
    return maybeFillWinnerCell(birthProb, majorProb, REDMINOR)
  elif winAntType == "major" and getCellColour(grid[r][c]) == "RED":
    return maybeFillWinnerCell(birthProb, majorProb, BLUEMAJOR)
  else:
    return maybeFillWinnerCell(birthProb, majorProb, REDMAJOR)

# And type should be returned, or "" (== False?)
def isDeathCondition(grid, r, c, check, noOfMinors, noOfMajors):
  minorCount = 0
  majorCount = 0
  for (i, j) in genCheckList(grid, r, c, check):
    # TODO: UPDATE for use of the getCellColour function
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
  if minorCount >= noOfMinors:
    return "minor"
  elif majorCount >= noOfMajors:
    return "major"
  else:
    return ""

# generates a list of cells to check, based on
# whether diagonal cells should be checked or not.
# Treats the grid as a torus
def genCheckList(grid, r, c, check):
  (maxr, maxc) = grid.shape
  cells = [((r-1) % maxr, c), ((r+1) % maxr, c), (r, (c-1) % maxc), (r, (c+1) % maxc)]

  if check == "diag":
    # Add diagonal cells
    cells.extend([((r-1) % maxr, (c-1) % maxc),
      ((r-1) % maxr, (c+1) % maxc), ((r+1) % maxr, (c-1) % maxc), ((r+1) % maxr, (c+1) % maxc)])
  return cells

# Populates a cell according to a given birth probability
# and major ant probability.  The optional type argument
# is used to populate a cell when the ant type (red/blue)
# is known in advance.  This only occurs after an ant death.
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

def maybeFillWinnerCell(birthProb, majorProb, type):
  birthRand = random.random()
  if birthRand < birthProb:
    majorRand = random.random()
    if type == BLUEMAJOR and majorRand < majorProb:
      return BLUEMAJOR
    elif type == BLUEMINOR and majorRand >= majorProb:
      return BLUEMINOR
    elif type == REDMAJOR and majorRand < majorProb:
      return REDMAJOR
    elif type == REDMINOR and majorRand >= majorProb:
      return REDMINOR
    else:
      return EMPTY
  else:
    return EMPTY

def printGrid(grid):
  (r, c) = grid.shape
  for i in range(r):
    for j in range(c):
      if grid[i][j] == EMPTY:
        print colorama.Back.BLACK + " ", # comma suppresses newline
      elif grid[i][j] == REDMINOR:
        print colorama.Back.RED + " ",
      elif grid[i][j] == REDMAJOR:
        print colorama.Back.RED + " ",
      elif grid[i][j] == BLUEMINOR:
        print colorama.Back.CYAN + " ",
      elif grid[i][j] == BLUEMAJOR:
        print colorama.Back.BLUE + " ",
    print colorama.Back.RESET
  time.sleep(.1)
  #os.system('cls' if os.name == 'nt' else 'clear')
  print

# Returns the colour of a grid cell as a string
#def getCellColour(grid, r, c):
#  if grid[r][c] == EMPTY:
#    return "EMPTY"
#  elif grid[r][c] == BLUEMINOR or grid[r][c] == BLUEMAJOR:
#    return "BLUE"
#  else:
#    return "RED"

def usage():
  print "python antwar.py gridsize birthprob majorprob noofsteps"

def getCellType(x):
  return {
    0: "EMPTY",
    1: "REDMINOR",
    2: "REDMAJOR",
    3: "BLUEMINOR",
    4: "BLUEMAJOR"
  }[x]

def getCellColour(x):
  return {
    0: "EMPTY",
    1: "RED",
    2: "RED",
    3: "BLUE",
    4: "BLUE"
  }[x]

def cellPrinting(x):
  return {
    0: "EY",
    1: "Rm",
    2: "RM",
    3: "Bm",
    4: "BM"
  }[x]


if __name__ == "__main__":
  main()
  #cornerCaseTest()
