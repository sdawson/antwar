from __future__ import division
# A simulation of ant warfare modelled as a self-organized critical system.
# Author: Sophie Dawson
import numpy, sys, random, os, time
import colorama, datetime

# Cell constants
EMPTY = 0
REDOLD = 1
REDYOUNG = 2
BLUEOLD = 3
BLUEYOUNG = 4

def main():
  if len(sys.argv[1:]) != 6:
    usage()
    sys.exit(1)
  gridSize = int(sys.argv[1])
  grid = initGrid(gridSize)
  birthProb = float(sys.argv[2])
  redYoungProb = float(sys.argv[3])
  blueYoungProb = float(sys.argv[4])
  noOfSteps = int(sys.argv[5])
  isPrintGrid = sys.argv[6]

  fullStats = {"oldblue": [0]*gridSize**2, "oldred": [0]*gridSize**2,
      "youngblue": [0]*gridSize**2, "youngred": [0]*gridSize**2}
  
  currentDate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  filenamePrefix = "antsim-p%.3f-rf%.3f-bf%.3f-steps%d-size%d-" % (birthProb,
      redYoungProb, blueYoungProb, noOfSteps, int(sys.argv[1]))
  filename = ''.join([filenamePrefix, currentDate, ".out"])
  #print filename
  #f = open(filename, 'w')

  #f.write("NoOfDeaths\toldblueDeath\tyoungblueDeath\toldredDeath\tMajReadDeath\n")
  colorama.init() # Initialize colorama
  for i in range(noOfSteps):
    grid = updateGrid(grid, birthProb, redYoungProb, blueYoungProb, fullStats, "diag")
    if i % 10 == 0 and isPrintGrid == "print":
      time.sleep(.2)
      os.system('cls' if os.name == 'nt' else 'clear')
      printGrid(grid)
      print i
    if allOneTribe(grid):
      print "%s\t%d" % (getCellColour(grid[0][0]), i)
      break
  #for stati in range(len(fullStats["oldblue"])):
  #  if fullStats["oldblue"][stati] != 0 or fullStats["youngblue"][stati] != 0 \
  #  or fullStats["oldred"][stati] != 0 or fullStats["youngred"][stati] !=0:
  #    f.write("%d\t%d\t%d\t%d\t%d\n" % (stati, fullStats["oldblue"][stati],
  #      fullStats["youngblue"][stati], fullStats["oldred"][stati], fullStats["youngred"][stati]))
  #f.close()
  colorama.deinit()

def initGrid(n):
  return numpy.zeros((n, n), dtype=numpy.int)

# Grid is updated destructively, so a new copy
# of the grid is returned
def updateGrid(grid, birthProb,
    redYoungProb, blueYoungProb, fullStats, check="nodiag"):
  newGrid = grid.copy()
  (r, c) = grid.shape
  stepStats = {"oldblue": 0, "oldred": 0, "youngblue": 0, "youngred": 0}
  for i in range(r):
    for j in range(c):
      if grid[i][j] == EMPTY:
        newGrid[i][j] = maybePopulateCell(birthProb, redYoungProb, blueYoungProb)
      else:
        (currentPos, fleeCell) = updateCell(grid, i, j, stepStats, birthProb,
            redYoungProb, blueYoungProb, check)
        # TODO: if currentpos = empty and there's a fleecell, update both current (i,j),
        # and the fleecell (put the current i,j value in the fleecell location 1st
        newGrid[i][j] = updateCell(grid, i, j, stepStats, birthProb,
            redYoungProb, blueYoungProb, check)
  updatePdfStats(fullStats, stepStats)
  return newGrid

def allOneTribe(grid):
  (r, c) = grid.shape
  initColour = getCellColour(grid[0][0])
  for i in range(r):
    for j in range(c):
      if getCellColour(grid[i][j]) != initColour:
        return False
  return True

# Updates the total set of stats for the PDF based
# on the number of deaths per ant type for a single step
def updatePdfStats(stats, stepStats):
  for antType in stepStats:
    stats[antType][stepStats[antType]] = stats[antType][stepStats[antType]] + 1

def updateCell(grid, r, c, stats, birthProb,
    redYoungProb, blueYoungProb, check):
  if grid[r][c] == REDOLD:
    isDeath = isDeathCondition(grid, r, c, check, 2, 1)
    if isDeath:
      stats["oldred"] = stats["oldred"] + 1
      return (fillAntDeathCell(grid, r, c, isDeath, birthProb,
          redYoungProb, blueYoungProb), ())
    else:
      return (grid[r][c], ())
  elif grid[r][c] == BLUEOLD:
    isDeath = isDeathCondition(grid, r, c, check, 2, 1)
    if isDeath:
      stats["oldblue"] = stats["oldblue"] + 1
      return (fillAntDeathCell(grid, r, c, isDeath, birthProb,
          redYoungProb, blueYoungProb), ())
    else:
      return (grid[r][c], ())
  elif grid[r][c] == REDYOUNG:
    fleeCell = toFleeLocation(grid, r, c, check)
    if fleeCell:
      return (EMPTY, fleeCell)
    else:
      isDeath = isDeathCondition(grid, r, c, check, 4, 1)
      if isDeath:
        stats["youngred"] = stats["youngred"] + 1
        return (fillAntDeathCell(grid, r, c, isDeath, birthProb,
            redYoungProb, blueYoungProb), ())
      else:
        return (grid[r][c], ())
  elif grid[r][c] == BLUEYOUNG:
    fleeCell = toFleeLocation(grid, r, c, check)
    if fleeCell:
      return (EMPTY, fleeCell)
    else:
      isDeath = isDeathCondition(grid, r, c, check, 4, 1)
      if isDeath:
        stats["youngblue"] = stats["youngblue"] + 1
        return (fillAntDeathCell(grid, r, c, isDeath, birthProb,
            redYoungProb, blueYoungProb), ())
      else:
        return (grid[r][c], ())
  else:
    print "Error: invalid cell value %d" % grid[r][c]
    sys.exit(1)

