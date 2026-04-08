The Mappability Masks of the Reference Genomes
===============================================

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


3) Start the Mappability Mask for each species
-----------------------------------------------

.. code-block:: console

  cd /lustre/scratch/mhoyosro/project1/MSMC2

A) Mask for *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano hLar_maskr.sh

.. code-block:: console

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mHipLar1.2.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../hLar_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mHipLar1.2.pri.fa  hLar_splitted  >  hLar_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f hLar_splitted.sam  $BASE_DIR/mHipLar1.2.pri.fa  hLar_splitted.sai  hLar_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  hLar_splitted.sam   >  hLar_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 hLar_genome_rawmask.fa > hLar.genome.mask.fa


B) Mask for *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano mMol_maskr.sh

.. code-block:: console

  cd /lustre/scratch/mhoyosro/project1/MSMC2

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mMolMol1.2.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../mMol_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mMolMol1.2.pri.fa  mMol_splitted  >  mMol_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f mMol_splitted.sam  $BASE_DIR/mMolMol1.2.pri.fa  mMol_splitted.sai  mMol_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  mMol_splitted.sam   >  mMol_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 mMol_genome_rawmask.fa > mMol.genome.mask.fa


C) Mask for *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano mMyo_maskr.sh

.. code-block:: console

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mMyoMyo1.6.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../mMyo_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mMyoMyo1.6.pri.fa  mMyo_splitted  >  mMyo_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f mMyo_splitted.sam  $BASE_DIR/mMyoMyo1.6.pri.fa  mMyo_splitted.sai  mMyo_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  mMyo_splitted.sam   >  mMyo_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 mMyo_genome_rawmask.fa > mMyo.genome.mask.fa


D) Mask for *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano pDis_maskr.sh

.. code-block:: console

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mPhyDis1.3.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../pDis_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mPhyDis1.3.pri.fa  pDis_splitted  >  pDis_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f pDis_splitted.sam  $BASE_DIR/mPhyDis1.3.pri.fa  pDis_splitted.sai  pDis_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  pDis_splitted.sam   >  pDis_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 pDis_genome_rawmask.fa > pDis.genome.mask.fa


E) Mask for *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano pKuh_maskr.sh

.. code-block:: console

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mPipKuh1.2.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../pKuh_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mPipKuh1.2.pri.fa  pKuh_splitted  >  pKuh_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f pKuh_splitted.sam  $BASE_DIR/mPipKuh1.2.pri.fa  pKuh_splitted.sai  pKuh_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  pKuh_splitted.sam   >  pKuh_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 pKuh_genome_rawmask.fa > pKuh.genome.mask.fa


F) Mask for *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano rFer_maskr.sh

.. code-block:: console

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mRhiFer1.5.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../rFer_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mRhiFer1.5.pri.fa  rFer_splitted  >  rFer_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f rFer_splitted.sam  $BASE_DIR/mRhiFer1.5.pri.fa  rFer_splitted.sai  rFer_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  rFer_splitted.sam   >  rFer_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 rFer_genome_rawmask.fa > rFer.genome.mask.fa


G) Mask for *Rousettus aegyptiacus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

  nano rAeg_maskr.sh

.. code-block:: console

  #!/bin/bash
  #SBATCH --job-name=MASKR
  #SBATCH --output=%x.%j.out
  #SBATCH --error=%x.%j.err
  #SBATCH --partition=nocona
  #SBATCH --nodes=1
  #SBATCH --ntasks=64

  # Activate the environment
  . /home/mhoyosro/conda/etc/profile.d/conda.sh
  conda activate alineador
  # Enter into the directory
  cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
  # Base directory
  BASE_DIR="/lustre/scratch/mhoyosro/project1/GENOMES"
  # Put the Splitfa software into the path
  export PATH=/lustre/work/mhoyosro/software/seqbility/seqbility-20091110/:${PATH}
  # Break down the reference genome in kmers
  mkdir x_files
  splitfa $BASE_DIR/mRouAeg1.4.pri.fa | split -l 20000000
  mv x* x_files
  cd x_files
  cat x* >> ../rAeg_splitted
  cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
  # Aling the spplited reference to the Genome
  bwa aln -t 64 -O 3 -E 3  $BASE_DIR/mRouAeg1.4.pri.fa  rAeg_splitted  >  rAeg_splitted.sai
  # Pass the sai file to a sam file
  bwa samse -f rAeg_splitted.sam  $BASE_DIR/mRouAeg1.4.pri.fa  rAeg_splitted.sai  rAeg_splitted
  # Create the RawMask
  perl /lustre/scratch/mhoyosro/project1/seqbility/gen_raw_mask.pl  rAeg_splitted.sam   >  rAeg_genome_rawmask.fa
  # Create the Mask
  gen_mask -l 35 -r 0.5 rAeg_genome_rawmask.fa > rAeg.genome.mask.fa


