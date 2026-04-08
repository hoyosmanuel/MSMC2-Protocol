The Mappability Mask
==============================================

.. note::

 Explicar que es esta mondá


1) Set directories
--------------------

.. code-block:: console

   cd /lustre/scratch/mhoyosro/project1/MSMC2
   mkdir hLar mMol mMyo pDis pKuh rFer rAeg


2) Index the genomes
-----------------------

.. code-block:: console

   cd /lustre/scratch/mhoyosro/project1/MSMC2
   nano indexer.sh

   #!/bin/bash
   #SBATCH --job-name=INDEX
   #SBATCH --output=%x.%A_%a.out
   #SBATCH --error=%x.%A_%a.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=12
   #SBATCH --array=1-7

   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador

   cd /lustre/scratch/mhoyosro/project1/GENOMES

   # LIST OF GENOMES

   GENOMAS=(
   /lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa
   /lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa
   /lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa
   /lustre/scratch/mhoyosro/project1/GENOMES/mPhyDis1.3.pri.fa
   /lustre/scratch/mhoyosro/project1/GENOMES/mPipKuh1.2.pri.fa
   /lustre/scratch/mhoyosro/project1/GENOMES/mRhiFer1.5.pri.fa
   /lustre/scratch/mhoyosro/project1/GENOMES/mRouAeg1.4.pri.fa
   )

   GENOMA=${GENOMAS[$SLURM_ARRAY_TASK_ID-1]}

   bwa index -p ${GENOMA}.bwa -a bwtsw -t $SLURM_NTASKS $GENOMA
