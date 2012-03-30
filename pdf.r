# Clear variables
rm(list=ls())

graph_file <- function(infile, outfile) {
  graph_par <- par(las = 0, mar = c(4, 4, 3, 2))
  # Colours taken from the University of Oregon Data Graphic Research list
  # of colour schemes appropriate for scientific data graphs.
  colours <- c(rgb(1.0, 0.5, 0.0), rgb(1.0, 1.0, 0.2), rgb(0.2, 1.0, 0.0),
               rgb(0.1, 0.7, 1.0), rgb(0.4, 0.3, 1.0), rgb(0.9, 0.1, 0.2),
               rgb(1.0, 0.75, 0.5), rgb(1.0, 1.0, 0.6), rgb(0.7, 1.0, 0.55),
               rgb(0.65, 0.93, 1.0), rgb(0.8, 0.75, 1.0), rgb(1.0, 0.6, 0.75))
  file_contents <- read.table(infile, header=TRUE, sep="\t")
  # Extract every column except the first (which contains the general number of deaths per step)
  deathColumns <- file_contents[-(1:1)]
  str(deathColumns)

  #pdf(file = outfile)
  ## Plotting minor ant pdf
  #if (isYoungAndOld) {
  #  plot(density(file_contents$oldblue), col="green", axes=FALSE, xlab="", ylab="", main="")
  #  par(new=TRUE)
  #  plot(density(file_contents$youngblue), col="blue", axes=FALSE, xlab="", ylab="", main="")
  #  par(new=TRUE)
  #  plot(density(file_contents$oldred), col="orange", axes=FALSE, xlab="", ylab="", main="")
  #  par(new=TRUE)
  #  plot(density(file_contents$youngred), col="red", axes=FALSE, xlab="", ylab="", main="")
  #  legend(x = 50, y = 0.05, c("Old Blue", "Young Blue", "Old Red", "Young Red"),
  #        col=c("green", "blue", "orange", "red"), lty=1, bty="n")
  #} else {
  #  plot(density(file_contents$minblue), col="green", axes=FALSE, xlab="", ylab="", main="")
  #  par(new=TRUE)
  #  plot(density(file_contents$majblue), col="blue", axes=FALSE, xlab="", ylab="", main="")
  #  par(new=TRUE)
  #  plot(density(file_contents$minred), col="orange", axes=FALSE, xlab="", ylab="", main="")
  #  par(new=TRUE)
  #  plot(density(file_contents$majred), col="red", axes=FALSE, xlab="", ylab="", main="")
  #  legend(x = 500, y = 0.10, c("Blue Minors", "Blue Majors", "Red Minors", "Red Majors"),
  #        col=c("green", "blue", "orange", "red"), lty=1, bty="n")
  #}
  #axis(1)
  #axis(2)
  #box()
  #title(main="Ant Death PDFs", xlab="Number of Deaths", ylab="Density")
  #dev.off()
}

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
outfile <- args[2]

graph_file(infile, outfile)
