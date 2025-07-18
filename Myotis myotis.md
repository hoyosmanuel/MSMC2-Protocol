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
```
#!/bin/bash
#SBATCH --job-name=mask
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=8

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

# Path for Splitfa
export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110:${PATH}
# Break down the reference genome in kmers
mkdir x_files
splitfa mMyo.fa | split -l 20000000
mv x* x_files
cd x_files
cat x* >> ../REF_splitted
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

# Aling the spplited reference to the reference itself
bwa aln -t 20 -R 1000000 -O 3 -E 3 mMyo.fa  REF_splitted  >  REF_splitted.sai 

# Convert the sai file to a sam file
BWA_THREAD=12 bwa samse -f REF_splitted.sam mMyo.fa REF_splitted.sai  REF_splitted 

# Create the Mask
perl /lustre/work/mhoyosro/software/seqbility/seqbility-20091110/gen_raw_mask.pl  REF_splitted.sam  > mMyo_rawmask.fa

/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/gen_mask -l 35 -r 0.5 mMyo_rawmask.fa  > mMyo_mask.fa
```

### 5. Finish the Mappability Mask
```
# Prepare the mask creator
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes
mkdir masks
```
Inside of **msmc_tools** there is a python script called **makeMappabilityMask.py**

Edit line 26 to be: 
with open("/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/mMyo_mask.fa", "r") as f:
Edit line 30 to be: 
mask = MaskGenerator("/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/masks/{}.mask.bed.gz".format(chr), chr)
```
#!/bin/bash
#SBATCH --job-name=FIN_MY
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=8

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes
mkdir masks

. ~/conda/etc/profile.d/conda.sh
conda activate py2
python /lustre/work/mhoyosro/software/msmc_tools/makeMappabilityMask.py
```

### 6. Map the samples against the reference genome: 
```
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

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

bwa aln -t 64 mMyo.fa SRR7704823_1.fastq > SRR7704823_1.sai && 
bwa aln -t 64 mMyo.fa SRR7704823_2.fastq > SRR7704823_2.sai && 
BWA_THREAD=64 bwa sampe mMyo.fa SRR7704823_1.sai SRR7704823_2.sai SRR7704823_1.fastq SRR7704823_2.fastq > SRR7704823_pe.sam
```

### 7. Convert to bam and index 
```
#!/bin/bash
#SBATCH --job-name=bamMyo
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

OMP_NUM_THREADS=64 samtools view -bS SRR7704823_pe.sam > SRR7704823.bam
OMP_NUM_THREADS=64 samtools sort -o SRR7704823.sorted.bam SRR7704823.bam
OMP_NUM_THREADS=64 samtools index SRR7704823.sorted.bam
```


