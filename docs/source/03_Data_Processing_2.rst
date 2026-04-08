Finish the Mappability Masks of the Reference Genomes
=====================================================

.. note::

   To complete the mappability mask for each genome, the file ``msmc-tools-master/makeMappabilityMask.py`` must be modified individually for each dataset. Since a copy of the ``msmc-tools-master`` directory has already been placed in each  working directory, you need to enter each of these directories and edit lines 26 and 30 of the ``makeMappabilityMask.py`` script.

   Below is an example for *hLar*:

.. code-block:: python

   #!/usr/bin/env python

   import gzip
   import sys

   class MaskGenerator:
       def __init__(self, filename, chr):
           self.lastCalledPos = -1
           self.lastStartPos = -1
           sys.stderr.write("making mask {}\n".format(filename))
           self.file = gzip.open(filename, "w")
           self.chr = chr

       # assume 1-based coordinate, output in bed format
       def addCalledPosition(self, pos):
           if self.lastCalledPos == -1:
               self.lastCalledPos = pos
               self.lastStartPos = pos
           elif pos == self.lastCalledPos + 1:
               self.lastCalledPos = pos
           else:
               self.file.write("{}\t{}\t{}\n".format(self.chr, self.lastStartPos - 1, self.lastCalledPos))
               self.lastStartPos = pos
               self.lastCalledPos = pos

   with open("/lustre/scratch/mhoyosro/project1/MSMC2/hLar/hLar.genome.mask.fa", "r") as f:
       for line in f:
           if line.startswith('>'):
               chr = line.split()[0][1:]
               mask = MaskGenerator("/lustre/scratch/mhoyosro/project1/MSMC2/hLar/map_mask/{}.mask.bed.gz".format(chr), chr)
               pos = 0
               continue
           for c in line.strip():
               pos += 1
               if pos % 1000000 == 0:
                   sys.stderr.write("processing pos:{}\n".format(pos))
               if c == "3":
                   mask.addCalledPosition(pos)



The original script: ``/lustre/scratch/mhoyosro/project1/MSMC2/hLar/msmc-tools-master/makeMappabilityMask.py`` was adapted by modifying line 26 and line 30 so that the input mask file and output ``.bed.gz`` files point to the ``hLar`` directory.


.. note::

   Once all scripts for each species have been modified, we can proceed with the following command. 

.. code-block:: python

   cd /lustre/scratch/mhoyosro/project1/MSMC2
   nano endr2.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=endr2
   #SBATCH --output=%x.%A_%a.out
   #SBATCH --error=%x.%A_%a.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=12
   #SBATCH --array=0-6

   . ~/conda/etc/profile.d/conda.sh
   conda activate py2

   # Array con los nombres de las especies
   SPECIES=(hLar mMol mMyo pDis pKuh rFer rAeg)

   # Obtener la especie correspondiente a este índice del array
   CURRENT_SPECIES=${SPECIES[$SLURM_ARRAY_TASK_ID]}

   # Ejecutar el script para la especie actual
   python /lustre/scratch/mhoyosro/project1/MSMC2/${CURRENT_SPECIES}/msmc-tools-master/makeMappabilityMask.py