# If a the ants in a cell have died, determines whether
# the cell should be filled with minors, majors or made empty.
# Cell will be filled with majors with probability pf, and
# minors with probability p(1-f)
def fillAntDeathCell(grid, r, c, winAntType, birthProb,
    redYoungProb, blueYoungProb):
  if winAntType == "minor" and getCellColour(grid[r][c]) == "RED":
    # Fill the cell with an ant of the opposite colour
    return maybeFillWinnerCell(birthProb, blueYoungProb, BLUEOLD)
  elif winAntType == "minor" and getCellColour(grid[r][c]) == "BLUE":
    return maybeFillWinnerCell(birthProb, redYoungProb, REDOLD)
  elif winAntType == "major" and getCellColour(grid[r][c]) == "RED":
    return maybeFillWinnerCell(birthProb, blueYoungProb, BLUEYOUNG)
  else:
    return maybeFillWinnerCell(birthProb, redYoungProb, REDYOUNG)

# And type should be returned, or "" (== False?)
def isDeathCondition(grid, r, c, check, noOfMinors, noOfMajors):
  minorCount = 0
  majorCount = 0
  for (i, j) in genCheckList(grid, r, c, check):
    #print "checking (%s, %s) for (%s, %s)" % (i, j, r, c)
    if getCellColour(grid[r][c]) == "BLUE" and (grid[i][j] == REDYOUNG):
      majorCount = majorCount + 1
    elif getCellColour(grid[r][c]) == "BLUE" and (grid[i][j] == REDOLD):
      minorCount = minorCount + 1
    elif getCellColour(grid[r][c]) == "RED" and (grid[i][j] == BLUEYOUNG):
      majorCount = majorCount + 1
    elif getCellColour(grid[r][c]) == "RED" and (grid[i][j] == BLUEOLD):
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

# Determines if a young ant should flee or not, then
# returns a possible location to flee to, if one exists.
def toFleeLocation(grid, r, c, check):
  friendlyCount = 0
  enemyCount = 0
  freeSpaces = []
  for (i, j) in genCheckList(grid, r, c, check):
    if getCellColour(grid[r][c]) == "BLUE" and getCellColour(grid[i][j]) == "RED":
      enemyCount = enemyCount + 1
    elif getCellColour(grid[r][c]) == "BLUE" and getCellColour(grid[i][j]) == "BLUE":
      friendlyCount = friendlyCount + 1
    elif getCellColour(grid[r][c]) == "RED" and getCellColour(grid[i][j]) == "RED":
      friendlyCount = friendlyCount + 1
    elif getCellColour(grid[r][c]) == "RED" and getCellColour(grid[i][j]) == "BLUE":
      enemyCount = enemyCount + 1
    else:
      freeSpaces.append((i, j))
  if (friendlyCount > enemyCount):
    return []
  elif freeSpaces:
    # Flee to the first free space, if there is one
    return freeSpaces[0]
  else:
    return []

# Populates a cell according to a given birth probability
# and major ant probability.  The optional type argument
# is used to populate a cell when the ant type (red/blue)
# is known in advance.  This only occurs after an ant death.
def maybePopulateCell(birthProb, redYoungProb, blueYoungProb):
  birthRand = random.random()
  if birthRand < birthProb:
    # Ant is born/cell is populated
    majorRand = random.random()
    if random.random() < 0.5:
      # Blue ant
      if majorRand < blueYoungProb:
        return BLUEYOUNG
      else:
        return BLUEOLD
    else:
      # Red ant
      if majorRand < redYoungProb:
        return REDYOUNG
      else:
        return REDOLD
  else:
    return EMPTY

# Altered to disallow old ants from repopulating a cell,
# since they are infertile.  i.e. Repopulation assumes
# fertility
def maybeFillWinnerCell(birthProb, majorProb, type):
  birthRand = random.random()
  if birthRand < birthProb:
    majorRand = random.random()
    if type == BLUEYOUNG and majorRand < majorProb:
      return BLUEYOUNG
    #elif type == BLUEOLD and majorRand >= majorProb:
    #  return BLUEOLD
    elif type == REDYOUNG and majorRand < majorProb:
      return REDYOUNG
    #elif type == REDOLD and majorRand >= majorProb:
    #  return REDOLD
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
      elif grid[i][j] == REDOLD:
        print colorama.Back.MAGENTA + " ",
      elif grid[i][j] == REDYOUNG:
        print colorama.Back.RED + " ",
      elif grid[i][j] == BLUEOLD:
        print colorama.Back.CYAN + " ",
      elif grid[i][j] == BLUEYOUNG:
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

def getCellAge(x):
  return {
    0: "EMPTY",
    1: "OLD",
    2: "YOUNG",
    3: "OLD",
    4: "YOUNG"
  }[x]

if __name__ == "__main__":
  main()
