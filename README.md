# MSMC2-Protocol
Protocol to run MSMC2 in our system

## 1. Set Directories:
```
mkdir -p /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
```
## 2. Get the genomes using SRAtoolkit: 
##### Once SRAtoolkit is installed, set the path to call the program anytime:
```
export PATH=/lustre/work/mhoyosro/software/sratoolkit/bin:${PATH}
```
##### Set the destination of the subsequent downloads with this command
```
vdb-config -i
```
##### Download this genome from NCBI:
```
prefetch --max-size 99999999999 SRR21002045 
```
##### Move the downloaded genome from now and on the sample to the working dir:
```
mv SRR21002045.sra  /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
```
##### Decompress the sample
```
fasterq-dump SRR21002045.sra
```
##### Get the Reference Genome aPal.fa (This is the genome of _Antrozous pallidus_ from our lab)
```
mv aPal.fa /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
```
## 3. Index the Reference Genome: 
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes

module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11
 
bwa index aPal.fa
```

## 4. Prepare the Reference Genome for MSMC2: 

#### 4.1 Download SPLITFA from https://lh3lh3.users.sourceforge.net/snpable.shtml, 
##### Download SPLITFA into your computer to then move it through SFTP will be faster 
##### In my case, I am going to storage 'seqbility-20091110' in this location: /lustre/scratch/mhoyosro/project1/MSMC2/
```
cd seqbility-20091110
make
```
##### Set the path
```
export PATH=/lustre/scratch/mhoyosro/project1/MSMC2/seqbility-20091110:${PATH}
splitfa
```
##### If you see this:
splitfa <in.fa> [len=35]
##### . . . Then splitfa is working and some other relevant things inside of it too

#### 4.2 Break down the Reference Genome in k-mers 
##### By default SPLITFA will break whatever FASTA you feed into it in k-mers of 35 nucleotides, that will produce a lot of mini files.  
##### Pack all those mini files in bundles of a size of 20000000 units using the command split of bash
```
cd /lustre/scratch/mhoyosro/project1/aPal3/genomes
splitfa aPal.fa | split -l 20000000
```
#### 4.3 Put all the resulting fragments in one folder and conglomerate them
##### All the mini files will have a name starting with the letter x. 
##### Concatenate them and store them in a file called x_files.
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
mkdir x_files
mv x* x_files
cd x_files
cat x* >> ../REF_splitted
```
#### 4.4 Align the resulting fragments of the reference genome to the reference genome
##### As this can be very demanding for the machine is recommendable doing it through a submission  
```
nano mappability_1.sh
```
##### Paste this:
```
#!/bin/bash
#SBATCH --job-name=map_1
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=32

cd /lustre/scratch/mhoyosro/project1/aPal3/genomes

module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

#NEXT we are going to align all the fragmented bits of the reference to the reference itself. 
#This is going to create sites of very good alignments and sites not so well aligned. 
#The intension of this routine is to identify those sites 

bwa aln -t 32 -R 1000000 -O 3 -E 3 aPal.fa  REF_splitted  >  REF_splitted.sai 

#Create a .sam file

BWA_THREAD=32 bwa samse -f REF_splitted.sam  aPal.fa  REF_splitted.sai  REF_splitted

#Create the first map of mappability

perl /lustre/scratch/mhoyosro/project1/MSMC2/seqbility-20091110/gen_raw_mask.pl  REF_splitted.sam  > SRR21002045_rawmask.fa
/lustre/scratch/mhoyosro/project1/MSMC2/seqbility-20091110/gen_mask -l 35 -r 0.5 SRR21002045_rawmask.fa  > SRR21002045_mask.fa 

#End of the script
```
##### Run the Script
```
sbatch mappability_1.sh
```