### 8.  Create the coverage files for each sample. This is how much of the reference chromosome is covered in each sample
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes
head -n 93 SRR7704823_pe.sam
```
This is the output:
```
@SQ     SN:scaffold_m19_p_1     LN:223369599
@SQ     SN:scaffold_m19_p_2     LN:217756413
@SQ     SN:scaffold_m19_p_3     LN:213723965
@SQ     SN:scaffold_m19_p_4     LN:130331158
@SQ     SN:scaffold_m19_p_5     LN:111266764
@SQ     SN:scaffold_m19_p_6     LN:101075066
@SQ     SN:scaffold_m19_p_7     LN:94448911
@SQ     SN:scaffold_m19_p_8     LN:94234955
@SQ     SN:scaffold_m19_p_9     LN:92776453
@SQ     SN:scaffold_m19_p_10    LN:80193900
@SQ     SN:scaffold_m19_p_11    LN:78476750
@SQ     SN:scaffold_m19_p_12    LN:74216526
@SQ     SN:scaffold_m19_p_13    LN:58607551
@SQ     SN:scaffold_m19_p_14    LN:55602309
@SQ     SN:scaffold_m19_p_15    LN:53400106
@SQ     SN:scaffold_m19_p_16    LN:53200087
@SQ     SN:scaffold_m19_p_17    LN:47534757
@SQ     SN:scaffold_m19_p_18    LN:43537823
@SQ     SN:scaffold_m19_p_19    LN:42769290
@SQ     SN:scaffold_m19_p_20    LN:25313220
@SQ     SN:scaffold_m19_p_21    LN:15591159
@SQ     SN:scaffold_m19_p_22    LN:8097369
@SQ     SN:scaffold_m19_p_23    LN:7815798
@SQ     SN:scaffold_m19_p_24    LN:6554382
@SQ     SN:scaffold_m19_p_25    LN:4996645
@SQ     SN:scaffold_m19_p_26    LN:3682276
@SQ     SN:scaffold_m19_p_27    LN:3557006
@SQ     SN:scaffold_m19_p_28    LN:3555632
@SQ     SN:scaffold_m19_p_29    LN:3393479
@SQ     SN:scaffold_m19_p_30    LN:3173525
@SQ     SN:scaffold_m19_p_31    LN:2913534
@SQ     SN:scaffold_m19_p_32    LN:2797511
@SQ     SN:scaffold_m19_p_33    LN:2461131
@SQ     SN:scaffold_m19_p_34    LN:2396235
@SQ     SN:scaffold_m19_p_35    LN:2395910
@SQ     SN:scaffold_m19_p_36    LN:2315537
@SQ     SN:scaffold_m19_p_37    LN:2205510
@SQ     SN:scaffold_m19_p_38    LN:2135428
@SQ     SN:scaffold_m19_p_39    LN:2080404
@SQ     SN:scaffold_m19_p_40    LN:2066723
@SQ     SN:scaffold_m19_p_41    LN:1964739
@SQ     SN:scaffold_m19_p_42    LN:1691905
@SQ     SN:scaffold_m19_p_43    LN:1569096
@SQ     SN:scaffold_m19_p_44    LN:1545942
@SQ     SN:scaffold_m19_p_45    LN:1459827
@SQ     SN:scaffold_m19_p_46    LN:1449802
@SQ     SN:scaffold_m19_p_47    LN:1408249
@SQ     SN:scaffold_m19_p_48    LN:1089875
@SQ     SN:scaffold_m19_p_49    LN:1086583
@SQ     SN:scaffold_m19_p_50    LN:1048190
@SQ     SN:scaffold_m19_p_51    LN:1038638
@SQ     SN:scaffold_m19_p_52    LN:842794
@SQ     SN:scaffold_m19_p_53    LN:769791
@SQ     SN:scaffold_m19_p_54    LN:738777
@SQ     SN:scaffold_m19_p_55    LN:715828
@SQ     SN:scaffold_m19_p_56    LN:694283
@SQ     SN:scaffold_m19_p_57    LN:679316
@SQ     SN:scaffold_m19_p_58    LN:642830
@SQ     SN:scaffold_m19_p_59    LN:630193
@SQ     SN:scaffold_m19_p_60    LN:626352
@SQ     SN:scaffold_m19_p_61    LN:578126
@SQ     SN:scaffold_m19_p_62    LN:544785
@SQ     SN:scaffold_m19_p_63    LN:522568
@SQ     SN:scaffold_m19_p_64    LN:372349
@SQ     SN:scaffold_m19_p_65    LN:353007
@SQ     SN:scaffold_m19_p_66    LN:319838
@SQ     SN:scaffold_m19_p_67    LN:268097
@SQ     SN:scaffold_m19_p_68    LN:239972
@SQ     SN:scaffold_m19_p_69    LN:213343
@SQ     SN:scaffold_m19_p_70    LN:206615
@SQ     SN:scaffold_m19_p_71    LN:188461
@SQ     SN:scaffold_m19_p_72    LN:147788
@SQ     SN:scaffold_m19_p_73    LN:125338
@SQ     SN:scaffold_m19_p_74    LN:124669
@SQ     SN:scaffold_m19_p_75    LN:104718
@SQ     SN:scaffold_m19_p_76    LN:104115
@SQ     SN:scaffold_m19_p_77    LN:98181
@SQ     SN:scaffold_m19_p_78    LN:97820
@SQ     SN:scaffold_m19_p_79    LN:97268
@SQ     SN:scaffold_m19_p_80    LN:91028
@SQ     SN:scaffold_m19_p_81    LN:88811
@SQ     SN:scaffold_m19_p_82    LN:84383
@SQ     SN:scaffold_m19_p_83    LN:84131
@SQ     SN:scaffold_m19_p_84    LN:71161
@SQ     SN:scaffold_m19_p_85    LN:63657
@SQ     SN:scaffold_m19_p_86    LN:60455
@SQ     SN:scaffold_m19_p_87    LN:56930
@SQ     SN:scaffold_m19_p_88    LN:56719
@SQ     SN:scaffold_m19_p_89    LN:55619
@SQ     SN:scaffold_m19_p_90    LN:45504
@SQ     SN:scaffold_m19_p_91    LN:42821
@SQ     SN:scaffold_m19_p_92    LN:15962
```
From the previous table create the following (in notepad++ or BB, spaces are tabulations)
```
NW_023416313.1	0	223369599
NW_023416324.1	0	217756413
NW_023416335.1	0	213723965
NW_023416346.1	0	130331158
NW_023416357.1	0	111266764
NW_023416368.1	0	101075066
NW_023416379.1	0	94448911
NW_023416390.1	0	94234955
NW_023416401.1	0	92776453
NW_023416314.1	0	80193900
NW_023416315.1	0	78476750
NW_023416316.1	0	74216526
NW_023416317.1	0	58607551
NW_023416318.1	0	55602309
NW_023416319.1	0	53400106
NW_023416320.1	0	53200087
NW_023416321.1	0	47534757
NW_023416322.1	0	43537823
NW_023416323.1	0	42769290
NW_023416325.1	0	25313220
NW_023416326.1	0	15591159
NW_023416327.1	0	8097369
NW_023416328.1	0	7815798
NW_023416329.1	0	6554382
NW_023416330.1	0	4765999
NW_023416331.1	0	3682276
NW_023416332.1	0	3557006
NW_023416333.1	0	3555632
NW_023416334.1	0	3393479
NW_023416336.1	0	3173525
NW_023416337.1	0	2913534
NW_023416338.1	0	2797511
NW_023416339.1	0	2461131
NW_023416340.1	0	2396235
NW_023416341.1	0	2395910
NW_023416342.1	0	2315537
NW_023416343.1	0	2205510
NW_023416344.1	0	2135428
NW_023416345.1	0	2080404
NW_023416347.1	0	2066723
NW_023416348.1	0	1964739
NW_023416349.1	0	1691905
NW_023416350.1	0	1569096
NW_023416351.1	0	1545942
NW_023416352.1	0	1459827
NW_023416353.1	0	1449802
NW_023416354.1	0	1408249
NW_023416355.1	0	1089875
NW_023416356.1	0	1086583
NW_023416358.1	0	1048190
NW_023416359.1	0	1038638
NW_023416360.1	0	842794
NW_023416361.1	0	769791
NW_023416362.1	0	738777
NW_023416363.1	0	715828
NW_023416364.1	0	694283
NW_023416365.1	0	679316
NW_023416366.1	0	642830
NW_023416367.1	0	630193
NW_023416369.1	0	626352
NW_023416370.1	0	578126
NW_023416371.1	0	544785
NW_023416372.1	0	522568
NW_023416373.1	0	372349
NW_023416375.1	0	319838
NW_023416376.1	0	268097
NW_023416377.1	0	239972
NW_023416378.1	0	213343
NW_023416380.1	0	206615
NW_023416381.1	0	188461
NW_023416382.1	0	147788
NW_023416374.1	0	126163
NW_023416383.1	0	125338
NW_023416384.1	0	124669
NW_023416385.1	0	104718
NW_023416386.1	0	104115
NW_023416387.1	0	98181
NW_023416388.1	0	97820
NW_023416389.1	0	97268
NW_023416391.1	0	91028
NW_023416392.1	0	88811
NW_023416393.1	0	84383
NW_023416394.1	0	84131
NW_023416395.1	0	71161
NW_023416396.1	0	63657
NW_023416397.1	0	60455
NW_023416398.1	0	56930
NW_023416399.1	0	56719
NW_023416400.1	0	55619
NW_023416402.1	0	45504
NW_023416403.1	0	42821
NC_029346.1	0	17213
```
Save the tables as: 
```
/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/mMyo_regions.bed
```
Now let's generate a BED file indicating the regions covered in our aligned bam file --> SRR7704823.sorted.bam. 
This will provide the coordinates of the regions having aligned reads
```
#!/bin/bash
#SBATCH --job-name=depth
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=32

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

