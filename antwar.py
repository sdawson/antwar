from __future__ import division
# A simulation of ant warfare modelled as a self-organized critical system.
# Author: Sophie Dawson
import numpy, sys, random, os, time
import colorama, datetime

# Cell constants
EMPTY = 0
REDMINOR = 1
REDMAJOR = 2
BLUEMINOR = 3
BLUEMAJOR = 4

def main():
  if len(sys.argv[1:]) != 6:
    usage()
    sys.exit(1)
  gridSize = int(sys.argv[1])
  grid = initGrid(gridSize)
  birthProb = float(sys.argv[2])
  redMajorProb = float(sys.argv[3])
  blueMajorProb = float(sys.argv[4])
  noOfSteps = int(sys.argv[5])
  isPrintGrid = sys.argv[6]

  fullStats = {"minblue": [0]*gridSize**2, "minred": [0]*gridSize**2,
      "majblue": [0]*gridSize**2, "majred": [0]*gridSize**2}
  
  currentDate = datetime.datetime.now().strftime("%Y%m%d%H%M")
  filenamePrefix = "antsim-p%.2f-rf%.2f-bf%.2f-steps%d-size%d-" % (birthProb,
      redMajorProb, blueMajorProb, noOfSteps, int(sys.argv[1]))
  filename = ''.join([filenamePrefix, currentDate, ".out"])
  print filename
  f = open(filename, 'w')

  f.write("NoOfDeaths\tMinBlueDeath\tMajBlueDeath\tMinRedDeath\tMajReadDeath\n")
  colorama.init() # Initialize colorama
  for i in range(noOfSteps):
    grid = updateGrid(grid, birthProb, redMajorProb, blueMajorProb, fullStats, "diag")
    if isPrintGrid == "print":
      time.sleep(.1)
      os.system('cls' if os.name == 'nt' else 'clear')
      printGrid(grid)
  for stati in range(len(fullStats["minblue"])):
    if fullStats["minblue"][stati] != 0 or fullStats["majblue"][stati] != 0 \
    or fullStats["minred"][stati] != 0 or fullStats["majred"][stati] !=0:
      f.write("%d\t%d\t%d\t%d\t%d\n" % (stati, fullStats["minblue"][stati],
        fullStats["majblue"][stati], fullStats["minred"][stati], fullStats["majred"][stati]))
  f.close()
  colorama.deinit()

def initGrid(n):
  return numpy.zeros((n, n), dtype=numpy.int)

# Grid is updated destructively, so a new copy
# of the grid is returned
def updateGrid(grid, birthProb,
    redMajorProb, blueMajorProb, fullStats, check="nodiag"):
  newGrid = grid.copy()
  (r, c) = grid.shape
  stepStats = {"minblue": 0, "minred": 0, "majblue": 0, "majred": 0}
  for i in range(r):
    for j in range(c):
      if grid[i][j] == EMPTY:
        newGrid[i][j] = maybePopulateCell(birthProb, redMajorProb, blueMajorProb)
      else:
        newGrid[i][j] = updateCell(grid, i, j, stepStats, birthProb,
            redMajorProb, blueMajorProb, check)
  updatePdfStats(fullStats, stepStats)
  return newGrid

# Updates the total set of stats for the PDF based
# on the number of deaths per ant type for a single step
def updatePdfStats(stats, stepStats):
  for antType in stepStats:
    stats[antType][stepStats[antType]] = stats[antType][stepStats[antType]] + 1

def updateCell(grid, r, c, stats, birthProb,
    redMajorProb, blueMajorProb, check):
  if grid[r][c] == REDMINOR:
    isDeath = isDeathCondition(grid, r, c, check, 1, 1)
    if isDeath:
      stats["minred"] = stats["minred"] + 1
      return fillAntDeathCell(grid, r, c, isDeath, birthProb,
          redMajorProb, blueMajorProb)
    else:
      return grid[r][c]
  elif grid[r][c] == BLUEMINOR:
    isDeath = isDeathCondition(grid, r, c, check, 1, 1)
    if isDeath:
      stats["minblue"] = stats["minblue"] + 1
      return fillAntDeathCell(grid, r, c, isDeath, birthProb,
          redMajorProb, blueMajorProb)
    else:
      return grid[r][c]
  elif grid[r][c] == REDMAJOR:
    isDeath = isDeathCondition(grid, r, c, check, 4, 1)
    if isDeath:
      stats["majred"] = stats["majred"] + 1
      return fillAntDeathCell(grid, r, c, isDeath, birthProb,
          redMajorProb, blueMajorProb)
    else:
      return grid[r][c]
  elif grid[r][c] == BLUEMAJOR:
    isDeath = isDeathCondition(grid, r, c, check, 4, 1)
    if isDeath:
      stats["majblue"] = stats["majblue"] + 1
      return fillAntDeathCell(grid, r, c, isDeath, birthProb,
          redMajorProb, blueMajorProb)
    else:
      return grid[r][c]
  else:
    print "Error: invalid cell value %d" % grid[r][c]
    sys.exit(1)

# If a the ants in a cell have died, determines whether
# the cell should be filled with minors, majors or made empty.
# Cell will be filled with majors with probability pf, and
# minors with probability p(1-f)
def fillAntDeathCell(grid, r, c, winAntType, birthProb,
    redMajorProb, blueMajorProb):
  if winAntType == "minor" and getCellColour(grid[r][c]) == "RED":
    # Fill the cell with an ant of the opposite colour
    return maybeFillWinnerCell(birthProb, blueMajorProb, BLUEMINOR)
  elif winAntType == "minor" and getCellColour(grid[r][c]) == "BLUE":
    return maybeFillWinnerCell(birthProb, redMajorProb, REDMINOR)
  elif winAntType == "major" and getCellColour(grid[r][c]) == "RED":
    return maybeFillWinnerCell(birthProb, blueMajorProb, BLUEMAJOR)
  else:
    return maybeFillWinnerCell(birthProb, redMajorProb, REDMAJOR)

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
def maybePopulateCell(birthProb, redMajorProb, blueMajorProb):
  birthRand = random.random()
  if birthRand < birthProb:
    # Ant is born/cell is populated
    majorRand = random.random()
    if random.random() < 0.5:
      # Blue ant
      if majorRand < blueMajorProb:
        return BLUEMAJOR
      else:
        return BLUEMINOR
    else:
      # Red ant
      if majorRand < redMajorProb:
        return REDMAJOR
      else:
        return REDMINOR
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
        print colorama.Back.MAGENTA + " ",
      elif grid[i][j] == REDMAJOR:
        print colorama.Back.RED + " ",
      elif grid[i][j] == BLUEMINOR:
        print colorama.Back.CYAN + " ",
      elif grid[i][j] == BLUEMAJOR:
        print colorama.Back.BLUE + " ",
    print colorama.Back.RESET

def usage():
  print "python antwar.py gridsize birthprob redmajorprob bluemajorprob noofsteps [print|noprint]"

def getCellColour(x):
  return {
    0: "EMPTY",
    1: "RED",
    2: "RED",
    3: "BLUE",
    4: "BLUE"
  }[x]

if __name__ == "__main__":
  main()