#### 4.5 Finish the mappability mask
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3
mkdir masks
```
##### Download the software msmc-tools-master from here: https://github.com/stschiff/msmc-tools/archive/master.zip
##### I am going to storage msmc-tools-master in:  /lustre/scratch/mhoyosro/project1/MSMC2/
##### Inside of the msmc-tools-master directory there is a python script called 'makeMappabilityMask.py'
##### It is necessary to edit that python script. 
##### According to Jessika Rick https://github.com/jessicarick/msmc2_scripts the lines 26 and 30 must be modify in this fashion:

Line 26 --->  with open("/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/SRR21002045_mask.fa", "r") as f:

Line 26 --->  mask = MaskGenerator("/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/masks/{}.mask.bed.gz".format(chr), chr)


##### To run makeMappabilityMask.py its necessary to use python 2.7
```
. ~/conda/etc/profile.d/conda.sh
conda create --name py2 python=2.7
```


##### Run makeMappabilityMask.py in a Script
```
nano mappability_2.sh
```
##### Paste this:
```
#!/bin/bash
#SBATCH --dependency=afterok:123456789 (number of the previous job)
#SBATCH --job-name=map_2
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=1

. ~/conda/etc/profile.d/conda.sh
conda activate py2
python /lustre/scratch/mhoyosro/project1/MSMC2/msmc-tools-master/makeMappabilityMask.py
```
##### Run the Script
```
sbatch mappability_2.sh
```

## 5. Map the sample to the reference genome:

##### samming
```
nano samming.sh
```
##### Paste this:
```
#!/bin/bash
#SBATCH --job-name=align
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes

module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

bwa aln -t 64 aPal.fa SRR21002045_1.fastq > SRR21002045_1.sai
bwa aln -t 64 aPal.fa SRR21002045_2.fastq > SRR21002045_2.sai
BWA_THREAD=64 bwa sampe aPal.fa SRR21002045_1.sai SRR21002045_2.sai SRR21002045_1.fastq SRR21002045_2.fastq > SRR21002045_pe.sam
```
##### Run the Script
```
sbatch samming.sh
```
##### bamming
```
nano bamming.sh
```
##### Paste this:
```
#!/bin/bash
#SBATCH --dependency=afterok:123456789
#SBATCH --job-name=bamming
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo/genomes

