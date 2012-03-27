# A class to keep track of the ant deaths 
class AntStats(object):
  def __init__(self, tribes, size):
    self.tribes = tribes
    # A list of number of deaths per step, one list per tribe
    self.majorDeaths = [[0]*size**2]*len(tribes)
    print self.majorDeaths
    self.minorDeaths = [[0]*size**2]*len(tribes)
    print self.minorDeaths

  # Takes lists of major and minor ant death counts
  # for each tribe, and updates the total counts
  def updateStats(self, majorDeaths, minorDeaths):
    for tribeId in range(0, len(self.tribes)):
      self.majorDeaths[tribeId][majorDeaths[tribeId]] = \
          self.majorDeaths[tribeId][majorDeaths[tribeId]] + 1
      self.minorDeaths[tribeId][minorDeaths[tribeId]] = \
          self.minorDeaths[tribeId][minorDeaths[tribeId]] + 1
