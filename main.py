import grid, os, time

def main():
  initGrid = grid.Grid(30, ["red", "blue"], 0.04, 0.12, True)
  #initGrid = grid.Grid(30, ["red", "blue"], 0.5, 0.22, True)
  for i in range(2000):
    initGrid.updateGrid()
    if i % 10 == 0:
      time.sleep(.5)
      os.system('cls' if os.name == 'nt' else 'clear')
      initGrid.printGrid()
      print i
  initGrid.antStats.writeToFile("2teams-2000steps-0.04p-0.12f-diag")

if __name__ == "__main__":
  main()