OMP_NUM_THREADS=64 samtools view -bS SRR7704823_pe.sam > SRR7704823.bam
OMP_NUM_THREADS=64 samtools sort -o SRR7704823.sorted.bam SRR7704823.bam
OMP_NUM_THREADS=64 samtools index SRR7704823.sorted.bam
```
##### Run the Script
```
sbatch bamming.sh
```
 
## 6. Create a coverage file for the sample. This is how much of the reference chromosomes is covered in the sample

##### The coverage file is a bed file with 4 columns:
|	 Chromosome  |	 Start  |	 End  |	 Name  |
##### The best way to create the coverage file is using aPal.fa.ann as a mold
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes
nano aPal2_regions.bed
```
##### paste this table and that will be the coverage file 
```
manual_scaffold_1	0	213208487	manual_scaffold_1
manual_scaffold_2	0	127226425	manual_scaffold_2
manual_scaffold_3	0	124294368	manual_scaffold_3
manual_scaffold_4	0	121648339	manual_scaffold_4
manual_scaffold_5	0	120116823	manual_scaffold_5
manual_scaffold_6	0	119589896	manual_scaffold_6
manual_scaffold_7	0	114648712	manual_scaffold_7
manual_scaffold_8	0	114169096	manual_scaffold_8
manual_scaffold_9	0	104822725	manual_scaffold_9
manual_scaffold_10	0	99069476	manual_scaffold_10
manual_scaffold_11	0	98043556	manual_scaffold_11
manual_scaffold_12	0	88393773	manual_scaffold_12
manual_scaffold_13	0	87307183	manual_scaffold_13
manual_scaffold_14	0	86061107	manual_scaffold_14
manual_scaffold_15	0	73516920	manual_scaffold_15
manual_scaffold_16	0	63379709	manual_scaffold_16
manual_scaffold_17	0	60205001	manual_scaffold_17
manual_scaffold_18	0	54249902	manual_scaffold_18
manual_scaffold_19	0	46128862	manual_scaffold_19
manual_scaffold_20	0	29832411	manual_scaffold_20
manual_scaffold_21	0	16410395	manual_scaffold_21
manual_scaffold_22	0	11805321	manual_scaffold_22
manual_scaffold_23	0	143654050	manual_scaffold_23
manual_scaffold_24	0	2089243	manual_scaffold_24
manual_scaffold_25	0	1246078	manual_scaffold_25
manual_scaffold_26	0	667518	manual_scaffold_26
manual_scaffold_27	0	504406	manual_scaffold_27
manual_scaffold_28	0	372598	manual_scaffold_28
manual_scaffold_29	0	324733	manual_scaffold_29
manual_scaffold_30	0	323044	manual_scaffold_30
manual_scaffold_31	0	291286	manual_scaffold_31
manual_scaffold_32	0	202501	manual_scaffold_32
manual_scaffold_33	0	178832	manual_scaffold_33
manual_scaffold_34	0	161717	manual_scaffold_34
manual_scaffold_35	0	150794	manual_scaffold_35
manual_scaffold_36	0	137424	manual_scaffold_36
manual_scaffold_37	0	132252	manual_scaffold_37
manual_scaffold_38	0	130276	manual_scaffold_38
manual_scaffold_39	0	121233	manual_scaffold_39
manual_scaffold_40	0	113340	manual_scaffold_40
manual_scaffold_41	0	113249	manual_scaffold_41
manual_scaffold_42	0	111288	manual_scaffold_42
manual_scaffold_43	0	110113	manual_scaffold_43
manual_scaffold_44	0	109813	manual_scaffold_44
manual_scaffold_45	0	109067	manual_scaffold_45
manual_scaffold_46	0	108250	manual_scaffold_46
manual_scaffold_47	0	102996	manual_scaffold_47
manual_scaffold_49	0	103225	manual_scaffold_49
manual_scaffold_50	0	102497	manual_scaffold_50
manual_scaffold_51	0	94339	manual_scaffold_51
manual_scaffold_52	0	90104	manual_scaffold_52
manual_scaffold_53	0	84365	manual_scaffold_53
manual_scaffold_54	0	84358	manual_scaffold_54
manual_scaffold_55	0	83136	manual_scaffold_55
manual_scaffold_56	0	80014	manual_scaffold_56
manual_scaffold_57	0	79477	manual_scaffold_57
manual_scaffold_58	0	75056	manual_scaffold_58
manual_scaffold_59	0	75040	manual_scaffold_59
manual_scaffold_60	0	73787	manual_scaffold_60
manual_scaffold_61	0	71657	manual_scaffold_61
manual_scaffold_62	0	71141	manual_scaffold_62
manual_scaffold_63	0	70405	manual_scaffold_63
manual_scaffold_64	0	69762	manual_scaffold_64
manual_scaffold_65	0	66623	manual_scaffold_65
manual_scaffold_66	0	62790	manual_scaffold_66
manual_scaffold_67	0	60994	manual_scaffold_67
manual_scaffold_68	0	61374	manual_scaffold_68
manual_scaffold_69	0	59887	manual_scaffold_69
manual_scaffold_70	0	59877	manual_scaffold_70
manual_scaffold_71	0	59524	manual_scaffold_71
manual_scaffold_72	0	58887	manual_scaffold_72
manual_scaffold_73	0	56135	manual_scaffold_73
manual_scaffold_74	0	54464	manual_scaffold_74
manual_scaffold_75	0	54057	manual_scaffold_75
manual_scaffold_76	0	51746	manual_scaffold_76
manual_scaffold_77	0	50470	manual_scaffold_77
manual_scaffold_78	0	50122	manual_scaffold_78
manual_scaffold_79	0	49888	manual_scaffold_79
manual_scaffold_80	0	49999	manual_scaffold_80
manual_scaffold_81	0	50043	manual_scaffold_81
manual_scaffold_82	0	49996	manual_scaffold_82
manual_scaffold_83	0	49519	manual_scaffold_83
manual_scaffold_84	0	44551	manual_scaffold_84
manual_scaffold_85	0	43778	manual_scaffold_85
manual_scaffold_86	0	44017	manual_scaffold_86
manual_scaffold_87	0	36257	manual_scaffold_87
manual_scaffold_88	0	36030	manual_scaffold_88
manual_scaffold_89	0	35132	manual_scaffold_89
manual_scaffold_90	0	34960	manual_scaffold_90
manual_scaffold_91	0	33599	manual_scaffold_91
manual_scaffold_92	0	30882	manual_scaffold_92
manual_scaffold_93	0	29324	manual_scaffold_93
manual_scaffold_94	0	27731	manual_scaffold_94
manual_scaffold_95	0	26459	manual_scaffold_95
manual_scaffold_96	0	25809	manual_scaffold_96
manual_scaffold_97	0	19945	manual_scaffold_97
manual_scaffold_98	0	17584	manual_scaffold_98
manual_scaffold_99	0	17118	manual_scaffold_99
manual_scaffold_100	0	15977	manual_scaffold_100
manual_scaffold_101	0	13030	manual_scaffold_101
manual_scaffold_102	0	12872	manual_scaffold_102
manual_scaffold_103	0	12777	manual_scaffold_103
manual_scaffold_104	0	11940	manual_scaffold_104
manual_scaffold_105	0	10802	manual_scaffold_105
manual_scaffold_106	0	10180	manual_scaffold_106
manual_scaffold_107	0	9368	manual_scaffold_107
manual_scaffold_108	0	8690	manual_scaffold_108
manual_scaffold_109	0	7872	manual_scaffold_109
manual_scaffold_110	0	7763	manual_scaffold_110
manual_scaffold_111	0	7425	manual_scaffold_111
manual_scaffold_112	0	6478	manual_scaffold_112
manual_scaffold_113	0	6076	manual_scaffold_113
manual_scaffold_114	0	6026	manual_scaffold_114
manual_scaffold_115	0	5379	manual_scaffold_115
manual_scaffold_116	0	2082	manual_scaffold_116
```

