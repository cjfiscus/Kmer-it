#!/usr/bin/env python3
# tally GC per sample

import sys
import os
import gzip

def count_gc(sequence):
    """Counts the number of Gs and Cs in a sequence."""
    return sequence.count('G') + sequence.count('C')

def sum_by_all_gc_contents(filename):
    """Sums the values in the second column for each GC count."""
    gc_sums = {}

    # Open the file, supporting both plain text and gzipped files
    if filename.endswith('.gz'):
        file = gzip.open(filename, 'rt')
        sample_name = os.path.basename(filename[:-3])
        sample_name = os.path.splitext(sample_name)[0]
    else:
        file = open(filename, 'r')
        sample_name = os.path.basename(os.path.splitext(filename)[0])

    with file:
        for line in file:
            sequence, value = line.split()
            gc_count = count_gc(sequence)
            value = int(value)
            
            if gc_count in gc_sums:
                gc_sums[gc_count] += value
            else:
                gc_sums[gc_count] = value
    
    return gc_sums, sample_name

##########
filename = sys.argv[1] 

result, sample_name = sum_by_all_gc_contents(filename)

for gc_count, total_sum in sorted(result.items()):
    print(f"{sample_name}\t{gc_count}\t{total_sum}")
