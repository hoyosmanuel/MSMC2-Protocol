### 1. Set Directories:
   
```
mkdir –p /lustre/scratch/mhoyosro/project1/artibeus_lituratus
cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus
```
### 2. Get the genomes:
These Genomes were provided by Nancy Simmons and Sonja Vernes to generate a high-quality reference genome for the Bat1K and are deposited in GenBank

```
export PATH=/lustre/work/mhoyosro/software/sratoolkit/bin:${PATH}
prefetch --max-size 99999999999 SRR28746557
prefetch --max-size 99999999999 SRR28746558
prefetch --max-size 99999999999 SRR28746559
prefetch --max-size 99999999999 SRR28746560
prefetch --max-size 99999999999 SRR28746561
prefetch --max-size 99999999999 SRR28746562
prefetch --max-size 99999999999 SRR28746563
prefetch --max-size 99999999999 SRR28746564
```
As a reference I am going to use this *A. lituratus* genome assembly mArtLit1.hap2 (2024). Isolate: mArtLit1.

```
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_038363175.2/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=RNA_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=SEQUENCE_REPORT&hydrated=FULLY_HYDRATED"
```

Colected in Belize: Orange Walk District, Lamanai

![image](https://github.com/user-attachments/assets/eb9c34ca-1070-43dd-b1d3-684ba528152e)



# Unpack the SRA
fasterq-dump -e 1O SRR28746557.sra
fasterq-dump -e 1O SRR28746558.sra
fasterq-dump -e 1O SRR28746559.sra
fasterq-dump -e 1O SRR28746560.sra
fasterq-dump -e 1O SRR28746561.sra
fasterq-dump -e 1O SRR28746562.sra
fasterq-dump -e 1O SRR28746563.sra
fasterq-dump -e 1O SRR28746564.sra


3. Index the reference genome: 
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11
 
bwa index aLit_REF.fasta


4. Start the mappability mask:
cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus
nano mask_1.sh

#!/bin/bash
#SBATCH --job-name=maskAL
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11
# Enter into the directory
cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus
# Put the Splitfa software into the path
export PATH=/lustre/scratch/mhoyosro/project1/MSMC2/seqbility-20091110:${PATH}
# Break down the reference genome in kmers
mkdir x_files
splitfa aLit_REF.fasta | split -l 20000000
mv x* x_files
cd x_files
cat x* >> ../REF_splitted
cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus
# Aling the spplited reference to the reference itself
bwa aln -t 64 -R 1000000 -O 3 -E 3  aLit_REF.fasta  REF_splitted  >  REF_splitted.sai 
# Pass the sai file to a sam file
BWA_THREAD=64 bwa samse -f REF_splitted.sam  aLit_REF.fasta REF_splitted.sai  REF_splitted 
# Create the RawMask
perl /lustre/scratch/mhoyosro/project1/MSMC2/seqbility-20091110/gen_raw_mask.pl  REF_splitted.sam  > aLit_rawmask.fa
# Create the Mask
/lustre/scratch/mhoyosro/project1/MSMC2/seqbility-20091110/gen_mask -l 35 -r 0.5 aLit_rawmask.fa  > aLit_mask.fa



5. Finish the Mask of the reference genome script: 

# Prepare the mask creator

cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus
mkdir masks

Inside of the folder /lustre/scratch/mhoyosro/project1/MSMC2/msmc-tools-master there is a python script called makeMappabilityMask.py

Edit line 26 to be: 
with open("/lustre/scratch/mhoyosro/project1/artibeus_lituratus/aLit_mask.fa", "r") as f:

Edit line 30 to be: 
mask = MaskGenerator("/lustre/scratch/mhoyosro/project1/artibeus_lituratus/masks/{}.mask.bed.gz".format(chr), chr)


# Run the mask creator
cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus
nano mask_2.sh

#!/bin/bash
#SBATCH --job-name=rawmask
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

. ~/conda/etc/profile.d/conda.sh
conda activate py2
python /lustre/scratch/mhoyosro/project1/MSMC2/msmc-tools-master/makeMappabilityMask.py



6. Map  the samples against the reference genome: 

nano mapping.sh

#!/bin/bash
#SBATCH --job-name=mapping
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus

BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746557.fastq >  SRR28746557_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746558.fastq >  SRR28746558_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746559.fastq >  SRR28746559_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746560.fastq >  SRR28746560_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746561.fastq >  SRR28746561_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746562.fastq >  SRR28746562_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746563.fastq >  SRR28746563_se.sam
BWA_THREAD=64 bwa mem -t 64 aLit_REF.fasta SRR28746564.fastq >  SRR28746564_se.sam



7. Convert to bam and index (being the previous job 12638832)

nano bamming.sh
 
#!/bin/bash
#SBATCH --dependency=afterok:13504203
#SBATCH --job-name=bamming
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

cd /lustre/scratch/mhoyosro/project1/artibeus_lituratus

OMP_NUM_THREADS=64 samtools view -bS SRR28746557_se.sam > SRR28746557.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746557.sorted.bam SRR28746557.bam
OMP_NUM_THREADS=64 samtools index SRR28746557.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746558_se.sam > SRR28746558.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746558.sorted.bam SRR28746558.bam
OMP_NUM_THREADS=64 samtools index SRR28746558.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746559_se.sam > SRR28746559.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746559.sorted.bam SRR28746559.bam
OMP_NUM_THREADS=64 samtools index SRR28746559.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746560_se.sam > SRR28746560.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746560.sorted.bam SRR28746560.bam
OMP_NUM_THREADS=64 samtools index SRR28746560.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746561_se.sam > SRR28746561.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746561.sorted.bam SRR28746561.bam
OMP_NUM_THREADS=64 samtools index SRR28746561.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746562_se.sam > SRR28746562.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746562.sorted.bam SRR28746562.bam
OMP_NUM_THREADS=64 samtools index SRR28746562.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746563_se.sam > SRR28746563.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746563.sorted.bam SRR28746563.bam
OMP_NUM_THREADS=64 samtools index SRR28746563.sorted.bam

OMP_NUM_THREADS=64 samtools view -bS SRR28746564_se.sam > SRR28746564.bam
OMP_NUM_THREADS=64 samtools sort -o SRR28746564.sorted.bam SRR28746564.bam
OMP_NUM_THREADS=64 samtools index SRR28746564.sorted.bam
![image](https://github.com/user-attachments/assets/21ea1db6-2ef0-4e1b-8e63-6f2db1f391ee)