## 7. Calculate the average depth to run a variant caller
```
module load gcc/9.2.0
module load bwa/0.7.17
module load samtools/1.11

OMP_NUM_THREADS=1 samtools bedcov aPal2_regions.bed SRR21002045.sorted.bam > SRR21002045_covered.bed
```


##### Define the variables
```
scaffolds=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_14" "manual_scaffold_15" "manual_scaffold_16" "manual_scaffold_17" "manual_scaffold_18" "manual_scaffold_19" "manual_scaffold_20" "manual_scaffold_21" "manual_scaffold_22" "manual_scaffold_23" "manual_scaffold_24" "manual_scaffold_25" "manual_scaffold_26" "manual_scaffold_27" "manual_scaffold_28" "manual_scaffold_29" "manual_scaffold_30" "manual_scaffold_31" "manual_scaffold_32" "manual_scaffold_33" "manual_scaffold_34" "manual_scaffold_35" "manual_scaffold_36" "manual_scaffold_37" "manual_scaffold_38" "manual_scaffold_39" "manual_scaffold_40" "manual_scaffold_41" "manual_scaffold_42" "manual_scaffold_43" "manual_scaffold_44" "manual_scaffold_45" "manual_scaffold_46" "manual_scaffold_47" "manual_scaffold_49" "manual_scaffold_50" "manual_scaffold_51" "manual_scaffold_52" "manual_scaffold_53" "manual_scaffold_54" "manual_scaffold_55" "manual_scaffold_56" "manual_scaffold_57" "manual_scaffold_58" "manual_scaffold_59" "manual_scaffold_60" "manual_scaffold_61" "manual_scaffold_62" "manual_scaffold_63" "manual_scaffold_64" "manual_scaffold_65" "manual_scaffold_66" "manual_scaffold_67" "manual_scaffold_68" "manual_scaffold_69" "manual_scaffold_70" "manual_scaffold_71" "manual_scaffold_72" "manual_scaffold_73" "manual_scaffold_74" "manual_scaffold_75" "manual_scaffold_76" "manual_scaffold_77" "manual_scaffold_78" "manual_scaffold_79" "manual_scaffold_80" "manual_scaffold_81" "manual_scaffold_82" "manual_scaffold_83" "manual_scaffold_84" "manual_scaffold_85" "manual_scaffold_86" "manual_scaffold_87" "manual_scaffold_88" "manual_scaffold_89" "manual_scaffold_90" "manual_scaffold_91" "manual_scaffold_92" "manual_scaffold_93" "manual_scaffold_94" "manual_scaffold_95" "manual_scaffold_96" "manual_scaffold_97" "manual_scaffold_98" "manual_scaffold_99" "manual_scaffold_100" "manual_scaffold_101" "manual_scaffold_102" "manual_scaffold_103" "manual_scaffold_104" "manual_scaffold_105" "manual_scaffold_106" "manual_scaffold_107" "manual_scaffold_108" "manual_scaffold_109" "manual_scaffold_110" "manual_scaffold_111" "manual_scaffold_112" "manual_scaffold_113" "manual_scaffold_114" "manual_scaffold_115" "manual_scaffold_116")
```

