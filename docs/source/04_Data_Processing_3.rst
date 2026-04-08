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
 #SBATCH --array=0-2   # 3 jobs, (one per SRA) 

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
 #SBATCH --array=0-0   # 1 job, (meh) 

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
 #SBATCH --array=0-2   # 3 jobs, (one per SRA) 
 
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
 #SBATCH --array=0-0   # 1 job, (meh)  

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


G) *Rousettus aegyptiacus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano rAeg_mapper.sh

.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=rAegMPR
 #SBATCH --output=%x.%A_%a.out
 #SBATCH --error=%x.%A_%a.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64
 #SBATCH --array=0-0   # 1 job, (meh) 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador
 # SRAs list
 SRAS=(SRR11773195)
 # Select the SRA acording to the arrayn index
 sra=${SRAS[$SLURM_ARRAY_TASK_ID]}
 # Mapping
 bwa mem -t 64 -x pacbio $ROOT/mRouAeg1.4.pri.fa SRAs/${sra}.fastq > ${sra}.sam
 samtools view -b ${sra}.sam > ${sra}.bam
 samtools sort -@ 64 -o ${sra}.sorted.bam ${sra}.bam
 samtools index -@ 64 ${sra}.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 ${sra}.sorted.bam > ${sra}.filtered.bam
 samtools index ${sra}.filtered.bam


2) MAP the SHORT reads now
-----------------------------

A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

_No reads for this one_

B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 nano mMol_single_mapper.sh

.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=mMolmap
 #SBATCH --output=%x.%j.out
 #SBATCH --error=%x.%j.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=64

 # Load the necessary modules
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador

 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
 #root 
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 bwa aln -t 64 $ROOT/mMolMol1.2.pri.fa  SRAs/SRR11747789_1.fastq > SRR11747789_1.sai && 
 bwa aln -t 64 $ROOT/mMolMol1.2.pri.fa  SRAs/SRR11747789_2.fastq > SRR11747789_2.sai && 
 BWA_THREAD=64 bwa sampe $ROOT/mMolMol1.2.pri.fa SRR11747789_1.sai SRR11747789_2.sai SRR11747789_1.fastq  SRR11747789_2.fastq > SRR11747789.sam
 samtools view -b SRR11747789.sam > SRR11747789.bam
 samtools sort -@ 64 -o  SRR11747789.sorted.bam  SRR11747789.bam
 samtools index -@ 64 SRR11747789.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 SRR11747789.sorted.bam > SRR11747789.filtered.bam
 samtools index SRR11747789.filtered.bam

 bwa aln -t 64 $ROOT/mMolMol1.2.pri.fa  SRAs/SRR11747790_1.fastq > SRR11747790_1.sai && 
 bwa aln -t 64 $ROOT/mMolMol1.2.pri.fa  SRAs/SRR11747790_2.fastq > SRR11747790_2.sai && 
 BWA_THREAD=64 bwa sampe $ROOT/mMolMol1.2.pri.fa SRR11747790_1.sai SRR11747790_2.sai SRR11747790_1.fastq  SRR11747790_2.fastq > SRR11747790.sam
 samtools view -b SRR11747790.sam > SRR11747790.bam
 samtools sort -@ 64 -o  SRR11747790.sorted.bam  SRR11747790.bam
 samtools index -@ 64 SRR11747790.sorted.bam
 # Make a filter MAPQ  ^i  20 ^`^s30 -> -q 20 // Exclude supplement, secondary, unmapped, duplicated reads    
 samtools view -b -q 20 -F 2308 SRR11747790.sorted.bam > SRR11747790.filtered.bam
 samtools index SRR11747790.filtered.bam


C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~


D) *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~


E) *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~


F) *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nano mMyo_single_mapper.sh

#!/bin/bash
#SBATCH --job-name=mMyomap
#SBATCH --output=%x_%A_%a.out
#SBATCH --error=%x_%A_%a.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --array=1-3

set -euo pipefail

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
#root 
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
# SRAs list
SRAS=(SRAs/SRR27216487 SRAs/SRR27216488 SRAs/SRR27216489)

ID=${SRAS[$((SLURM_ARRAY_TASK_ID-1))]}

R1="${ID}_1.fastq"
R2="${ID}_2.fastq"

# Align
bwa aln -t 64 $ROOT/mMyoMyo1.6.pri.fa ${R1} > ${ID}_1.sai
bwa aln -t 64 $ROOT/mMyoMyo1.6.pri.fa ${R2} > ${ID}_2.sai

bwa sampe $ROOT/mMyoMyo1.6.pri.fa \
  ${ID}_1.sai ${ID}_2.sai \
  ${R1} ${R2} > ${ID}.sam

# Convert and sort
samtools sort -@ 64 -o ${ID}.sorted.bam ${ID}.sam
samtools index -@ 64 ${ID}.sorted.bam

# Filter MAPQ 20, remove supplementary, secondary, unmapped reads
samtools view -b -q 20 -F 2308 ${ID} > ${ID}.filtered.bam
samtools index ${ID}.filtered.bam



 

nano pDis_single_mapper.sh

#!/bin/bash
#SBATCH --job-name=pDismap
#SBATCH --output=%x_%A_%a.out
#SBATCH --error=%x_%A_%a.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --array=1-4

