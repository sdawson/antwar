import grid, os, time

def main():
  initGrid = grid.Grid(30, ["red", "blue"], 0.1, 0.05, True)
  for i in range(200):
    initGrid.updateGrid()
    if i % 10 == 0:
      time.sleep(.5)
      os.system('cls' if os.name == 'nt' else 'clear')
      initGrid.printGrid()
      print i
  print initGrid.antStats.tribes
  print initGrid.antStats.majorDeaths
  print initGrid.antStats.minorDeaths

if __name__ == "__main__":
  main()
