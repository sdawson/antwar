# A class to keep track of the ant deaths 
class AntStats(object):
  def __init__(self, tribes, size):
    self.tribes = tribes
    # A list of number of deaths per step, one list per tribe
    self.majorDeaths = [[0]*size**2 for n in range(len(tribes))]
    self.minorDeaths = [[0]*size**2 for n in range(len(tribes))]

  # Takes lists of major and minor ant death counts
  # for each tribe, and updates the total counts
  def updateStats(self, majorDeaths, minorDeaths):
    for (tribeId, tribe) in enumerate(self.tribes):
      self.majorDeaths[tribeId][majorDeaths[tribeId]] = \
          self.majorDeaths[tribeId][majorDeaths[tribeId]] + 1
      self.minorDeaths[tribeId][minorDeaths[tribeId]] = \
          self.minorDeaths[tribeId][minorDeaths[tribeId]] + 1

  def writeToFile(self, filename):
    f = open(filename, "w")
    titles = self._createColTitles()
    f.write(titles)
    for i in range(len(self.majorDeaths[0])):
      f.write("%d\t" % i)
      for (tn, t) in enumerate(self.tribes):
        if tn == 0:
          f.write("%d\t%d" % (self.majorDeaths[tn][i], self.minorDeaths[tn][i]))
        else:
          f.write("\t%d\t%d" % (self.majorDeaths[tn][i], self.minorDeaths[tn][i]))
      f.write("\n")
    f.close()


  def _createColTitles(self):
    titles = ["NoOfDeaths"]
    for tribe in self.tribes:
      titles.extend([tribe + "MajDeath", tribe + "MinDeath"])
    return "\t".join(titles) + "\n"
