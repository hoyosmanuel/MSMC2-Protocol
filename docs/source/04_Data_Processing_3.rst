Map the samples to the Reference Genomes
===============================================

1) MAP the PACBIO reads first
-----------------------------

A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano hLar_mapper.sh

.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=hLarMPR
 #SBATCH --output=%x.%A_%a.out
 #SBATCH --error=%x.%A_%a.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64
 #SBATCH --mem=128G
 #SBATCH --array=0-2   # 2 jobs, (one per SRA) 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador
 # SRAs list
 SRAS=(SRR23683930 SRR23695894 SRR23695893)
 # Select the SRA acording to the arrayn index
 sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
 # Mapping
 bwa mem -t 64 -x pacbio $ROOT/mHipLar1.2.pri.fa SRAs/${sra}.fastq > ${sra}.sam
 samtools view -b ${sra}.sam > ${sra}.bam
 samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
 samtools index -@ 64 ${sra}.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
 samtools index ${sra}.filtered.bam

