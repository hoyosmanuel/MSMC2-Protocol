Extract the neutral regions from the reference genome
=====================================================

.. note::

 The main objective of this step is to compute the intersection between the BED intervals derived from the reference genome mappability mask and the BED intervals representing intergenic regions from the corresponding genome annotation file.

.. image:: _static/pic.png
   :width: 400px
   :align: center


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


3) Get the Neutralomes
----------------------------------------

.. note::

 My TOGA annotations are in BED12 format, so they contain 12 columns. This format includes both gene and transcript intervals. I will use intergenic regions, as they are expected to be closer to neutrality. To do this, we will extract the columns corresponding to genes—specifically, the first six columns—and create a simplified BED file

.. code-block:: bash

	cd /lustre/scratch/mhoyosro/project1/MSMC2/hipposideros
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mHipLar1.2.pri.TOGA.bed >  hLar_justGENES.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/molossus
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mMolMol1.2.pri.TOGA.bed >  mMol_justGENES.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/myotis
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mMyoMyo1.6.pri.TOGA.bed >  mMyo_justGENES.bed
				
	cd /lustre/scratch/mhoyosro/project1/MSMC2/phyllostomus
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mPhyDis1.3.pri.TOGA.bed >  pDis_justGENES.bed
	
	cd /lustre/scratch/mhoyosro/project1/MSMC2/pipistrellus
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mPipKuh1.2.pri.TOGA.bed >  pKuh_justGENES.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/rhinolophus
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mRhiFer1.5.pri.TOGA.bed >  rFer_justGENES.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/rousettus
	cut -f1-6 /lustre/scratch/mhoyosro/project1/ANNOTATIONS/mRouAeg1.4.pri.TOGA.bed >  rAeg_justGENES.bed


4) Calculate the scaffold sizes of the reference genome
--------------------------------------------------------
.. code-block:: bash

	. /home/mhoyosro/conda/etc/profile.d/conda.sh
	conda activate alineador

	cd /lustre/scratch/mhoyosro/project1/GENOMES
	
	for file in *.fa; do
	    samtools faidx "$file"
	done

	cd /lustre/scratch/mhoyosro/project1/MSMC2/hipposideros
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa.fai>  hLar_genomeSIZE

	cd /lustre/scratch/mhoyosro/project1/MSMC2/molossus
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa.fai > mMol_genomeSIZE

	cd /lustre/scratch/mhoyosro/project1/MSMC2/myotis
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa.fai > mMyo_genomeSIZE

	cd /lustre/scratch/mhoyosro/project1/MSMC2/phyllostomus
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mPhyDis1.3.pri.fa.fai > pDis_genomeSIZE

	cd /lustre/scratch/mhoyosro/project1/MSMC2/pipistrellus
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mPipKuh1.2.pri.fa.fai > pKuh_genomeSIZE

	cd /lustre/scratch/mhoyosro/project1/MSMC2/rhinolophus
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mRhiFer1.5.pri.fa.fai > rFer_genomeSIZE

	cd /lustre/scratch/mhoyosro/project1/MSMC2/rousettus
	cut -f1-2 /lustre/scratch/mhoyosro/project1/GENOMES/mRouAeg1.4.pri.fa.fai > rAeg_genomeSIZE


5) Sort the files
------------------

