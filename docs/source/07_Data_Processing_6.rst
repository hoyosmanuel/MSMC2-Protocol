.. note::

 The importance of sequencing depth in population inference is well summarized by Fumagalli (2023): “Sequencing depth is an important characteristic of the data. Genotypes called for sites with higher depth are likely to be more accurate, while lower sequencing depth leads to a non-negligible amount of genotyping uncertainty. Since SNP calling proceeds from genotype calling, sequencing depth influences the detection of variable sites.” In this study average sequencing depth was estimated using samtools depth (Li et al. 2009 "The SAMtools paper"), focusing on the largest scaffold of the reference genome as a representative region. This is an empirical approach that provides a practical approximation of genome-wide coverage but other strategies may also be applied.


Depth
=======================

1) Determine which is the largest scaffold of the genome
---------------------------------------------------------

A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mHipLar1.2.pri.fa.fai > hLar.genome.sorted.txt

Largest scaffold = manual_scaffold_1

B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mMolMol1.2.pri.fa.fai > mMol.genome.sorted.txt

Largest scaffold = scaffold_m16_p_1

C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mMyoMyo1.6.pri.fa.fai > mMyo.genome.sorted.txt

Largest scaffold = scaffold_m19_p_1

D) *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mPhyDis1.3.pri.fa.fai > pDis.genome.sorted.txt

Largest scaffold = scaffold_m19_p_1

E) *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mPipKuh1.2.pri.fa.fai > pKuh.genome.sorted.txt

Largest scaffold = scaffold_m20_p_1

F) *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mRhiFer1.5.pri.fa.fai > rFer.genome.sorted.txt

Largest scaffold = scaffold_m29_p_1

G) *Rousettus aegyptiacus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
 ROOT=/lustre/scratch/mhoyosro/project1/GENOMES
 sort -k2,2nr $ROOT/mRouAeg1.4.pri.fa.fai > rAeg.genome.sorted.txt

Largest scaffold = scaffold_m13_p_1


2) Run samtools depth for each sample
---------------------------------------------------------

.. code-block:: bash

nano depth.sh

.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=depth
 #SBATCH --output=%x.%j.out
 #SBATCH --error=%x.%j.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=32

 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador 

 # for Hipposideros larvatus
 cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
 OMP_NUM_THREADS=32 samtools depth -r manual_scaffold_1 SRR23695894.sorted.bam > depth_SRR23695894.txt
 OMP_NUM_THREADS=32 samtools depth -r manual_scaffold_1 SRR23695893.sorted.bam > depth_SRR23695893.txt
 OMP_NUM_THREADS=32 samtools depth -r manual_scaffold_1 SRR23683930.sorted.bam > depth_SRR23683930.txt

 # for Molossus molossus
 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m16_p_1 SRR11747789.sorted.bam > depth_SRR11747789.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m16_p_1 SRR11747790.sorted.bam > depth_SRR11747790.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m16_p_1 SRR11747792.sorted.bam > depth_SRR11747792.txt

 # for Myotis myotis
 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR11650039.sorted.bam > depth_SRR11650039.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR11650040.sorted.bam > depth_SRR11650040.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR11650041.sorted.bam > depth_SRR11650041.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR27216487.sorted.bam > depth_SRR27216487.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR27216488.sorted.bam > depth_SRR27216488.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR27216489.sorted.bam > depth_SRR27216489.txt

 # for Phyllostomus discolor
 cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR11788443.sorted.bam > depth_SRR11788443.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR25743055.sorted.bam > depth_SRR25743055.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR25743067.sorted.bam > depth_SRR25743067.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR25743100.sorted.bam > depth_SRR25743100.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m19_p_1 SRR25743112.sorted.bam > depth_SRR25743112.txt

 # for Pipistrellus kuhlii
 cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m20_p_1 SRR11744706.sorted.bam > depth_SRR11744706.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m20_p_1 SRR11744991.sorted.bam > depth_SRR11744991.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m20_p_1 SRR11744992.sorted.bam > depth_SRR11744992.txt

 # for Rhinolophus ferrumequinum
 cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m29_p_1 SRR11776490.sorted.bam > depth_SRR11776490.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m29_p_1 SRR11777081.sorted.bam > depth_SRR11777081.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m29_p_1 SRR30056794.sorted.bam > depth_SRR30056794.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m29_p_1 SRR924361.sorted.bam > depth_SRR924361.txt

 # for Rousettus aegyptiacus
 cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m13_p_1 SRR11773195.sorted.bam > depth_SRR11773195.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m13_p_1 SRR11773636.sorted.bam > depth_SRR11773636.txt
 OMP_NUM_THREADS=32 samtools depth -r scaffold_m13_p_1 SRR7637819.sorted.bam > depth_SRR7637819.txt