OMP_NUM_THREADS=32 samtools bedcov mMyo_regions.bed SRR7704823.sorted.bam > SRR7704823_covered.bed
OMP_NUM_THREADS=32 samtools depth -b SRR7704823_covered.bed -r NW_023416313.1  SRR7704823.sorted.bam > depth_SRR7704823
```

### 9. Calculate the DEPTH 
```
awk '{sum += $3} END {print sum / NR}' depth_SRR7704823
```
The result is:
29.1005

### 10. Detect the sexual chromosomes
```
#Activate my Blast
. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate blast

mkdir -p /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/blast_sex
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/blast_sex

makeblastdb -in ../genomes/mMyo.fa -dbtype nucl -out mMyo_DB
ROOT=/lustre/scratch/mhoyosro/project1/MSMC2/SEX_MARKERS

blastn -query $ROOT/aJamAMELX.fasta -db mMyo_DB -out aJamAMELX_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/aJamPGK1.fasta -db mMyo_DB -out aJamPGK1_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/aJamZXDB.fasta -db mMyo_DB -out aJamZXDB_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/dRotAMELX.fasta -db mMyo_DB -out dRotAMELX_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/dRotPGK1.fasta -db mMyo_DB -out dRotPGK1_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/dRotSRY.fasta -db mMyo_DB -out dRotSRY_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/dRotZXDB.fasta -db mMyo_DB -out dRotZXDB_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/mDauZXDB.fasta -db mMyo_DB -out mDauZXDB_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/mMbrAMELX.fasta -db mMyo_DB -out mMbrAMELX_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/mMbrPGK1.fasta -db mMyo_DB -out mMbrPGK1_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/mMbrSRY.fasta -db mMyo_DB -out mMbrSRY_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/rFerAMELX.fasta -db mMyo_DB -out rFerAMELX_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/rFerPGK1.fasta -db mMyo_DB -out rFerPGK1_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/rFerZXDB.fasta -db mMyo_DB -out rFerZXDB_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/sHonAMELX.fasta -db mMyo_DB -out sHonAMELX_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/sHonPGK1.fasta -db mMyo_DB -out sHonPGK1_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/sHonSRY.fasta -db mMyo_DB -out sHonSRY_blast.txt -evalue 1e-5 -outfmt 6 
blastn -query $ROOT/sHonZXDB.fasta -db mMyo_DB -out sHonZXDB_blast.txt -evalue 1e-5 -outfmt 6
```
This is the result:
```
NW_023416321.1	1
NW_023416324.1	2
NW_023416329.1	5
NW_023416335.1	11
NW_023416346.1	80 --> I should not use this chromosome
NW_023416379.1	2
NW_023416401.1	10
```

### 11. Calculate the heterozygosity
```
#!/bin/bash
#SBATCH --job-name=MmHET
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=32

