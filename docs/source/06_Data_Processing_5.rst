.. note::

 MSMC methods assume homogeneous recombination and diploid Mendelian inheritance (Mather et al., 2019). Therefore, excluding sex chromosomes (or sex-linked loci located on autosomes) from the main analysis is advisable. Here, we removed these regions prior to analysis. Alternative and potentially more robust approaches may exist; however, the following describes the procedure used in this study.


Detect sex chromosomes
=======================

1. Create a directories for sexual markers
-----------------------------------------------

.. code-block:: bash

 mkdir /lustre/scratch/mhoyosro/project1/SEX_MARKERS


2. Get sexual markers from Genbank
-----------------------------------------------

.. note::

 In this study, the markers KDM5C and ZFX (X-linked genes) and SRY (a Y-specific gene) were used. Reference sequences for these genes were obtained from GenBank using bat-derived FASTA files. These FASTA files are placed in the SEX_MARKERS directory. The SRY marker did not yield conclusive results.


3. Create the DataBases
------------------------

.. note::

 The reference genomes now must be formatted as BLAST databases to enable sequence searches..

.. code-block:: bash

 cd /lustre/scratch/mhoyosro/project1/SEX_MARKERS
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa -dbtype nucl -out hLar_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa -dbtype nucl -out mMol_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa -dbtype nucl -out mMyo_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mPhyDis1.3.pri.fa -dbtype nucl -out pDis_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mPipKuh1.2.pri.fa -dbtype nucl -out pKuh_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mRhiFer1.5.pri.fa -dbtype nucl -out rFer_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mRouAeg1.4.pri.fa -dbtype nucl -out rAeg_DB


4. Search in the DataBases
---------------------------

.. code-block:: bash

 #Look for the KDM5C first 
 blastn -query KDM5C_gene.fa -db hLar_DB -out hLar_res_KDM5C.txt -outfmt 6
 blastn -query KDM5C_gene.fa -db mMol_DB -out mMol_res_KDM5C.txt -outfmt 6
 blastn -query KDM5C_gene.fa -db mMyo_DB -out mMyo_res_KDM5C.txt -outfmt 6
 blastn -query KDM5C_gene.fa -db pDis_DB -out pDis_res_KDM5C.txt -outfmt 6
 blastn -query KDM5C_gene.fa -db pKuh_DB -out pKuh_res_KDM5C.txt -outfmt 6
 blastn -query KDM5C_gene.fa -db rFer_DB -out rFer_res_KDM5C.txt -outfmt 6
 blastn -query KDM5C_gene.fa -db rAeg_DB -out rAeg_res_KDM5C.txt -outfmt 6

 #Look for the ZFX 
 blastn -query ZFX_gene.fa -db hLar_DB -out hLar_res_ZFX.txt -outfmt 6
 blastn -query ZFX_gene.fa -db mMol_DB -out mMol_res_ZFX.txt -outfmt 6
 blastn -query ZFX_gene.fa -db mMyo_DB -out mMyo_res_ZFX.txt -outfmt 6
 blastn -query ZFX_gene.fa -db pDis_DB -out pDis_res_ZFX.txt -outfmt 6
 blastn -query ZFX_gene.fa -db pKuh_DB -out pKuh_res_ZFX.txt -outfmt 6
 blastn -query ZFX_gene.fa -db rFer_DB -out rFer_res_ZFX.txt -outfmt 6
 blastn -query ZFX_gene.fa -db rAeg_DB -out rAeg_res_ZFX.txt -outfmt 6

 #Look for the SRY
 blastn -query SRY_gene.fa -db hLar_DB -out hLar_res_SRY.txt -outfmt 6
 blastn -query SRY_gene.fa -db mMol_DB -out mMol_res_SRY.txt -outfmt 6
 blastn -query SRY_gene.fa -db mMyo_DB -out mMyo_res_SRY.txt -outfmt 6
 blastn -query SRY_gene.fa -db pDis_DB -out pDis_res_SRY.txt -outfmt 6
 blastn -query SRY_gene.fa -db pKuh_DB -out pKuh_res_SRY.txt -outfmt 6
 blastn -query SRY_gene.fa -db rFer_DB -out rFer_res_SRY.txt -outfmt 6
 blastn -query SRY_gene.fa -db rAeg_DB -out rAeg_res_SRY.txt -outfmt 6


5. Search in the DataBases
---------------------------

.. note::

 Based on these results, scaffold identities were assigned. Although alternative and potentially more robust approaches may exist, this was the strategy followed in this study.


A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 32 => 14 pairs of Autosomes + X Y 
| Chromosome X = manual_scaffold_14 


B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 48 => 22 pairs of Autosomes + X Y
| Chromosome X = scaffold_m16_p_2 & scaffold_m16_p_1

C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 44 => 20 pairs of Autosomes + X Y
| Chromosome X = scaffold_m19_p_4

D) *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 32 => 14 pairs of Autosomes + X Y
| Chromosome X = scaffold_m19_p_9 

E) *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 44 => 20 pairs of Autosomes + X Y
| Chromosome X = 16  (Scaffold 16 was tentatively assigned based on ZFX)

F) *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 58 => 27 pairs of Autosomes + X Y
| Chromosome X = scaffold_m29_p_1 

G) *Rousettus aegyptiacus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| 2n = 36 => 16 pairs of Autosomes + X Y
| Chromosome X = scaffold_m13_p_9 

