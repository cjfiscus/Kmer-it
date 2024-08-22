# Kmer-it: A Snakemake Workflow to Generate K-mer Profiles from High-Throughput Sequencing Reads
Kmer-it is a flexible Snakemake workflow to generate genome content profiles from K-mer abundances in high-throughput sequencing reads.

The workflow takes as input raw or gzipped [FASTQ files](https://en.wikipedia.org/wiki/FASTQ_format) and counts K-mer frequencies in each file. Reads can be optionally adapter and quality trimmed with trimmomatic, read-error corrected with bayeshammer, and then filtered of likely organellar sequences by mapping against organellar genomes. K-mer frequencies are then normalized to correct %GC and coverage differences between samples. Finally, the K-mer frequencies can be used to estimate the copy number of given sequences in a multi-FASTA.


The workflow takes as input sequencing reads either Sequence Read Archive (SRA) accessions or paths to FASTQ sequencing files and (optionally) trims
adapters and poor quality sequence with trimmomatic. To reduce contamination from organellar genomes, trimmed reads are then
mapped to organelle genomes from the [NCBI Organelle Genome Database](https://www.ncbi.nlm.nih.gov/genome/organelle/). K-mers are then
counted in unmapped reads with jellyfish. K-mer abundance is then normalized across samples using a custom Rscript.

## Installation
1. Clone this repository:
`git clone https://github.com/cjfiscus/Kmer-it.git`

2. Move into cloned repo
`cd Kmer-it`

3. [If needed, install mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html#)

4. Install dependencies with mamba:
`mamba env create -n kmerit -f workflow/envs/environment.yaml`

5. Activate environment:
`mamba activate kmerit`


## Running the workflow

## Citation
If you use this software, please cite:
(citation)