set -euo pipefail

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
#root 
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
# SRAs list
SRAS=(SRAs/SRR25743112 SRAs/SRR25743100 SRAs/SRR25743067 SRAs/SRR25743055)

ID=${SRAS[$((SLURM_ARRAY_TASK_ID-1))]}

R1="${ID}_1.fastq"
R2="${ID}_2.fastq"

# Align
bwa aln -t 64 $ROOT/mPhyDis1.3.pri.fa ${R1} > ${ID}_1.sai
bwa aln -t 64 $ROOT/mPhyDis1.3.pri.fa ${R2} > ${ID}_2.sai

bwa sampe $ROOT/mPhyDis1.3.pri.fa \
  ${ID}_1.sai ${ID}_2.sai \
  ${R1} ${R2} > ${ID}.sam

# Convert and sort
samtools sort -@ 64 -o ${ID}.sorted.bam ${ID}.sam
samtools index -@ 64 ${ID}.sorted.bam

# Filter MAPQ 20, remove supplementary, secondary, unmapped reads
samtools view -b -q 20 -F 2308 ${ID} > ${ID}.filtered.bam
samtools index ${ID}.filtered.bam




nano pKuh_single_mapper.sh

#!/bin/bash
#SBATCH --job-name=pKuhmap
#SBATCH --output=%x_%A_%a.out
#SBATCH --error=%x_%A_%a.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --array=1-1

set -euo pipefail

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
#root 
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES

# SRAs list
SRAS=(SRAs/SRR11744706)

ID=${SRAS[$((SLURM_ARRAY_TASK_ID-1))]}

R1="${ID}_1.fastq"
R2="${ID}_2.fastq"

# Align
bwa aln -t 64 $ROOT/mPipKuh1.2.pri.fa ${R1} > ${ID}_1.sai
bwa aln -t 64 $ROOT/mPipKuh1.2.pri.fa ${R2} > ${ID}_2.sai

bwa sampe $ROOT/mPipKuh1.2.pri.fa \
  ${ID}_1.sai ${ID}_2.sai \
  ${R1} ${R2} > ${ID}.sam

# Convert and sort
samtools sort -@ 64 -o ${ID}.sorted.bam ${ID}.sam
samtools index -@ 64 ${ID}.sorted.bam

# Filter MAPQ 20, remove supplementary, secondary, unmapped reads
samtools view -b -q 20 -F 2308 ${ID} > ${ID}.filtered.bam
samtools index ${ID}.filtered.bam




nano rFer_single_mapper.sh

#!/bin/bash
#SBATCH --job-name=rFermap
#SBATCH --output=%x_%A_%a.out
#SBATCH --error=%x_%A_%a.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --array=1-3

set -euo pipefail

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
#root 
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
# SRAs list
SRAS=(SRAs/SRR11777081 SRAs/SRR30056794 SRAs/SRR924361)

ID=${SRAS[$((SLURM_ARRAY_TASK_ID-1))]}

R1="${ID}_1.fastq"
R2="${ID}_2.fastq"

# Align
bwa aln -t 64 $ROOT/mRhiFer1.5.pri.fa ${R1} > ${ID}_1.sai
bwa aln -t 64 $ROOT/mRhiFer1.5.pri.fa ${R2} > ${ID}_2.sai

bwa sampe $ROOT/mRhiFer1.5.pri.fa \
  ${ID}_1.sai ${ID}_2.sai \
  ${R1} ${R2} > ${ID}.sam

# Convert and sort
samtools sort -@ 64 -o ${ID}.sorted.bam ${ID}.sam
samtools index -@ 64 ${ID}.sorted.bam

# Filter MAPQ 20, remove supplementary, secondary, unmapped reads
samtools view -b -q 20 -F 2308 ${ID} > ${ID}.filtered.bam
samtools index ${ID}.filtered.bam



nano rAeg_single_mapper.sh

#!/bin/bash
#SBATCH --job-name=rAegmap
#SBATCH --output=%x_%A_%a.out
#SBATCH --error=%x_%A_%a.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --array=1-2

set -euo pipefail

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
#root 
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
# SRAs list
SRAS=(SRAs/SRR11773636 SRAs/SRR7637819)

ID=${SRAS[$((SLURM_ARRAY_TASK_ID-1))]}

R1="${ID}_1.fastq"
R2="${ID}_2.fastq"

# Align
bwa aln -t 64 $ROOT/mRouAeg1.4.pri.fa ${R1} > ${ID}_1.sai
bwa aln -t 64 $ROOT/mRouAeg1.4.pri.fa ${R2} > ${ID}_2.sai

bwa sampe $ROOT/mRouAeg1.4.pri.fa \
  ${ID}_1.sai ${ID}_2.sai \
  ${R1} ${R2} > ${ID}.sam

# Convert and sort
samtools sort -@ 64 -o ${ID}.sorted.bam ${ID}.sam
samtools index -@ 64 ${ID}.sorted.bam

# Filter MAPQ 20, remove supplementary, secondary, unmapped reads
samtools view -b -q 20 -F 2308 ${ID} > ${ID}.filtered.bam
samtools index ${ID}.filtered.bam