##### Using 20 threads
```
for scaffold in "${scaffolds[@]}"; do
OMP_NUM_THREADS=20 samtools depth -b SRR21002045_covered.bed -r $scaffold SRR21002045.sorted.bam > depth_SRR21002045_$scaffold.txt 
done
```
##### It is very important to use double carrot >> if not we would be overwritten
```
for scaffold in "${scaffolds[@]}"; do
cat depth_SRR21002045_$scaffold.txt >> SRR21002045_totaldepth.txt
done
```
##### Now calculate the average depth for the sample 
```
awk '{sum += $3} END {print sum / NR}' SRR21002045_totaldepth.txt
```
My is Result = 14.3127

##### Now we can erase all those spurious files 
```
rm depth_SRR21002045_manual_scaffold*
```

## 8. Calculate the heterozygosity
##### Calculate those bases different from the reference 
```
module load gcc/9.2.0
module load samtools/1.11
module load bcftools/1.11

BAM="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/SRR21002045.sorted.bam"
reference="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/aPal.fa"
OMP_NUM_THREADS=20 bcftools mpileup -B -q 20 -Q 20 -C 50 -f $reference $BAM -o SRR21002045_pileup_H.bcf
grep -v "#"  SRR21002045_pileup_H.bcf | cut -f 5 | grep -v "<*>" | wc -l
```
My is Result = 14.3127

##### Calculate the total of the lines
```
grep -v "#"  SRR21002045_pileup_H.bcf | wc -l
```
My is Result = 47487726

##### So the heterozygosity  will be  
41441/47487726 = 0.0008726676

##### As this organism is diploid the value of heterozygosity that should be used is:
0.0008726676/2 = 0.0004363338