.. code-block:: bash

	cd /lustre/scratch/mhoyosro/project1/MSMC2/hipposideros
	sort -k1,1 -k2,2n hLar_justGENES.bed > hLar_justGENES.sorted.bed
	sort -k1,1 -k2,2n hLar_genomeSIZE > hLar_sorted.genomeSIZE
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/molossus
	sort -k1,1 -k2,2n mMol_justGENES.bed > mMol_justGENES.sorted.bed
	sort -k1,1 -k2,2n mMol_genomeSIZE > mMol_sorted.genomeSIZE 
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/myotis
	sort -k1,1 -k2,2n mMyo_justGENES.bed > mMyo_justGENES.sorted.bed
	sort -k1,1 -k2,2n mMyo_genomeSIZE > mMyo_sorted.genomeSIZE 
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/phyllostomus
	sort -k1,1 -k2,2n pDis_justGENES.bed > pDis_justGENES.sorted.bed
	sort -k1,1 -k2,2n pDis_genomeSIZE > pDis_sorted.genomeSIZE 
	
	cd /lustre/scratch/mhoyosro/project1/MSMC2/pipistrellus
	sort -k1,1 -k2,2n pKuh_justGENES.bed > pKuh_justGENES.sorted.bed
	sort -k1,1 -k2,2n pKuh_genomeSIZE > pKuh_sorted.genomeSIZE 
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/rhinolophus
	sort -k1,1 -k2,2n rFer_justGENES.bed > rFer_justGENES.sorted.bed
	sort -k1,1 -k2,2n rFer_genomeSIZE > rFer_sorted.genomeSIZE 
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/rousettus
	sort -k1,1 -k2,2n rAeg_justGENES.bed > rAeg_justGENES.sorted.bed
	sort -k1,1 -k2,2n rAeg_genomeSIZE > rAeg_sorted.genomeSIZE


6) Merge overlapping gene regions
---------------------------------

.. note::

 bedtools merge combines genes that overlap or are adjacent into a single continuous region.

.. code-block:: bash

	. /home/mhoyosro/conda/etc/profile.d/conda.sh
	conda activate alineador
	
	cd /lustre/scratch/mhoyosro/project1/MSMC2/hipposideros
	bedtools merge -i hLar_justGENES.sorted.bed > hLar_merged_genes.bed
	 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/molossus
	bedtools merge -i mMol_justGENES.sorted.bed > mMol_merged_genes.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/myotis
	bedtools merge -i mMyo_justGENES.sorted.bed > mMyo_merged_genes.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/phyllostomus
	bedtools merge -i pDis_justGENES.sorted.bed > pDis_merged_genes.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/pipistrellus
	bedtools merge -i pKuh_justGENES.sorted.bed > pKuh_merged_genes.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/rhinolophus
	bedtools merge -i rFer_justGENES.sorted.bed > rFer_merged_genes.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/rousettus
	bedtools merge -i rAeg_justGENES.sorted.bed > rAeg_merged_genes.bed



7) Extend the flanking regions by ~10 kb
-----------------------------------------

.. note::

	. /home/mhoyosro/conda/etc/profile.d/conda.sh
	conda activate alineador

	cd /lustre/scratch/mhoyosro/project1/MSMC2/hipposideros
	bedtools slop -i hLar_merged_genes.bed -g hLar_sorted.genomeSIZE -b 10000 > hLar_genes_with_buffer.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/molossus
	bedtools slop -i mMol_merged_genes.bed -g mMol_sorted.genomeSIZE -b 10000 > mMol_genes_with_buffer.bed

	cd /lustre/scratch/mhoyosro/project1/MSMC2/myotis
	bedtools slop -i mMyo_merged_genes.bed -g mMyo_sorted.genomeSIZE -b 10000 > mMyo_genes_with_buffer.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/phyllostomus
	bedtools slop -i pDis_merged_genes.bed -g pDis_sorted.genomeSIZE -b 10000 > pDis_genes_with_buffer.bed
	
	cd /lustre/scratch/mhoyosro/project1/MSMC2/pipistrellus
	bedtools slop -i pKuh_merged_genes.bed -g pKuh_sorted.genomeSIZE -b 10000 > pKuh_genes_with_buffer.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/rhinolophus
	bedtools slop -i rFer_merged_genes.bed -g rFer_sorted.genomeSIZE -b 10000 > rFer_genes_with_buffer.bed
 
	cd /lustre/scratch/mhoyosro/project1/MSMC2/rousettus
	bedtools slop -i rAeg_merged_genes.bed -g rAeg_sorted.genomeSIZE -b 10000 > rAeg_genes_with_buffer.bed
