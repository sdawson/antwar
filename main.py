import grid, os, time

def main():
  initGrid = grid.Grid(30, ["red", "blue"], 0.04, 0.12, True)
  for i in range(4000):
    initGrid.updateGrid()
    #if i % 10 == 0:
      #time.sleep(.5)
      #os.system('cls' if os.name == 'nt' else 'clear')
      #initGrid.printGrid()
      #print i
  #print initGrid.antStats.tribes
  #print initGrid.antStats.majorDeaths
  #print initGrid.antStats.minorDeaths
  initGrid.antStats.writeToFile("2teams-4000steps-0.5p-0.25f-diag")

if __name__ == "__main__":
  main()
