Software installation and workspace setup
=========================================

1) Set up working directories
-----------------------------

.. code-block:: bash

   mkdir -p /lustre/scratch/mhoyosro/project1/MSMC2
   # Create the working folders
   cd /lustre/scratch/mhoyosro/project1/MSMC2
   mkdir hLar mMol mMyo pDis pKuh rFer rAeg


2) Set up working directories
-----------------------------

.. code-block:: bash

  cd /lustre/scratch/mhoyosro/project1/MSMC2
  wget -O msmc-tools-master.zip "https://github.com/stschiff/msmc-tools/archive/master.zip" unzip msmc-tools-master.zip cd msmc-tools-master
  unzip msmc-tools-master.zip
  rm msmc-tools-master.zip
  # Put one copy of the msmc-tools-master in each working folder
  for directory in hLar mMol mMyo pDis pKuh rFer rAeg; do
      cp -r msmc-tools-master "$directory/"
  done


3) Install required software
----------------------------

The required software was installed using conda from the bioconda and conda-forge channels.

.. code-block:: bash

   conda create -n alineador \
       bwa \
       samtools \
       bcftools \
       bedtools \
       bedops \
       genmap \
       gff2bed \
       -c bioconda -c conda-forge

   conda activate alineador