# Load the necessary modules
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.1

BAM="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/SRR7704823.sorted.bam" 

reference="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/mMyo.fa"

OMP_NUM_THREADS=32 bcftools mpileup -B -q 20 -Q 20 -C 50 -f $reference $BAM -o mMyo_pileup_H.bcf &&

grep -v "#"  mMyo_pileup_H.bcf | cut -f 5 | grep -v "<*>" | wc -l 
# Result = 2567135
grep -v "#"  mMyo_pileup_H.bcf | wc -l
```
The Result is = 1958873201  
The heterozygosity is:  2567135/1958873201=0.00131051616  
As this organism is diploid the value of heterozygosity that should be used is: 0.00131051616/2 = 0.00065525808  


### 12. Generate a pileup (mpileup):
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

mkdir output_sample_1 
mkdir -p masks2/sample_1

#!/bin/bash
#SBATCH --job-name=bmclerMM
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=32

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

# List of values of the argument -r
scaffolds=("NW_023416313.1" "NW_023416324.1" "NW_023416335.1" "NW_023416357.1" "NW_023416368.1" "NW_023416379.1" "NW_023416390.1" "NW_023416401.1" "NW_023416314.1" "NW_023416315.1" "NW_023416316.1" "NW_023416317.1" "NW_023416318.1" "NW_023416319.1" "NW_023416320.1" "NW_023416321.1" "NW_023416322.1" "NW_023416323.1" "NW_023416325.1" "NW_023416326.1" "NW_023416327.1" "NW_023416328.1" "NW_023416329.1" "NW_023416330.1" "NW_023416331.1" "NW_023416332.1" "NW_023416333.1" "NW_023416334.1" "NW_023416336.1" "NW_023416337.1" "NW_023416338.1" "NW_023416339.1" "NW_023416340.1" "NW_023416341.1" "NW_023416342.1" "NW_023416343.1" "NW_023416344.1" "NW_023416345.1" "NW_023416347.1" "NW_023416348.1" "NW_023416349.1" "NW_023416350.1" "NW_023416351.1" "NW_023416352.1" "NW_023416353.1" "NW_023416354.1" "NW_023416355.1" "NW_023416356.1" "NW_023416358.1" "NW_023416359.1" "NW_023416360.1" "NW_023416361.1" "NW_023416362.1" "NW_023416363.1" "NW_023416364.1" "NW_023416365.1" "NW_023416366.1" "NW_023416367.1" "NW_023416369.1" "NW_023416370.1" "NW_023416371.1" "NW_023416372.1" "NW_023416373.1" "NW_023416375.1" "NW_023416376.1" "NW_023416377.1" "NW_023416378.1" "NW_023416380.1" "NW_023416381.1" "NW_023416382.1" "NW_023416374.1" "NW_023416383.1" "NW_023416384.1" "NW_023416385.1" "NW_023416386.1" "NW_023416387.1" "NW_023416388.1" "NW_023416389.1" "NW_023416391.1" "NW_023416392.1" "NW_023416393.1" "NW_023416394.1" "NW_023416395.1" "NW_023416396.1" "NW_023416397.1" "NW_023416398.1" "NW_023416399.1" "NW_023416400.1" "NW_023416402.1" "NW_023416403.1")

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/mMyo.fa"

# Options for samtools mpileup
options="-B -q 20 -Q 20 -C 50 -g"

# Depth sample1
DEPTH_1=29.0899

# BAM1
BAM_1="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/SRR7704823.sorted.bam"  

# Bamcaller
TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/msmc-tools-master/bamCaller.py"

module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11
module load bcftools/1.11

for scaffold in "${scaffolds[@]}"; do
    samtools mpileup -B -q 20 -Q 20 -C 50 -u -r $scaffold -f $reference $BAM | bcftools call -c -V indels | bcftools view -i 'INFO/DP>10' | python ../msmc-tools-master/bamCaller.py $DEPTH masks3/$scaffold.mask.bed.gz | gzip -c >  output_sample_1.3/out.$scaffold.vcf.gz
done
```

