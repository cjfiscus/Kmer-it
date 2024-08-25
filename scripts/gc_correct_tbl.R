#!/usr/bin/env Rscript

# install/ load required libs 
if (!require("pacman")) install.packages("pacman")
pacman::p_load(data.table, matrixStats, stringr, tidyverse)

# correct raw kmer counts by proportion of lib
# in each gc bin 

# read sysargs
args = commandArgs(trailingOnly=TRUE)

## FUNCTIONS ## 
# define GC correction function 
CorrectGC<-function(column){
  ## aggregate bins 
  gc<-data.table(cbind(GC_content, column))
  names(gc)<-c("GC_content", "column")
  gc<-as.data.frame(gc[,sum(column),by=GC_content])
  names(gc)<-c("GC_content", "column")
  
  ## merge reference table with table for column
  gc<-merge(REF, gc, by="GC_content")
  
  ## calculate weights
  gc$Proportion2<-gc$column/as.numeric(sum(gc$column))
  weights<-gc$Proportion/gc$Proportion2
  names(weights)<-gc$GC_content
  
  # column name that is being processed
  gc$Library<-names(counts)[i]
  i<<-i+1 # this is bad practice but could not find another way
  
  proportions<<-rbind(proportions, cbind(gc$Library, gc$GC_content, round(gc$Proportion2, 4)))
  
  ## apply weights
  Correction<-as.data.frame(cbind(column, GC_content))
  keys<-sapply(Correction[,2], function(x) weights[[as.character(x)]]) # get factors 
  Correction$Cts<-round(Correction$column*keys) # apply correction
  return(Correction$Cts)
}

#####

# read in K-mer counts 
counts<-fread(args[1])

# calc gc prop per lib
gc_props<-read.table(args[3])
names(gc_props)<-c("lib", "gc", "count")

gc_props<-gc_props %>% group_by(lib) %>% mutate(s=sum(count))
gc_props$propo<-gc_props$count/gc_props$s

# read in ref
gc_ref<-read.delim(args[4])
gc_props<-merge(gc_props, gc_ref, by="gc")
gc_props$key<-gc_props$prop/gc_props$propo
gc_props<-gc_props[,c("lib", "gc", "key")]
rm(gc_ref)

## add gc per kmer
gc_kmer<-str_count(counts$mer, pattern="G|C")

# correct counts
choose_cols=colnames(counts)[2:length(counts)]
for (i in choose_cols){
  sub<-gc_props[gc_props$lib==i,]
  
  temp<-as.data.frame(cbind(gc_kmer, counts[[i]]))
  names(temp)<-c("gc", "raw")
  temp<-merge(temp, sub, by="gc")
  temp$prod<-temp$raw*temp$key
  counts[[i]]<-temp$prod
  
}

# write kmer table out
fwrite(counts, file=args[2], sep="\t", quote=F)

