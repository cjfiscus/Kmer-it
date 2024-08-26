#!/usr/bin/env Rscript

# install/ load required libs 
library(pacman)
pacman::p_load(data.table, edgeR)

args = commandArgs(trailingOnly=TRUE)

# tmm normalize gc corrected kmer counts

# read in K-mer counts 
counts<-fread(args[1])
norm_me<-args[3]

# what the data looks like 
dim(counts) 
counts[1:5,1:5]

info<-counts[,1]

# TMM normalize counts
factors<-calcNormFactors(DGEList(counts[,2:ncol(counts)]), method=norm_me)
rm(counts) # the purge
gc()
counts<-cpm(factors)
rm(factors)
gc()
out<-as.data.table(cbind(info, counts))
rm(counts)
gc()

## write out normalized counts
fwrite(out, file=args[2], sep="\t", quote=F)
