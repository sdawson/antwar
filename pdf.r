# Clear variables
rm(list=ls())

graph_file <- function(infile, outfile, isMultipleMajor) {
  graph_par <- par(las = 0, mar = c(4, 4, 3, 2))
  col_names <- c("steps", "minblue", "majblue", "minred", "majred")
  file_contents <- read.table(infile, skip=2, sep="\t", col.names=col_names, dec=".")

  pdf(file = outfile)
  # Plotting minor ant pdf
  plot(density(file_contents$minblue), col="green", axes=FALSE, xlab="", ylab="", main="")
  par(new=TRUE)
  plot(density(file_contents$majblue), col="blue", axes=FALSE, xlab="", ylab="", main="")
  par(new=TRUE)
  plot(density(file_contents$minred), col="yellow", axes=FALSE, xlab="", ylab="", main="")
  par(new=TRUE)
  plot(density(file_contents$majred), col="red", axes=FALSE, xlab="", ylab="", main="")
  axis(1)
  axis(2)
  box()
  title(main="Minor Ant Deaths", xlab="Minor ant deaths per time step",
        ylab="Density")

  ## plotting major ant pdf
  #if (isMultipleMajor) {
  #  plot(density(file_contents$redsma), axes=FALSE, xlab="Red Major ant deaths
  #               per time step", ylab="Density", main="Red Major Ant Deaths")
  #  axis(1)
  #  axis(2)
  #  box()
  #  plot(density(file_contents$bluesma), axes=FALSE, xlab="Blue Major ant deaths
  #               per time step", ylab="Density", main="Blue Major Ant Deaths")
  #  axis(1)
  #  axis(2)
  #  box()
  #} else {
  #  plot(density(file_contents$sma), axes=FALSE, xlab="Major ant deaths per time
  #       step", ylab="Density", main="Major Ant Deaths")
  #  axis(1)
  #  axis(2)
  #  box()
  #}
  dev.off()
}

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
outfile <- args[2]
isMultipleMajor <- as.logical(args[3])

graph_file(infile, outfile, isMultipleMajor)
