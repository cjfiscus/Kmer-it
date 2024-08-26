#!/usr/bin/env Rscript
# quantile-quantile count normalization
# cjfiscus

# load pkgs
library(pacman)
p_load(data.table, limma)

# read args
args = commandArgs(trailingOnly=TRUE)

# read in counts
counts<-fread(args[1])

# take a peek
dim(counts)
counts[1:5,1:5]

# save kmers
kmers<-counts[,1]

# normalize
norm<-voom(counts[,2:ncol(counts)], normalize.method="quantile", save.plot=T)

# cleanup
rm(counts)

# write out plot data
p<-as.data.frame(cbind(norm$voom.xy$x, norm$voom.xy$y))
names(p)<-c(norm$voom.xy$xlab, norm$voom.xy$ylab)
write.table(p, "voom_mean_var.txt", sep="\t", quote=F, row.names=F)

# write out normalized counts
counts<-as.data.table(cbind(kmers, norm$E))
fwrite(counts, file=args[2], sep="\t", quote=F)
