# Clear variables
rm(list=ls())

graph_file <- function(infile, outfile) {
  graph_par <- par(las = 0, mar = c(4, 4, 3, 2))
  file_contents <- read.table(infile, skip=2, sep="\t", col.names=c("mad",
    "mid", "redd", "blued", "sma", "smi"), dec=".")

  pdf(file = outfile)
  # Plotting minor ant pdf
  plot(density(file_contents$smi), axes=FALSE, xlab="", ylab="", main="")
  axis(1)
  axis(2)
  box()
  title(main="Minor Ant Death PDF", xlab="Minor ant deaths per time step",
        ylab="Density")

  # plotting major ant pdf
  plot(density(file_contents$sma), axes=FALSE, xlab="Major ant deaths per time 
       step", ylab="Density", main="Major Ant Death PDF")
  axis(1)
  axis(2)
  box()
  dev.off()
}
