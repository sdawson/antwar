import numpy, random, collections
import ant, stats, colorama

EMPTY = 0

class Grid(object):
  # Takes a grid size, a list of the possible tribes for the simulation,
  # the probability of a cell being populated by an ant, and the probability
  # that a major ant is spawned.
  def __init__(self, size, tribes, birthProb, majorProb, checkDiag):
    colorama.init()
    self.grid = numpy.zeros((size, size), dtype=object)
    self.birthProb = birthProb
    self.tribes = tribes
    self.majorProb = majorProb
    self.antStats = stats.AntStats(tribes, size)
    self.checkDiag = checkDiag

  def updateGrid(self):
    newGrid = self.grid.copy()
    (r, c) = self.grid.shape
    majorDeaths = [0]*len(self.tribes)
    minorDeaths = [0]*len(self.tribes)
    for i in range(r):
      for j in range(c):
        if self.grid[i][j] == EMPTY:
          newGrid[i][j] = self.populateCell()
        else:
          newGrid[i][j] = self.updateCell(i, j, majorDeaths, minorDeaths)
    self.antStats.updateStats(majorDeaths, minorDeaths)
    self.grid = newGrid


  # Attempts to populate a grid cell, and returns either
  # a new ant, or EMPTY
  def populateCell(self):
    birthRand = random.random()
    if birthRand < self.birthProb:
      # Cell is populated
      tribeId = random.randint(0, len(self.tribes)-1)
      majorRand = random.random()
      if majorRand < self.majorProb:
        # Create a major ant
        return ant.Ant(self.tribes[tribeId], "major")
      else:
        # Create a minor ant
        return ant.Ant(self.tribes[tribeId], "minor")
    else:
      return EMPTY

  def updateCell(self, r, c, majorDeaths, minorDeaths):
    if self.grid[r][c].antType == "minor":
      (isDeath, enemTribe) = self.isDeathCondition(r, c, 2, 1)
      if isDeath:
        tribeId = self.tribes.index(self.grid[r][c].tribe)
        minorDeaths[tribeId] = minorDeaths[tribeId] + 1
        return self.fillAntDeathCell(r, c, isDeath, enemTribe)
      else:
        return self.grid[r][c]
    elif self.grid[r][c].antType == "major":
      (isDeath, enemTribe) = self.isDeathCondition(r, c, 4, 1)
      if isDeath:
        tribeId = self.tribes.index(self.grid[r][c].tribe)
        majorDeaths[tribeId] = majorDeaths[tribeId] + 1
        return self.fillAntDeathCell(r, c, isDeath, enemTribe)
      else:
        return self.grid[r][c]

  # Attempts to fill the cell of the killed ant with
  # an ant of the specified tribe and type.  The cell will be
  # filled with majors with probability pf (p = birth prob, f = major prob)
  # or minors with probability p(1-f)
  def fillAntDeathCell(self, r, c, antType, tribe):
    birthRand = random.random()
    if birthRand < self.birthProb:
      majorRand = random.random()
      if majorRand < self.majorProb and tribe == "major":
        return ant.Ant(tribe, antType)
      elif majorRand >= self.majorProb and tribe == "minor":
        return ant.Ant(tribe, antType)
      else:
        return EMPTY
    else:
      return EMPTY

  # Cell coordinates, and the number of minor or major enemy ants
  # required to kill the ant at the given cell.
  #
  # Returns either the type of enemy ant that kills the current ant,
  # or the empty string if the death conditions aren't met.
  def isDeathCondition(self, r, c, noOfMinors, noOfMajors):
    minorCount = 0
    majorCount = 0
    adjTribes = []
    for (i, j) in self.genCheckList(r, c):
      if self.isEnemyAnt(self.grid[r][c], self.grid[i][j], "minor"):
        minorCount = minorCount + 1
        adjTribes.append(self.grid[i][j].tribe)
      elif self.isEnemyAnt(self.grid[r][c], self.grid[i][j], "major"):
        majorCount = majorCount + 1
        adjTribes.append(self.grid[i][j].tribe)
    # Determine the most common enemy tribe
    tribeCounts = collections.Counter(adjTribes)
    if minorCount >= noOfMinors:
      return ("minor", tribeCounts.most_common(1)[0][0])
    elif majorCount >= noOfMajors:
      return ("major", tribeCounts.most_common(1)[0][0])
    else:
      return ("", "")

  def genCheckList(self, r, c):
    (maxr, maxc) = self.grid.shape
    cells = [((r-1) % maxr, c), ((r+1) % maxr, c), (r, (c-1) % maxc),
        (r, (c+1) % maxc)]

    if self.checkDiag:
      # Add diagonal cells
      cells.extend([((r-1) % maxr, (c-1) % maxc), ((r-1) % maxr, (c+1) % maxc),
        ((r+1) % maxr, (c-1) % maxc), ((r+1) % maxr, (c+1) % maxc)])
    return cells

  # Checks to see if the ant adjacent to the current ant
  # is an enemy ant, and of the expected type (minor/major)
  def isEnemyAnt(self, currAnt, adjAnt, expectedType):
    if adjAnt == EMPTY:
      return False
    elif (currAnt.tribe != adjAnt.tribe) and adjAnt.antType == expectedType:
      return True
    else:
      return False

  def printGrid(self):
    (r, c) = self.grid.shape
    for i in range(r):
      for j in range(c):
        if self.grid[i][j] == EMPTY:
          print colorama.Back.BLACK + " ",
        elif self.grid[i][j].tribe == "red" and self.grid[i][j].antType == "minor":
          print colorama.Back.MAGENTA + " ",
        elif self.grid[i][j].tribe == "red" and self.grid[i][j].antType == "major":
          print colorama.Back.RED + " ",
        elif self.grid[i][j].tribe == "blue" and self.grid[i][j].antType == "minor":
          print colorama.Back.CYAN + " ",
        elif self.grid[i][j].tribe == "blue" and self.grid[i][j].antType == "major":
          print colorama.Back.BLUE + " ",
      print colorama.Back.RESET

