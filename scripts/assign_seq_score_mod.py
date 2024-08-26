#!/usr/bin/env python
import sys
import re
import os
import statistics
from Bio import SeqIO
from Bio import Seq
from Bio.Data import IUPACData
from itertools import product 
import numpy as np

#By Dan Koenig 2018, modified by Chris Fiscus 2019,2022
#Script to use Kmer table to calculate median values for a genomic sequence
#Each kmer in the fasta sequence will be assigned the value from the kmer table and then a global median will be taken for the sequences
#Kmers not found in the table will be ignored
#Values for Kmers with ambiguous nucleotides is the mean for all possible Kmers that could compose that seq 

#command line inputs:
#1: kmer table file
#Input kmer table format is tab delimited two column 1: kmer 2: statistic
#f = gzip.open(sys.argv[1], 'r')
#2: fasta file
#3: length of kmer to analyze (should be consistent with kmer table)
#Returned values:
#1: Chromosome
#2: Region start position
#3: Region end position
#4: median value for the region
#5: number of kmers used for #4
#If no kmers are found that match the kmer table NA will be returned for the median value

#################################################################################################
#################################################################################################
#############################FUNCTIONS###########################################################
#################################################################################################
#################################################################################################
#Function to reverse complement sequences in the input kmer table
revcompl = lambda x: ''.join([{'A':'T','C':'G','G':'C','T':'A'}[B] for B in x][::-1])
#Function to process individual fasta
def processthisseq (fastaseq,merlen,keyindex,normd):
    fastaseq = fastaseq.upper()
    sum_score = []
    sum_score2 = []
    kmercount = 0
    kmercount2 = 0
    for i in range(0,len(fastaseq)):
        if len(fastaseq[i:i + merlen]) == merlen and fastaseq[i:i+merlen] in keyindex:
            kmercount += 1
            sum_score.append(float(keyindex[fastaseq[i:i+merlen]]))
        elif len(fastaseq[i:i + merlen]) == merlen and fastaseq[i:i+merlen] not in keyindex:
            possibleseqs=listseqs(fastaseq[i:i+merlen])
            possibleseqs=[item for sublist in possibleseqs for item in sublist]
            if len(possibleseqs) > 1: # multiple possible kmers due to ambiguity
                score=0
                for j in possibleseqs:
                    try:
                        score = score + float(keyindex[j])
                    except:
                        pass
                score=score/len(possibleseqs)
                kmercount += 1
                sum_score.append(float(score))
    if kmercount >0: # trim kmers in top and bot 25% of range
        max_score=np.max(sum_score)
        min_score=np.min(sum_score)
        qtr_rng=(max_score-min_score)/4
        for i in sum_score:
            if i >= (min_score + qtr_rng):
                if i <= (max_score - qtr_rng):
                    sum_score2.append(float(i))
                    kmercount2 +=1
    if kmercount2 >0:
        return [statistics.median(sum_score2),kmercount2]
    else:
        return ["NA",kmercount]
#Function to list all possible seqs with ambiguous characters
#attributed to Jivan, https://stackoverflow.com/questions/27551921/how-to-extend-ambiguous-dna-sequence
def listseqs(seq):
   d = IUPACData.ambiguous_dna_values
   return [ list(map("".join, product(*map(d.get, seq)))) ]
#################################################################################################
#################################################################################################
#############################COMMANDLINE PARAMETERS##############################################
#################################################################################################
#################################################################################################
tablefile = sys.argv[1]
g = sys.argv[2]
merlen = int(sys.argv[3])

#################################################################################################
#################################################################################################
#############################KMER TABLE PARSE AND STORE##########################################
#################################################################################################
#################################################################################################
#create a dictionary with kmer keys and table values from the input table
#Will reverse complment every kmer and add it to the dictionary with the same value
keydata = {}
fulldata = 0
with open(tablefile,'r') as f:
    for line in f:
        if not line: break
        line = line.rstrip('\n')
        linesplit = line.split()
        fulldata += float(linesplit[1])
        keydata[str(linesplit[0])] = linesplit[1]
        keydata[revcompl(str(linesplit[0]))] = linesplit[1]
f.close
#################################################################################################
#################################################################################################
#############################FASTA PARSE AND SCORE CALCULATIONS##################################
#################################################################################################
#################################################################################################
with open(g, "r") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        seqscore = processthisseq(record.seq,merlen,keydata,fulldata)
        if seqscore[1] > 0:
            print (record.id + '\t' + str(round(seqscore[0],4)) + "\t" + str(seqscore[1]))
        else:
            print (record.id+"\t"+"NA"+"\t"+"0")
