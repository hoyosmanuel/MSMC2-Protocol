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
.. note::

 Reference genome annotations were provided by the Ray Lab at Texas Tech. If annotations are not available, the analysis can still be carried out using only the mappability mask, although this may introduce biases due to sites under selection. To better approximate neutral evolution, we focused on intergenic regions, which are generally less affected by selection. These regions were then intersected with the mappability mask to define high-confidence callable sites, improving the reliability of effective population size estimates.

.. code-block:: bash
  cd /lustre/scratch/mhoyosro/project1/
  cp -r /lustre/scratch/mhoyosro/project3/GENOMES .
  /lustre/scratch/mhoyosro/project3/ANNOTATIONS
  cp *.TOGA.bed /lustre/scratch/mhoyosro/project1/
  cd /lustre/scratch/mhoyosro/project1/
  mkdir ANNOTATIONS
  mv *.bed ANNOTATIONS
