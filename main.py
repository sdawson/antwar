import grid, os, time

def main():
  initGrid = grid.Grid(30, ["red", "blue"], 0.10, 0.05, True)
  #initGrid = grid.Grid(30, ["red", "blue"], 0.5, 0.22, True)
  for i in range(2000):
    initGrid.updateGrid()
    if i % 10 == 0:
      time.sleep(.5)
      os.system('cls' if os.name == 'nt' else 'clear')
      initGrid.printGrid()
  initGrid.antStats.writeToFile("2teams-2000steps-0.10p-0.05f-diag-withcapping")

if __name__ == "__main__":
  main()
