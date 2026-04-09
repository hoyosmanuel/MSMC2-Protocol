Extract the neutral regions from the reference genome
=====================================================

1) Set new directories for the neutralome
------------------------------------------

.. code-block:: bash

  mkdir /lustre/scratch/mhoyosro/project1/MSMC2
  cd /lustre/scratch/mhoyosro/project1/MSMC2
  mkdir hipposideros molossus myotis phyllostomus pipistrellus rhinolophus rousettus


2) Get the genomes and the Annotations
----------------------------------------

cd /lustre/scratch/mhoyosro/project1/
cp -r /lustre/scratch/mhoyosro/project3/GENOMES .
/lustre/scratch/mhoyosro/project3/ANNOTATIONS
cp *.TOGA.bed /lustre/scratch/mhoyosro/project1/
cd /lustre/scratch/mhoyosro/project1/
mkdir ANNOTATIONS
mv *.bed ANNOTATIONS
