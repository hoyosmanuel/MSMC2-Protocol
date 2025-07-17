### 1. Set Directories:
```
mkdir –p /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes
```

### 2. Get the genomes:
```
# This is my SRA Toolkit path:
export PATH=/lustre/work/mhoyosro/software/sratoolkit/bin:${PATH}

# I am going to explore this sequencing experiment from the Broad Institute
prefetch --max-size 99999999999 SRR7704823

# As a reference I am going to use the Genome assembly mMyoMyo1.p from Bat1k August 2020
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_014108235.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT"

# I'm going to rename the _Myotis myotis_ reference genome as mMyo.fa
# It will be stored in /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes.
```

### 3. Unpack and index the genome: 
```
# Unpack
fasterq-dump SRR7704823.sra

# Load the necessary modules for the programs I need.
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

# Index
bwa index mMyo.fa
```

### 4. Start Mappability Mask of the reference genome 

