## 9. Run Mpileup
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/
mkdir masks2 output_vcf
mkdir masks2.1 output_vcf.1
```
##### Define the variables
```
scaffolds=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_14" "manual_scaffold_15" "manual_scaffold_16" "manual_scaffold_17" "manual_scaffold_18" "manual_scaffold_19" "manual_scaffold_20" "manual_scaffold_21" "manual_scaffold_22" "manual_scaffold_23" "manual_scaffold_24" "manual_scaffold_25" "manual_scaffold_26" "manual_scaffold_27" "manual_scaffold_28" "manual_scaffold_29" "manual_scaffold_30" "manual_scaffold_31" "manual_scaffold_32" "manual_scaffold_33" "manual_scaffold_34" "manual_scaffold_35" "manual_scaffold_36" "manual_scaffold_37" "manual_scaffold_38" "manual_scaffold_39" "manual_scaffold_40" "manual_scaffold_41" "manual_scaffold_42" "manual_scaffold_43" "manual_scaffold_44" "manual_scaffold_45" "manual_scaffold_46" "manual_scaffold_47" "manual_scaffold_49" "manual_scaffold_50" "manual_scaffold_51" "manual_scaffold_52" "manual_scaffold_53" "manual_scaffold_54" "manual_scaffold_55" "manual_scaffold_56" "manual_scaffold_57" "manual_scaffold_58" "manual_scaffold_59" "manual_scaffold_60" "manual_scaffold_61" "manual_scaffold_62" "manual_scaffold_63" "manual_scaffold_64" "manual_scaffold_65" "manual_scaffold_66" "manual_scaffold_67" "manual_scaffold_68" "manual_scaffold_69" "manual_scaffold_70" "manual_scaffold_71" "manual_scaffold_72" "manual_scaffold_73" "manual_scaffold_74" "manual_scaffold_75" "manual_scaffold_76" "manual_scaffold_77" "manual_scaffold_78" "manual_scaffold_79" "manual_scaffold_80" "manual_scaffold_81" "manual_scaffold_82" "manual_scaffold_83" "manual_scaffold_84" "manual_scaffold_85" "manual_scaffold_86" "manual_scaffold_87" "manual_scaffold_88" "manual_scaffold_89" "manual_scaffold_90" "manual_scaffold_91" "manual_scaffold_92" "manual_scaffold_93" "manual_scaffold_94" "manual_scaffold_95" "manual_scaffold_96" "manual_scaffold_97" "manual_scaffold_98" "manual_scaffold_99" "manual_scaffold_100" "manual_scaffold_101" "manual_scaffold_102" "manual_scaffold_103" "manual_scaffold_104" "manual_scaffold_105" "manual_scaffold_106" "manual_scaffold_107" "manual_scaffold_108" "manual_scaffold_109" "manual_scaffold_110" "manual_scaffold_111" "manual_scaffold_112" "manual_scaffold_113" "manual_scaffold_114" "manual_scaffold_115" "manual_scaffold_116")

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/aPal.fa"

# Options for samtools mpileup
# -B, --no-BAQ            disable BAQ (per-Base Alignment Quality)
# -q, --min-MQ INT        skip alignments with mapQ smaller than INT [0]
# -Q, --min-BQ INT        skip bases with baseQ/BAQ smaller than INT [13]
# -C, --adjust-MQ INT     adjust mapping quality; recommended:50, disable:0 [0]
# -g --> samtools mpileup option `g` is functional, but deprecated. This option enables the BCF output
options="-B -q 20 -Q 20 -C 50 -g"

# Depth of the Sample
DEPTH=14.3127  

# BAM
BAM="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/SRR21002045.sorted.bam"
```

##### Run the commands
```
module load gcc/9.2.0
module load samtools/1.11
module load bcftools/1.11

# This command is considering those calls with more depth >9

for scaffold in "${scaffolds[@]}"; do
    samtools mpileup -B -q 20 -Q 20 -C 50 -u -r $scaffold -f $reference $BAM | bcftools call -c -V indels | bcftools view -i 'INFO/DP>9' | python ../msmc-tools-master/bamCaller.py $DEPTH masks2/$scaffold.mask.bed.gz | gzip -c >  output_vcf/out.$scaffold.vcf.gz
don
```
```
# This command will consider everything

for scaffold in "${scaffolds[@]}"; do
    samtools mpileup $options -r $scaffold -f $reference $BAM | bcftools call -c -V indels | python ../msmc-tools-master/bamCaller.py $DEPTH masks2.1/$scaffold.mask.bed.gz | gzip -c >  output_vcf.1/out.$scaffold.vcf.gz
done
```

##### Also we can send everything as a submission
```
#!/bin/bash
#SBATCH --job-name=mpileup
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

# Define the variables
scaffolds=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaf$

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/aPal.fa"

# Options for samtools mpileup
# -B, --no-BAQ            disable BAQ (per-Base Alignment Quality)
# -q, --min-MQ INT        skip alignments with mapQ smaller than INT [0]
# -Q, --min-BQ INT        skip bases with baseQ/BAQ smaller than INT [13]
# -C, --adjust-MQ INT     adjust mapping quality; recommended:50, disable:0 [0]
# -g --> samtools mpileup option `g` is functional, but deprecated. This option enables the BCF output
options="-B -q 20 -Q 20 -C 50 -g"

# Depth sample1
DEPTH=14.3127

