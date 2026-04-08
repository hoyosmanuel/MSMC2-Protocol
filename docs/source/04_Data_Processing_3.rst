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

B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano mMol_mapper.sh

.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=mMolMPR
 #SBATCH --output=%x.%A_%a.out
 #SBATCH --error=%x.%A_%a.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64
 #SBATCH --mem=128G
 #SBATCH --array=0-0   # 2 jobs, (one per SRA) 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador
 # SRAs list
 SRAS=(SRR11747792) 
 # Select the SRA acording to the arrayn index
 sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
 # Mapping
 bwa mem -t 64 -x pacbio $ROOT/mMolMol1.2.pri.fa SRAs/${sra}.fastq > ${sra}.sam
 samtools view -b ${sra}.sam > ${sra}.bam
 samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
 samtools index -@ 64 ${sra}.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
 samtools index ${sra}.filtered.bam

C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano mMyo_mapper.sh

.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=mMyoMPR
 #SBATCH --output=%x.%A_%a.out
 #SBATCH --error=%x.%A_%a.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64
 #SBATCH --array=0-2   # 2 jobs, (one per SRA) 
 
 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador
 # SRAs list
 SRAS=(SRR11650040 SRR11650041 SRR11650039)
 # Select the SRA acording to the arrayn index
 sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
 # Mapping
 bwa mem -t 64 -x pacbio $ROOT/mMyoMyo1.6.pri.fa SRAs/${sra}.fastq > ${sra}.sam
 samtools view -b ${sra}.sam > ${sra}.bam
 samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
 samtools index -@ 64 ${sra}.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
 samtools index ${sra}.filtered.bam

D) *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano pDis_mapper.sh

.. code-block:: bash

 nano pDis_mapper.sh

 #!/bin/bash
 #SBATCH --job-name=pDisMPR
 #SBATCH --output=%x.%A_%a.out
 #SBATCH --error=%x.%A_%a.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64
 #SBATCH --array=0-0 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador
 # SRAs list
 SRAS=(SRR11788443)
 # Select the SRA acording to the arrayn index
 sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
 # Mapping
 bwa mem -t 64 -x pacbio $ROOT/mPhyDis1.3.pri.fa SRAs/${sra}.fastq > ${sra}.sam
 samtools view -b ${sra}.sam > ${sra}.bam
 samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
 samtools index -@ 64 ${sra}.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
 samtools index ${sra}.filtered.bam

E) *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano pKuh_mapper.sh

.. code-block:: bash

 nano pDis_mapper.sh

 #!/bin/bash
 #SBATCH --job-name=pKuhMPR
 #SBATCH --output=%x.%A_%a.out
 #SBATCH --error=%x.%A_%a.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64
 #SBATCH --array=0-1 # 2 jobs, (one per SRA) 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador
 # SRAs list
 SRAS=(SRR11744991 SRR11744992) 
 # Select the SRA acording to the arrayn index
 sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
 # Mapping
 bwa mem -t 64 -x pacbio $ROOT/mPipKuh1.2.pri.fa SRAs/${sra}.fastq > ${sra}.sam
 samtools view -b ${sra}.sam > ${sra}.bam
 samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
 samtools index -@ 64 ${sra}.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
 samtools index ${sra}.filtered.bam

F) *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano rFer_mapper.sh

.. code-block:: bash

#!/bin/bash
#SBATCH --job-name=rFerMPR
#SBATCH --output=%x.%A_%a.out
#SBATCH --error=%x.%A_%a.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --array=0-0   # 2 jobs, (one per SRA) 

cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
#root 
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
# Load the necessary modules
. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador
# SRAs list
SRAS=(SRR11776490)
# Select the SRA acording to the arrayn index
sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
# Mapping
bwa mem -t 64 -x pacbio $ROOT/mRhiFer1.5.pri.fa SRAs/${sra}.fastq > ${sra}.sam
samtools view -b ${sra}.sam > ${sra}.bam
samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
samtools index -@ 64 ${sra}.sorted.bam
# Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
samtools index ${sra}.filtered.bam

