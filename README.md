# Kmer-it: A Snakemake Workflow to Generate K-mer Profiles from High-Throughput Sequencing Reads  
Kmer-it is a flexible Snakemake workflow to generate K-mer profiles from high-throughput sequencing reads.  

The workflow takes as input either Sequence Read Archive (SRA) accessions or paths to FASTQ sequencing runs and trims
adapters and poor quality sequence with trimmomatic. To reduce contamination from organellar genomes, trimmed reads are then 
mapped to organelle genomes from the [NCBI Organelle Genome Database](https://www.ncbi.nlm.nih.gov/genome/organelle/). K-mers are then
counted in unmapped reads with jellyfish. K-mer abundance is then normalized across samples using a custom Rscript. 

## Installation
1. Clone this repository:  
`git clone https://github.com/cjfiscus/Kmer-it.git`  

2. [Install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/#regular-installation) (if needed), 
then install dependencies with conda:  
`conda env create -n kmerit -f workflow/envs/environment.yaml`  

3. Activate environment:  
`conda activate kmerit`

## Running the workflow

## Citation
If you use this software, please cite:
(citation)