### 14. Run generate_multihetsep.py
```
mkdir -p /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/multihetsep
```
```
#!/bin/bash
#SBATCH --job-name=mulmm
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=8

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/multihetsep

TOOL="/lustre/work/mhoyosro/software/msmc_tools/generate_multihetsep.py"
# Mask of the reference genome
MASKS="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/masks"
# Masks resulting from mpileup
NEGMASKS1="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/masks2/sample_1"
# VCFs resulting from mpileup
NEGMASKS2="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes/output_sample_1"


scaffolds=("NW_023416313.1" "NW_023416324.1" "NW_023416335.1" "NW_023416357.1" "NW_023416368.1" "NW_023416379.1" "NW_023416390.1" "NW_023416401.1" "NW_023416314.1" "NW_023416315.1" "NW_023416316.1" "NW_023416317.1" "NW_023416318.1" "NW_023416319.1" "NW_023416320.1" "NW_023416321.1" "NW_023416322.1" "NW_023416323.1" "NW_023416325.1" "NW_023416326.1" "NW_023416327.1" "NW_023416328.1" "NW_023416329.1" "NW_023416330.1" "NW_023416331.1" "NW_023416332.1" "NW_023416333.1" "NW_023416334.1" "NW_023416336.1" "NW_023416337.1" "NW_023416338.1" "NW_023416339.1" "NW_023416340.1" "NW_023416341.1" "NW_023416342.1" "NW_023416343.1" "NW_023416344.1" "NW_023416345.1" "NW_023416347.1" "NW_023416348.1" "NW_023416349.1" "NW_023416350.1" "NW_023416351.1" "NW_023416352.1" "NW_023416353.1" "NW_023416354.1" "NW_023416355.1" "NW_023416356.1" "NW_023416358.1" "NW_023416359.1" "NW_023416360.1" "NW_023416361.1" "NW_023416362.1" "NW_023416363.1" "NW_023416364.1" "NW_023416365.1" "NW_023416366.1" "NW_023416367.1" "NW_023416369.1" "NW_023416370.1" "NW_023416371.1" "NW_023416372.1" "NW_023416373.1" "NW_023416375.1" "NW_023416376.1" "NW_023416377.1" "NW_023416378.1" "NW_023416380.1" "NW_023416381.1" "NW_023416382.1" "NW_023416374.1" "NW_023416383.1" "NW_023416384.1" "NW_023416385.1" "NW_023416386.1" "NW_023416387.1" "NW_023416388.1" "NW_023416389.1" "NW_023416391.1" "NW_023416392.1" "NW_023416393.1" "NW_023416394.1" "NW_023416395.1" "NW_023416396.1" "NW_023416397.1" "NW_023416398.1" "NW_023416399.1" "NW_023416400.1" "NW_023416402.1" "NW_023416403.1")


for scaffold in "${scaffolds[@]}" 
do 
python $TOOL --mask=$NEGMASKS1/$scaffold.mask.bed.gz --mask=$MASKS/$scaffold.mask.bed.gz  $NEGMASKS2/out.$scaffold.vcf.gz > mMyo1_$scaffold.txt
done
```

### 15. Run generate_multihetsep.py
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
export PATH=/lustre/work/mhoyosro/software/msmc2-2.1.4/build/release:${PATH}

#Create a directory for the output:
mkdir -p MSMC2_output 

#Create variables
output="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/MSMC2_output"

#De
scaffolds=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_4" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")



for scaffold in "${scaffolds[@]}" 
do
msmc2 -o $output  -t 64 -i 20  -p 1*2+25*1+1*2+1*3 multihetsep_out3/mMyo_$scaffold.txt -m 0.00065525808 -I 0,1
done
```
<img width="1168" height="588" alt="image" src="https://github.com/user-attachments/assets/94644eee-8426-4fa8-b4f4-ba0f8bb7c1ac" />