# BAM
BAM="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/genomes/SRR21002045.sorted.bam"

module load gcc/9.2.0
module load samtools/1.11
module load bcftools/1.11

for scaffold in "${scaffolds[@]}"; do
    samtools mpileup -B -q 20 -Q 20 -C 50 -u -r $scaffold -f $reference $BAM | bcftools call -c -V indels | bcftools view -i 'INFO/DP>9' | python ../msmc-tools-master/bamCaller.py $DEPTH masks2/$scaffold.mask.bed.gz | gzip -c >  output_vcf/out.$scaffold.vcf.gz
done

for scaffold in "${scaffolds[@]}"; do
    samtools mpileup $options -r $scaffold -f $reference $BAM | bcftools call -c -V indels | python ../msmc-tools-master/bamCaller.py $DEPTH masks2.1/$scaffold.mask.bed.gz | gzip -c >  output_vcf.1/out.$scaffold.vcf.gz
done


## 10. Run Generate Multihetset

cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3
mkdir multihetset multihetset.1

#This script is the main workhorse to generate input files for msmc for one chromosome.
# Define the variables

# These variables are for the data with values to a depth >9
scaffolds1=("manual_scaffold_1" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_14" "manual_scaffold_15" "manual_scaffold_16" "manual_scaffold_17" "manual_scaffold_18" "manual_scaffold_19" "manual_scaffold_2" "manual_scaffold_20" "manual_scaffold_22" "manual_scaffold_25" "manual_scaffold_27" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_6" "manual_scaffold_65" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_93" )

# These variables are for the data with no restriction of depth 
scaffolds2=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_14" "manual_scaffold_15" "manual_scaffold_16" "manual_scaffold_17" "manual_scaffold_18" "manual_scaffold_19" "manual_scaffold_20" "manual_scaffold_21" "manual_scaffold_22" "manual_scaffold_23" "manual_scaffold_24" "manual_scaffold_25" "manual_scaffold_26" "manual_scaffold_27" "manual_scaffold_28" "manual_scaffold_29" "manual_scaffold_30" "manual_scaffold_31" "manual_scaffold_32" "manual_scaffold_33" "manual_scaffold_34" "manual_scaffold_35" "manual_scaffold_36" "manual_scaffold_37" "manual_scaffold_38" "manual_scaffold_39" "manual_scaffold_40" "manual_scaffold_41" "manual_scaffold_42" "manual_scaffold_43" "manual_scaffold_44" "manual_scaffold_45" "manual_scaffold_46" "manual_scaffold_47" "manual_scaffold_49" "manual_scaffold_50" "manual_scaffold_51" "manual_scaffold_52" "manual_scaffold_53" "manual_scaffold_54" "manual_scaffold_55" "manual_scaffold_56" "manual_scaffold_57" "manual_scaffold_58" "manual_scaffold_59" "manual_scaffold_60" "manual_scaffold_61" "manual_scaffold_62" "manual_scaffold_63" "manual_scaffold_64" "manual_scaffold_65" "manual_scaffold_66" "manual_scaffold_67" "manual_scaffold_68" "manual_scaffold_69" "manual_scaffold_70" "manual_scaffold_71" "manual_scaffold_72" "manual_scaffold_73" "manual_scaffold_74" "manual_scaffold_75" "manual_scaffold_76" "manual_scaffold_77" "manual_scaffold_78" "manual_scaffold_79" "manual_scaffold_80" "manual_scaffold_81" "manual_scaffold_82" "manual_scaffold_83" "manual_scaffold_84" "manual_scaffold_85" "manual_scaffold_86" "manual_scaffold_87" "manual_scaffold_88" "manual_scaffold_89" "manual_scaffold_90" "manual_scaffold_91" "manual_scaffold_92" "manual_scaffold_93" "manual_scaffold_94" "manual_scaffold_95" "manual_scaffold_96" "manual_scaffold_97" "manual_scaffold_98" "manual_scaffold_99" "manual_scaffold_100" "manual_scaffold_101" "manual_scaffold_102" "manual_scaffold_103" "manual_scaffold_104" "manual_scaffold_105" "manual_scaffold_106" "manual_scaffold_107" "manual_scaffold_108" "manual_scaffold_109" "manual_scaffold_110" "manual_scaffold_111" "manual_scaffold_112" "manual_scaffold_113" "manual_scaffold_114" "manual_scaffold_115" "manual_scaffold_116")


masks="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/masks"

TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/msmc-tools-master/generate_multihetsep.py"

masks2="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/masks2"
masks21="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/masks2.1"

output_vcf="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/output_vcf"
output_vcf.1="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/output_vcf.1"

# Run the command

# Command for the data with values to a depth >9
for scaffold in "${scaffolds1[@]}" 
do 
python $TOOL --mask $masks/$scaffold.mask.bed.gz --mask $masks2/$scaffold.mask.bed.gz $output_vcf/out.$scaffold.vcf.gz > /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/multihetset/$scaffold.txt
done 

# Command  for the data with no restriction of depth 
for scaffold in "${scaffolds2[@]}" 
do 
python $TOOL --mask $masks/$scaffold.mask.bed.gz --mask $masks21/$scaffold.mask.bed.gz $output_vcf.1/out.$scaffold.vcf.gz > /lustre/scratch/mhoyosro/project1/MSMC2/aPal3/multihetset.1/$scaffold.txt
done 
```



## 11. Run MSMC2
```
cd /lustre/scratch/mhoyosro/project1/MSMC2/aPal3
export PATH=/lustre/work/mhoyosro/software/msmc2-2.1.4/build/release:${PATH}
```
##### Create a directory for the output:
mkdir -p MSMC2_output 

##### Set variables
##### Scaffolds 23 y 24 are sexual chromosomes, poorly represented actually, they are excluded because their depth was not good and sexual chromosomes should not be in the analysis
```
output="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/MSMC2_output/"
```
```
scaffolds=("manual_scaffold_1" "manual_scaffold_13" "manual_scaffold_14" "manual_scaffold_15" "manual_scaffold_18" "manual_scaffold_19" "manual_scaffold_2" "manual_scaffold_25" "manual_scaffold_27" "manual_scaffold_4" "manual_scaffold_65" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_93")
```
```
scaffolds1=("manual_scaffold_1" "manual_scaffold_13" "manual_scaffold_14" "manual_scaffold_15" "manual_scaffold_18" "manual_scaffold_19" "manual_scaffold_2")
```

##### Run the command

```
for scaffold in "${scaffolds[@]}" 
do
msmc2 -o $output  -t 12 -i 20  -p 1*2+25*1+1*2+1*3 multihetset/$scaffold.txt -m 0.0004363338 -I 0,1
done
```

```
for scaffold in "${scaffolds1[@]}" 
do
msmc2 -o $output  -t 12 -i 20  -p 1*2+25*1+1*2+1*3 multihetset.1/$scaffold.txt -m 0.0004363338 -I 0,1
done
```

## 12. Plot in R

```
#Set working direcrory
setwd("D:/POSGRADO/DOCTORADO")

#Mu is the mutation rate of the mammals (Mutation rates in mammalian genomes --- Sudhir Kumar and Sankar SubramanianAuthors Info & Affiliations --- January 15, 2002 --- 99 (2) 803-808 ---https://doi.org/10.1073/pnas.022629899 
  mu <- 2.2e-9
  gen <- 1.2

#Read the table in this output file output="/lustre/scratch/mhoyosro/project1/MSMC2/aPal3/MSMC2_output/"
  aPal<-read.table("MSMC-tutorial-files/results/MNL.msmc2.final.txt", header=TRUE)

#Make the plot
  plot(
    aPal$left_time_boundary/mu*gen, 
    (1/aPal$lambda)/(2*mu),
    ylim = c(0, 2e8),
    xlim = c(0, 2e6),
    type="s", 
    col="red", 
    xlab="Years ago", 
    ylab="effective population size")
  
 #Add some legends

  legend("topright",legend=c("Antrozous pallidus"), col=c("red"), lty=c(1,1))
