#!/usr/bin/env Rscript
# calc median %GC per bin

args <- commandArgs(trailingOnly = TRUE)

if (!require("pacman")) install.packages("pacman")
library(pacman)
p_load(tidyverse)

# import data
df<-read.table(args[1])
names(df)<-c("lib", "gc", "count")

## calc prop of counts per GC bin
df<-df %>% group_by(lib) %>% mutate(s=sum(count))
df$prop<-df$count/df$s

## calc med prop across ids
df1 <- df %>% group_by(gc) %>% summarize(m=median(prop))

## scale to %
df1$prop<-df1$m/sum(df1$m)

write.table(df1[,c("gc", "prop")], args[2], sep="\t", quote=F, row.names=F)
