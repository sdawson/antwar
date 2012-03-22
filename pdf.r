# Clear variables
rm(list=ls())

graph_file <- function(infile, outfile) {
  graph_par <- par(las = 0, mar = c(4, 4, 3, 2))
  col_names <- NULL
  if (isYoungAndOld) {
    col_names <- c("noofdeaths", "oldblue", "youngblue", "oldred", "youngred")
  } else {
    col_names <- c("noofdeaths", "minblue", "majblue", "minred", "majred")
  }
  file_contents <- read.table(infile, skip=2, sep="\t", col.names=col_names, dec=".")

  pdf(file = outfile)
  # Plotting minor ant pdf
  if (isYoungAndOld) {
    plot(density(file_contents$oldblue), col="green", axes=FALSE, xlab="", ylab="", main="")
    par(new=TRUE)
    plot(density(file_contents$youngblue), col="blue", axes=FALSE, xlab="", ylab="", main="")
    par(new=TRUE)
    plot(density(file_contents$oldred), col="orange", axes=FALSE, xlab="", ylab="", main="")
    par(new=TRUE)
    plot(density(file_contents$youngred), col="red", axes=FALSE, xlab="", ylab="", main="")
    legend(x = 50, y = 0.05, c("Old Blue", "Young Blue", "Old Red", "Young Red"),
          col=c("green", "blue", "orange", "red"), lty=1, bty="n")
  } else {
    plot(density(file_contents$minblue), col="green", axes=FALSE, xlab="", ylab="", main="")
    par(new=TRUE)
    plot(density(file_contents$majblue), col="blue", axes=FALSE, xlab="", ylab="", main="")
    par(new=TRUE)
    plot(density(file_contents$minred), col="orange", axes=FALSE, xlab="", ylab="", main="")
    par(new=TRUE)
    plot(density(file_contents$majred), col="red", axes=FALSE, xlab="", ylab="", main="")
    legend(x = 500, y = 0.10, c("Blue Minors", "Blue Majors", "Red Minors", "Red Majors"),
          col=c("green", "blue", "orange", "red"), lty=1, bty="n")
  }
  axis(1)
  axis(2)
  box()
  title(main="Ant Death PDFs", xlab="Number of Deaths", ylab="Density")
  dev.off()
}

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
outfile <- args[2]
isYoungAndOld <- as.logical(args[3])

graph_file(infile, outfile)