3) Calculate Depth for each sample
---------------------------------------------------------

.. code-block:: bash

 nano depth2.sh


.. code-block:: bash

 #!/bin/bash
 #SBATCH --job-name=depth
 #SBATCH --output=%x.%j.out
 #SBATCH --error=%x.%j.err
 #SBATCH --partition=nocona
 #SBATCH --nodes=1
 #SBATCH --ntasks=1

 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate alineador 


 # For each line in the file, sum the value of the third field; at the end, print the sumatory and divide it by the number of records

 # for Hipposideros larvatus
 cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
 awk '{sum += $3} END {print sum / NR}' depth_SRR23695894.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR23695893.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR23683930.txt

 # for Molossus molossus
 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
 awk '{sum += $3} END {print sum / NR}' depth_SRR11747789.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11747790.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11747792.txt

 # for Myotis myotis
 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
 awk '{sum += $3} END {print sum / NR}' depth_SRR11650039.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11650040.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11650041.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR27216487.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR27216488.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR27216489.txt

 # for Phyllostomus discolor
 cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
 awk '{sum += $3} END {print sum / NR}' depth_SRR11788443.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR25743055.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR25743067.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR25743100.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR25743112.txt

 # for Pipistrellus kuhlii
 cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
 awk '{sum += $3} END {print sum / NR}' depth_SRR11744706.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11744991.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11744992.txt

 # for Rhinolophus ferrumequinum
 cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
 awk '{sum += $3} END {print sum / NR}' depth_SRR11776490.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11777081.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR30056794.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR924361.txt

 # for Rousettus aegyptiacus
 cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
 awk '{sum += $3} END {print sum / NR}' depth_SRR11773195.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR11773636.txt
 awk '{sum += $3} END {print sum / NR}' depth_SRR7637819.txt


4) Results of the previous operation
---------------------------------------------------------

A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 13.293
| 10.544
| 13.0935

B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 22.418
| 24.9835
| 41.6384

C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 4.62979
| 28.6231
| 32.4736
| 14.5317
| 18.5191
| 46.3561

D) *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 14.4049
| 7.83154
| 8.57277
| 8.59096
| 6.89059

E) *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 31.4564
| 21.7211
| 37.9392

F) *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 4.93611
| 14.3368
| 5.74006
| 8.78948

G) *Rousettus aegyptiacus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 24.2094
| 40.1932
| 29.9446


5) Create new directories for the posterior analysis
---------------------------------------------------------

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
 mkdir output_sample_894 output_sample_893 output_sample_930 
 mkdir masks2 && cd masks2 
 mkdir sample_894 sample_893 sample_930

 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
 mkdir output_sample_789 output_sample_790 output_sample_792 
 mkdir masks2 && cd masks2 
 mkdir sample_789 sample_790 sample_792

 cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
 mkdir output_sample_039 output_sample_040 output_sample_041 output_sample_487 output_sample_488 output_sample_489 
 mkdir masks2 && cd masks2 
 mkdir sample_039 sample_040 sample_041 sample_487 sample_488 sample_489 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
 mkdir  output_sample_443 output_sample_055 output_sample_067 output_sample_100 output_sample_112 
 mkdir masks2 && cd masks2 
 mkdir sample_443 sample_055 sample_067 sample_100 sample_112 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
 mkdir  output_sample_706 output_sample_991 output_sample_992 
 mkdir masks2 && cd masks2 
 mkdir sample_706 sample_991 sample_992 

 cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
 mkdir  output_sample_490 output_sample_081 output_sample_794 output_sample_361
 mkdir masks2 && cd masks2 
 mkdir sample_490 sample_081 sample_794 sample_361

 cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
 mkdir  output_sample_195 output_sample_636 output_sample_819
 mkdir masks2 && cd masks2 
 mkdir sample_195 sample_636 sample_819
