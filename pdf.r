# Clear variables
rm(list=ls())

graph_file <- function(infile, outfile) {
  graph_par <- par(las = 0, mar = c(4, 4, 3, 2))
  # Colours taken from the University of Oregon Data Graphic Research list
  # of colour schemes appropriate for scientific data graphs.
  colours <- c(rgb(1.0, 0.5, 0.0), rgb(0.9, 0.1, 0.2), rgb(0.2, 1.0, 0.0),
               rgb(0.1, 0.7, 1.0), rgb(0.4, 0.3, 1.0), rgb(1.0, 1.0, 0.2),
               rgb(1.0, 0.75, 0.5), rgb(1.0, 1.0, 0.6), rgb(0.7, 1.0, 0.55),
               rgb(0.65, 0.93, 1.0), rgb(0.8, 0.75, 1.0), rgb(1.0, 0.6, 0.75))
  file_contents <- read.table(infile, header=TRUE, sep="\t")
  # Extract every column except the first (which contains the general number of deaths per step)
  deathColumns <- file_contents[-(1:1)]
  str(deathColumns)
  cat(ncol(deathColumns), '\n')
  
  pdf(file = outfile)
  plot(density(deathColumns[[1]]), col=colours[1], axes=FALSE, xlab="", ylab="", main="")#, xlim=c(-30, 100))
  par(new=T)
  plot(density(deathColumns[[2]]), col=colours[2], axes=FALSE, xlab="", ylab="", main="")# xlim=c(-30, 100))
  par(new=T)
  plot(density(deathColumns[[3]]), col=colours[3], axes=FALSE, xlab="", ylab="", main="")# xlim=c(-30, 100))
  par(new=T)
  plot(density(deathColumns[[4]]), col=colours[4], axes=FALSE, xlab="", ylab="", main="")# xlim=c(-30, 100))

  legend("topright", names(deathColumns), col=colours[1:ncol(deathColumns)], 
         lty=1, bty="n")
  axis(1)
  axis(2)
  box()
  title(main="Ant Death PDFs", xlab="Number of Deaths", ylab="Density")
  dev.off()
}

args <- commandArgs(trailingOnly = TRUE)
infile <- args[1]
outfile <- args[2]

graph_file(infile, outfile)
